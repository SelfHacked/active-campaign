
""" something """

import typing
from .active-campaign-resources import Resource


class ContactTag(Resource):
    """Tag for a contact."""

    def __init__(
            self,
            tag: Optional[int],
            contact: Optional[int],
            **kwargs: typing.Dict,
    ) -> None:
        """Initialize the contact tag.

        Args:
            tag: The id of the tag.
            contact: The id of the contact.
        """
        super().__init__(**kwargs)
        self.tag = tag
        self.contact = contact

    @staticmethod
    def resource_name() -> str:
        """Get the name of the API resource.

        Returns:
            The name of the resource
        """
        return 'contactTags'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Map field names to attributes."""
        return {
            'tag': 'tag',
            'contact': 'contact',
        }
