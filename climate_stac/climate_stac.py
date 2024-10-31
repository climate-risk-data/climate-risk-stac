"""Convert csv inputs to STAC."""

import pystac
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
import pandas as pd
from datetime import datetime
from shapely.geometry import Polygon, mapping
import numpy as np
import logging

from climate_stac.globals import cat_keywords, format_to_media_type
from climate_stac.utils import (
    compute_overall_bbox,
    generate_keywords,
    parse_year_range,
    providers_are_equal,
    update_keywords,
)

__all__ = [
    "create_catalog",
    "update_catalog_from_dataframe",
]

# Configure the logger
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("climate_stac")


def create_catalog() -> pystac.Catalog:
    """Create a new climate risk data STAC catalog."""
    # Create the main catalog
    catalog_main = pystac.Catalog(
        id="climate-risk-stac",
        title="Climate Risk STAC",
        description="This is a living, community-driven metadata catalog of geospatial datasets relevant for climate risk assessments (CRAs). The catalog is structured around the three risk drivers hazard, exposure, and vulnerability, with a focus on global-scale datasets. We provide detailed documentation on how to navigate the catalog, including a user guide (see 'Catalog documentation'). The development of the catalog is described in detail in the referenced publication (see 'Peer-reviewed publication'). As the catalog is designed to be a community-led endeavor, we encourage risk data users to add datasets to this catalog, thereby creating a growing knowledge base for potential users. New datasets can be submitted via GitHub (see 'Submit a new dataset').",
        )
    
    # Create catalog links
    documentation_link = pystac.Link(
        rel=pystac.RelType.VIA,
        target="https://climate-risk-data.github.io/climate-risk-stac/",
        title="Catalog documentation",
    )
    # Add the link to the catalog
    catalog_main.add_link(documentation_link)

    publication_link = pystac.Link(
        rel=pystac.RelType.VIA,
        target="https://doi.org/XXXXXXX",
        title="Peer-reviewed publication (will be added once published)",
    )
    # Add the link to the catalog
    catalog_main.add_link(publication_link)

    github_link = pystac.Link(
        rel=pystac.RelType.VIA,
        target="https://github.com/climate-risk-data/climate-risk-stac/issues/new/choose",
        title="Submit a new dataset",
    )
    # Add the link to the catalog
    catalog_main.add_link(github_link)

    return catalog_main


# Function to create collections and items
def update_catalog_from_dataframe(
    catalog: pystac.Catalog, dataframe: pd.DataFrame
) -> pystac.Catalog:
    """Update a STAC catalog with collections and items from a pandas dataframe."""
    indicator = dataframe.copy()
    catalog_main = catalog.full_copy()

    for row_num in range(len(indicator)):
        item = indicator.iloc[row_num]

        # Extract values from the row
        catalog_id = item["catalog"]
        category_id = item["category"]

        ## CATALOGS ##
        # Create or retrieve the first-level catalog
        if catalog_id not in [cat.id for cat in catalog_main.get_children()]:
            catalog1 = pystac.Catalog(
                id=catalog_id,
                title=catalog_id.capitalize(),
                description=f"{catalog_id.capitalize()} datasets",
            )
            catalog_main.add_child(catalog1)
        else:
            catalog1 = catalog_main.get_child(catalog_id)

        # Create or retrieve the second-level catalog
        if category_id not in [cat.id for cat in catalog1.get_children()]:
            catalog2 = pystac.Catalog(
                id=category_id,
                title=category_id.capitalize(),
                description=f"{category_id.capitalize()} datasets",
            )
            catalog1.add_child(catalog2)
        else:
            catalog2 = catalog1.get_child(category_id)

        # Process bbox (needed for collections and items)
        bbox = item["bbox"]
        bbox_list = [float(coord.strip()) for coord in bbox.split(",")]

        # Process temporal resolution (needed for collections and items)
        start, end = parse_year_range(str(item["temporal_coverage"]))

        ## COLLECTIONS ##
        # combine title and short title
        title_collection = (
            item["title_collection"] + " (" + item["title_short"] + ")"
            if not pd.isna(item["title_short"])
            else (item["title_collection"])
        )

        # make keywords
        keywords = generate_keywords(item)

        # make provider
        provider = pystac.Provider(
            name=item["provider_name"],
            # description= 'test test',
            roles=[pystac.ProviderRole(item["provider_role"])],
            url=item["data_overview_link"],
        )

        # Create or retrieve the collection
        if title_collection not in [col.id for col in catalog2.get_children()]:
            # create basic collection
            collection = pystac.Collection(
                id=title_collection,
                title=title_collection,
                description=item["description_collection"],
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent([bbox_list]),
                    temporal=pystac.TemporalExtent([[start, end]]),
                ),
                license=item["license"],
                keywords=keywords,
                providers=[provider],
                # extra_fields={ ## any extra field specified will be displayed in the 'Metadata' section ##
                #    'risk data type': item['risk_data_type'],
                #    'subcategory': item['subcategory']
                # }
            )

            catalog2.add_child(collection)

            logger.info(f"collection {row_num} {title_collection} successfully added")

        else:
            # retrieve collection
            collection = catalog2.get_child(title_collection)

            # Update spatial extent
            # get all items
            items = list(collection.get_all_items())
            # Compute the overall bbox from all items
            overall_bbox = compute_overall_bbox(items)
            # Update the collection bbox
            collection.extent.spatial.bboxes = [overall_bbox]
            logger.info(f"Updated collection bbox: {overall_bbox}")

            # Update temporal extent
            # Retrieve the current temporal extent
            exts = collection.extent.temporal.to_dict()
            # Parse the current temporal extent
            current_start = (
                exts["interval"][0][0]
                if exts["interval"][0][0] is not None
                else datetime.min
            )
            current_end = (
                exts["interval"][0][1]
                if exts["interval"][0][1] is not None
                else datetime.max
            )
            # Convert current_start and current_end to datetime objects
            current_start = datetime.fromisoformat(current_start)
            current_end = datetime.fromisoformat(current_end)
            # print({current_start}, {current_end})
            # Determine the new temporal extent based on the year provided
            updated_start_year = min(current_start.year, start.year)
            updated_end_year = max(current_end.year, end.year)
            # update start and end year
            updated_start = datetime(
                updated_start_year, current_start.month, current_start.day
            )
            updated_end = datetime(updated_end_year, current_end.month, current_end.day)
            # Update the temporal extent in the collection
            collection.extent.temporal = pystac.TemporalExtent(
                [updated_start, updated_end]
            )
            logger.info(
                f"Updated collection temporal extent: {updated_start}; {updated_end}"
            )

            # Update keywords
            # retrieve existing keywords
            key_col = collection.keywords
            # update keywords
            new_key = update_keywords(key_col, keywords, cat_keywords)
            # add to collection
            collection.keywords = new_key
            logger.info(f"updated and sorted keywords: {new_key}")

            # Update providers
            # Access providers in the collection and compare to the new provider
            ext_providers = collection.providers
            is_new_provider_unique = all(
                not providers_are_equal(provider, ext_provider)
                for ext_provider in ext_providers
            )
            # print(f"The new provider is unique: {is_new_provider_unique}")

            # If unique, add the new provider to the collection
            if is_new_provider_unique:
                collection.providers.append(provider)
                logger.info(f"New provider '{provider}' added to the collection.")
            else:
                logger.info(f"The provider '{provider}' already exists in the collection.")

            logger.info(f"collection {row_num} {title_collection} successfully updated")

        ## ITEMS ##
        # Create new item if not present yet
        if item["title_item"] not in [col.id for col in collection.get_items()]:
            # define item attributes that can deviate per item
            temporal_coverage = (
                f"{item['temporal_coverage']} ({item['temporal_interval']})"
                if np.nan_to_num(item["temporal_interval"])
                else f"{item['temporal_coverage']}"
            )
            scenarios = item["scenarios"] if np.nan_to_num(item["scenarios"]) else None
            analysis_type = (
                item["analysis_type"] if np.nan_to_num(item["analysis_type"]) else None
            )
            underlying_data = (
                item["underlying_data"]
                if np.nan_to_num(item["underlying_data"])
                else None
            )
            code = (
                f"{item['code_type']} (see Code link)"
                if np.nan_to_num(item["code_link"])
                else None
            )
            usage_notes = (
                item["usage_notes"] if np.nan_to_num(item["usage_notes"]) else None
            )
            data_format = item["data_format"] if np.nan_to_num(item["data_format"]) else "unknown"

            # condition for spatial resolution
            if np.nan_to_num(item["spatial_resolution_unit"]):
                if item["spatial_resolution"] == "administrative units":
                    spatial_resolution = f"{item['spatial_resolution']} ({item['spatial_resolution_unit']})"
                else:
                    spatial_resolution = f"{item['spatial_resolution']} {item['spatial_resolution_unit']}"
            else:
                spatial_resolution = f"{item['spatial_resolution']}"

            # condition for publication
            if str(item["publication_link"]).startswith("10."):
                publication = f"{item['publication_type']} (see DOI)"
            elif np.nan_to_num(item["publication_link"]):
                publication = f"{item['publication_type']} (see Publication link)"
            else:
                publication = None

            # create geometry from bbox_list
            footprint_polygon = Polygon([
                [bbox_list[0], bbox_list[1]],  # (min_lon, min_lat)
                [bbox_list[2], bbox_list[1]],  # (max_lon, min_lat)
                [bbox_list[2], bbox_list[3]],  # (max_lon, max_lat)
                [bbox_list[0], bbox_list[3]],  # (min_lon, max_lat)
                [bbox_list[0], bbox_list[1]]   # Close the polygon
                ])

            # Create basic item
            item_stac = pystac.Item(
                id=item["title_item"],
                geometry=mapping(footprint_polygon),
                bbox=bbox_list,
                datetime=None,  # datetime.now(),
                start_datetime=start,
                end_datetime=end,
                properties={
                    "title": item["title_item"],
                    "description": item["description_item"],
                    "risk data type": item["risk_data_type"],
                    "subcategory": item["subcategory"],
                    "spatial scale": item["spatial_scale"],
                    "reference period": item["reference_period"],
                    "temporal coverage": temporal_coverage,  # combination of resolution and interval
                    "scenarios": scenarios,
                    "data type": item["data_type"],
                    "data format": data_format,
                    "spatial resolution": spatial_resolution,  # combination of resolution and unit
                    "source type": item["source_type"],
                    "analysis type": analysis_type,
                    "underlying data": underlying_data,
                    "publication type": publication,
                    "code type": code,
                    "usage notes": usage_notes,
                },
                # extra_fields={ # are part of the json, but not shown in the browser
                #         'subcategory': str(item['subcategory']), #remove str() again once subcategory fixed
                #         'risk data type': item['risk_data_type']
                #     }
            )

            # add projection extension
            proj_ext = ProjectionExtension.ext(item_stac, add_if_missing=True)
            # Add projection properties
            proj_ext.epsg = int(item["coordinate_reference_system"])

            # Publication: Add scientific extension if DOI is present
            if str(item["publication_link"]).startswith("10."):
                logger.info("doi available")
                sci_ext = ScientificExtension.ext(item_stac, add_if_missing=True)
                sci_ext.doi = item["publication_link"]
            elif np.nan_to_num(item["publication_link"]):
                logger.info("weblink available")
                link = pystac.Link(
                    rel="cite-as",  # Relationship of the link
                    target=item["publication_link"],  # Target URL
                    title="Publication link",  # Optional title
                )
                item_stac.add_link(link)

            # Code: add link if available
            if code != None:
                logger.info("code available")
                if str(item["code_link"]).startswith("10."):
                    logger.info("doi available")
                    link = pystac.Link(
                        rel="cite-as",  # Relationship of the link
                        target=f"https://doi.org/{item['code_link']}",  # Target URL
                        title="Code link",  # Optional title
                    )
                else:
                    logger.info("weblink available")
                    link = pystac.Link(
                        rel="cite-as",  # Relationship of the link
                        target=item["code_link"],  # Target URL
                        title="Code link",  # Optional title
                    )
                item_stac.add_link(link)

            # ADD ASSETS
            # establish the number of assets
            asset_str = item["asset_links"]
            if np.nan_to_num(asset_str):
                logger.info("at least one asset provided; use asset link")
                assets = asset_str.split(" ") if " " in asset_str else [asset_str]
                roles = ["data"]
                # description = "data download"
            else:
                logger.info("no assets provided; use data overview link instead")
                assets = [item["data_overview_link"]]  # change here once asset link updated
                roles = ["overview"]
                # description = "overview page"

            # loop through all assets
            counter = 1
            for asset in assets:
                # Determine the media type based on the format attribute
                media_type = format_to_media_type.get(
                    data_format.lower(), "format unknown"
                )  # Default to None
                logger.info(f"media type defined as: {media_type}")
                # Define the asset
                asset_stac = pystac.Asset(
                    href=asset,
                    media_type=media_type,
                    roles=roles,
                    title=asset, #f"Data Link {counter}",
                    # description=description
                )
                # Add the asset to the item
                key = f"data-file_{counter}"
                item_stac.add_asset(key, asset_stac)
                counter += 1

            # Add item to collection
            collection.add_item(item_stac)

            # confirmation item added
            logger.info(f"item {row_num} {item['title_item']} successfully added")
        else:
            logger.warning(
                f"item {row_num} {item['title_item']} already present. "
                "Compare items and remove duplicates."
            )

    logger.info("catalog built")

    return catalog_main
