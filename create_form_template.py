"""Create a GitHub issue form template data submission"""

from climate_stac.data_model import HazardDataModel
from climate_stac.issue_form import IssueForm

if __name__ == '__main__':
    form = IssueForm(
        data_model=HazardDataModel,
        name="Data submission form (hazard data)",
        description="Suggest a new hazard dataset to be included in the living catalog",
        labels=["Hazard", "Enhancement"],
    )
    form.to_yaml(".github/ISSUE_TEMPLATE/data-submission-hazard.yaml")