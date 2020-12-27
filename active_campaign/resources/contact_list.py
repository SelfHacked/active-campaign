""" ContactList resource for ActiveCampaign """

import typing
from ..base_resource import Resource


class ContactList(Resource):
    """
    List contact pair in ActiveCampaign. Allows to:
     - Subscribe a contact to a list
     - Unsubscribe a contact from a list.

    Check docs in:
    https://developers.activecampaign.com/reference#update-list-status-for-contact
    """

    def __init__(
            self,
            list_id: typing.Optional[int],
            contact_id: typing.Optional[int],
            status: typing.Optional[int],
            **kwargs: typing.Dict,
    ) -> None:
        """Initialize the contact list.

        Args:
            list_id: The id of the list.
            contact_id: The id of the contact.
            status: 1 to subscribe the contact and 2 to unsubscribe.
        """
        super().__init__(**kwargs)
        self.list_id = list_id
        self.contact_id = contact_id
        self.status = status

    @staticmethod
    def resource_name() -> str:
        """Get the name of the API resource.

        Returns:
            The name of the resource
        """
        return 'contactLists'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Map field names to attributes."""
        return {
            'list': 'list_id',
            'contact': 'contact_id',
            'status': 'status',
        }
