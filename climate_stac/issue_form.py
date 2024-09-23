from pathlib import Path
from typing import TYPE_CHECKING, cast
import yaml

if TYPE_CHECKING:
    from climate_stac.data_model import CommonDataModel


class IssueForm(object):
    def __init__(
        self,
        data_model: "CommonDataModel",
        name: str,
        description: str,
        labels: list[str],
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.labels: list[str] = labels
        self.body: list[dict] = []

        # Extract fields from data model
        model_schema: dict[str, dict] = data_model.model_json_schema()
        field_schema: dict[str, dict] = model_schema["properties"]
        required: list = model_schema["required"]
        for id, schema in field_schema.items():
            ftype = schema["form-type"]
            field = {
                "type": ftype,
                "id": id,
                "attributes": {
                    "label": schema["label"],
                    "description": schema["description"],
                },
            }
            if ftype == "dropdown":
                field["attributes"]["options"] = schema["enum"]
            elif "placeholder" in schema:
                field["attributes"]["placeholder"] = schema["placeholder"]
            if id in required:
                field["validations"] = {"required": True}
            # Add field to body
            self.body.append(field)

    @property
    def json(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "labels": self.labels,
            "body": self.body,
        }

    def to_yaml(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            yaml.safe_dump(
                self.json, f, sort_keys=False, default_flow_style=False, indent=2
            )
