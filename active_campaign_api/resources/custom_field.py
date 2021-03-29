"""CustomField resource for Active Campaign """

import typing
from django.http import Http404
from ..base_resource import Resource


class CustomField(Resource):
    """An ActiveCampaign CustomField. Allows to:
     - Create a CustomField
     - Find a CustomField by the title
     - Delete a CustomField
    """

    def __init__(
            self,
            title: str,
            field_type: str,
            **kwargs: typing.Dict,
    ) -> None:
        """Initialize the CustomField.

        Args:
            title: str
                Title of the CustomField being created

            field_type: str
                Possible Values: dropdown, hidden, checkbox, date,
                text, datetime, textarea, NULL, listbox, radio
        """
        super().__init__(**kwargs)
        self.title = title
        self.type = field_type

    @staticmethod
    def resource_name() -> str:
        """Get the resource name."""
        return 'fields'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Serialize the field."""
        return {
            'title': 'title',
            'type': 'type',
        }

    @classmethod
    def find(cls, field_title: str) -> 'CustomField':
        """Get the CustomField with the given title.

        Args:
            field_title: str
                The title of the CustomField to find

        Returns:
            The CustomField with the given titles.
        """
        for custom_field in cls.all():
            if custom_field.title == field_title:
                return custom_field
        raise Http404

    def __repr__(self) -> str:
        """Generate internal representation."""
        return f"<CustomField '{self.title}'>"
