"""FieldValue resource for Active Campaign """

import typing
from ..base_resource import Resource


class CustomFieldValue(Resource):
    """An ActiveCampaign CustomFieldValue."""

    def __init__(
            self,
            contact_id: str,
            custom_field_id: str,
            value,
            **kwargs: typing.Dict,
    ) -> None:
        """Initialize the CustomFieldValue.

        Args:
            contact_id: int
                ID of the contact whose field value you're updating

            custom_field_id: int
                ID of the custom field whose value you're updating for the contact

            value: str
                Value for the field that you're updating. For multi-select options
                this needs to be in the format of ||option1||option2||
        """
        super().__init__(**kwargs)
        self.contact_id = contact_id
        self.field_id = custom_field_id
        self.value = value

    @staticmethod
    def resource_name() -> str:
        """Get the resource name."""
        return 'fieldValues '

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Serialize the CustomFieldValue."""
        return {
            'contact': 'contact_id',
            'field': 'field_id',
            'value': 'value'
        }
