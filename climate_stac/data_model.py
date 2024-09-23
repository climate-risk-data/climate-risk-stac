import json
from pathlib import Path
from typing import Any, List, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


__all__ = ["HazardDataModel"]

HAZARDS = {
    "flood": [
        "coastal flood",
        "river flood",
        "flash flood",
        "urban flood",
        "pluvial flood",
        "not specified",
    ],
    "precipitation-related": ["drought"],
    "temperature-related": ["heatwave", "coldwave"],
    "wind-related": [
        "tropical cyclone",
        "extratropical cyclone",
        "tornado",
        "windstorm",
    ],
    "environmental": ["landslide", "wildfire"],
    "multi-hazard": ["multi-hazard"],
}

# Derived values
HAZARD_CATEGORIES = tuple(HAZARDS.keys())
HAZARD_SUBCATEGORIES = tuple(
    set([subcat for cat in HAZARDS.values() for subcat in cat])
)


class CommonDataModel(BaseModel):
    catalog: Literal["hazard", "exposure-vulnerability"]

    risk_data_type: Literal["hazard", "exposure", "vulnerability", "response"]

    category: str

    subcategory: str

    title_collection: str = Field(
        json_schema_extra={
            "label": "Collection title",
            "description": "Name of the dataset collection; the collection title must be the same for each item belonging to that collection (see 'Item title' for further instructions).",
            "placeholder": "e.g. CMIP6 heat stress indicators",
            "form-type": "input",
        }
    )

    title_collection_short: str | None = Field(
        default=None,
        optional=True,
        json_schema_extra={
            "label": "Short collection title",
            "description": "Short name/acronym of the dataset (if available)",
            "placeholder": "e.g. CMIP6-HIS",
            "form-type": "input",
        },
    )

    description_collection: str = Field(
        json_schema_extra={
            "label": "Collection description",
            "description": "Detailed description of the dataset collection; the collection description must be the same for each item belonging to that collection",
            "placeholder": "e.g. The indices are provided for historical and future climate projections (SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5) included in the Coupled Model Intercomparison Project Phase 6 (CMIP6) and used in the 6th Assessment Report of the Intergovernmental Panel on Climate Change (IPCC).",
            "form-type": "textarea",
        }
    )

    title_item: str = Field(
        json_schema_extra={
            "label": "Item title",
            "description": "Concise name of the dataset item; each item from the same collection needs to have a unique name. If data are from the same overall data source, but metadata attributes differ, these are separate items that belong to the same collection. Please submit separate data items per collection by creating a new issue.",
            "placeholder": "e.g. CMIP6 heat stress indicators for historical period (1850-2014)",
            "form-type": "input",
        }
    )

    description_item: str = Field(
        json_schema_extra={
            "label": "Item description",
            "description": "Detailed description of the dataset item; if there is only one item in the collection, the collection description can be copied here.",
            "placeholder": "e.g. Heat index is a heat stress indicator used by the US National Oceanic and Atmospheric Administration (NOAA) National Weather Service for issuing heat warnings. It is calculated using multiple linear regression based on daily maximum temperature and relative humidity (calculated from daily mean specific humidity and surface pressure).",
            "form-type": "textarea",
        }
    )

    spatial_scale: Literal["(near-)global", "regional", "national", "subnational"] = Field(
        json_schema_extra={
            "label": "Spatial scale",
            "description": "Spatial coverage of the dataset",
            "form-type": "dropdown",
        }
    )

    bbox: list[float] = Field(
        json_schema_extra={
            "label": "Bounding box",
            "description": "Bounding box of the dataset in the format [west, south, east, north]",
            "placeholder": "e.g. [-180, -90, 180, 90]",
            "form-type": "input",
        }
    )

    reference_period: Literal["historical", "future", "historical & future"] = Field(
        json_schema_extra={
            "label": "Reference period",
            "description": "Reference period for which the data are available",
            "form-type": "dropdown",
        }
    )

    temporal_coverage: str = Field(
        json_schema_extra={
            "label": "Temporal coverage",
            "description": "Temporal coverage of the dataset format YYYY, YYYY-YYYY or YYYY-now (if data are updated in real time)",
            "placeholder": "e.g. 1850-2014",
            "form-type": "input",
        }
    )

    temporal_resolution: str | None = Field(
        default=None,
        optional=True,
        json_schema_extra={
            "label": "Temporal resolution",
            "description": "Temporal resolution of the dataset",
            "placeholder": "e.g. hourly, monthly, yearly, x-hourly, etc.",
            "form-type": "input",
        }
    )

    scenario: str | None = Field(
        default=None,
        optional=True,
        json_schema_extra={
            "label": "Scenario",
            "description": "Name of the scenarios used if 'Reference period' is 'future'",
            "form-type": "dropdown",
            "enum": ["RCPs", "SSP-RCP combinations", "warming levels", "extrapolation", "other (please specify below)"]
        },
    )

    custom_scenario: str | None = Field(
        default=None,
        optional=True,
        json_schema_extra={
            "label": "Custom scenario",
            "description": "Name of the custom scenario used if 'Scenario' is 'other'",
            "form-type": "input",
        },
    )


    @field_validator("bbox", mode="before")
    @classmethod
    def validate_bbox(cls, value: Any) -> list[float]:
        if isinstance(value, str):
            value = [float(coord.strip()) for coord in value.strip('[]').split(",")]
        if not isinstance(value, list) or len(value) != 4:
            raise ValueError("Bounding box must be list with 4 values")
        return value

    @model_validator(mode="before")
    @classmethod
    def _preprocess(cls, data: Any) -> dict:
        if isinstance(data, dict):
            # Rename label to field name
            field_schema = cls.model_json_schema()["properties"]
            rename = {item["label"]: name for name, item in field_schema.items()}
            data = {rename.get(k, k): v for k, v in data.items()}
        return data
    
    @model_validator(mode="after")
    def _postprocess(self) -> None:
        # set custom scenario if scenario is 'other'
        if self.scenario == "other": 
            if not self.custom_scenario:
                raise ValueError("Custom scenario must be provided if 'Scenario' is 'other'")
            self.scenario = self.custom_scenario

    @property
    def id(self) -> str:
        if self.title_collection_short:
            collection = self.title_collection_short.replace(" ", "_").lower()
        else:
            collection = self.title_collection.replace(" ", "_").lower()
        item = self.title_item.replace(" ", "_").lower()
        return f"{collection}-{item}"

    @property
    def collection_title(self) -> str:
        title = self.title_collection
        if self.title_collection_short:
            title += f" ({self.title_collection_short})"
        return title

    @property
    def json_path(self) -> str:
        return f"{self.catalog}/{self.category}/{self.id}.json"

    def to_json(
        self, path: str | Path, indent=4, exclude_none=True, round_trip=True, **kwargs
    ) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json = self.model_dump_json(
                indent=indent,
                exclude_none=exclude_none,
                round_trip=round_trip,
                **kwargs,
            )
            f.write(json)


class HazardDataModel(CommonDataModel):
    catalog: Literal["hazard"] = Field(
        json_schema_extra={
            "label": "Catalog",
            "description": "Overarching catalog that the data belong to (i.e. hazard, exposure-vulnerability)",
            "form-type": "dropdown",
        }
    )

    category: Literal[HAZARD_CATEGORIES] = Field(  # type: ignore
        json_schema_extra={
            "label": "Category",
            "description": "Category of data type according to classification scheme (see readme)",
            "form-type": "dropdown",
        }
    )

    subcategory: Literal[HAZARD_SUBCATEGORIES] = Field(  # type: ignore
        json_schema_extra={
            "label": "Subcategory",
            "description": "Subcategory of data type according to classification scheme (see readme)",
            "form-type": "dropdown",
        }
    )

    risk_data_type: Literal["hazard"] = Field(
        json_schema_extra={
            "label": "Risk data type",
            "description": "Risk driver (i.e. hazard, exposure, vulnerability, response)",
            "form-type": "dropdown",
        }
    )


if __name__ == "__main__":
    data = {
        "catalog": "hazard",
        "category": "flood",
        "subcategory": "coastal flood",
        "risk_data_type": "hazard",
        "title_collection": "CMIP6 heat stress indicators",
    }

    hazard = HazardDataModel(**data)
    print(hazard)
    # > catalog='hazard' category='flood' subcategory='coastal flood'

    model_schema = HazardDataModel.model_json_schema()
    print(json.dumps(model_schema, indent=2))
