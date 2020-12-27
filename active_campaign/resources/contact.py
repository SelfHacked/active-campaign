""" Contact resource for ActiveCampaign """

import typing
from django.http import Http404
from ..utils.resource import Resource


class Contact(Resource):
    """
    An ActiveCampaign contact. Allows to:
     - Create a contact
     - Update a contact
     - Delete a contact

    Check docs in:
    https://developers.activecampaign.com/reference#contact
    """

    def __init__(self, email: str, **kwargs: typing.Dict) -> None:
        """Initialize contact."""
        super().__init__(**kwargs)
        self.email = email

    @staticmethod
    def resource_name() -> str:
        """Get the name of the API resource.

        Returns:
            The name of the resource
        """
        return 'contacts'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Map field names to attributes."""
        return {
            'email': 'email',
        }

    @classmethod
    def find(cls: typing.Type, email: str) -> 'Contact':
        """Find contact by email."""
        for contact in cls.filter({'email': email}):
            return contact
        raise Http404
