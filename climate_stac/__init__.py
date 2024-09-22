"""Small library to maintain a STAC climate risk data catalog."""

from climate_stac.climate_stac import create_catalog, update_catalog_from_dataframe

__all__ = ["create_catalog", "update_catalog_from_dataframe"]
