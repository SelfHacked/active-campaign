"""ContactTag resource for ActiveCampaign"""

import typing
from ..base_resource import Resource


class ContactTag(Resource):
    """
    Tag for a contact in ActiveCampaign. Allows to:
     - Add a tag to contact
     - Remove a tag from a contact.

    Check docs in:
    https://developers.activecampaign.com/reference#contact-tags
    """

    def __init__(
        self,
        tag: typing.Optional[int],
        contact: typing.Optional[int],
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

    @classmethod
    def all_in_contact(cls, contact_id: int):
        """Get all ContactTags associated to contact with that id"""
        for contact_tag in cls.get_all_in("contacts", contact_id):
            yield contact_tag
