""" something """

import typing
from django.http import Http404
from ..utils.resource import Resource


class MarketingList(Resource):
    """An ActiveCampaign contact list."""

    def __init__(
            self,
            name: str,
            stringid: str,
            sender_url: str,
            sender_reminder: str,
            **kwargs: typing.Dict,
    ) -> None:
        """Initialize the marketing list.

        Args:
            name: Name of the list to create

            stringid: URL-safe list name. Example: 'list-name-sample'

            sender_url: The website URL this list is for.

            sender_reminder: A reminder for your contacts as to why
            they are on this list and you are messaging them.
        """
        super().__init__(**kwargs)
        self.name = name
        self.stringid = stringid
        self.sender_url = sender_url
        self.sender_reminder = sender_reminder

    @staticmethod
    def resource_name() -> str:
        """Get the resource name."""
        return 'lists'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Serialize the list."""
        return {
            'name': 'name',
            'stringid': 'stringid',
            'sender_url': 'sender_url',
            'sender_reminder': 'sender_reminder',
        }

    @classmethod
    def find(cls: typing.Type, name: str) -> 'MarketingList':
        """Get the list first list with the given name.

        Args:
            name: The name of the list to find

        Returns:
            The list with the given name.
        """
        for lst in cls.filter({'filters[name]': name}):
            return lst
        raise Http404

    def __repr__(self) -> str:
        """Generate internal representation."""
        return f"<List '{self.name}'>"
