"""List resource for ActiveCampaign"""

import typing
from django.http import Http404
from ..base_resource import Resource


class List(Resource):
    """
    An ActiveCampaign list. Allows to:
     - Find a list by name
     - Delete a list

    Check docs in:
    https://developers.activecampaign.com/reference#lists
    """

    def __init__(self, name: str, **kwargs: typing.Dict) -> None:
        """Initialize list."""
        super().__init__(**kwargs)
        self.name = name

    @staticmethod
    def resource_name() -> str:
        """Get the name of the API resource.

        Returns:
            The name of the resource
        """
        return 'lists'

    @staticmethod
    def map_field_name_to_attribute() -> typing.Dict:
        """Map field names to attributes."""
        return {
            'name': 'name',
        }

    @classmethod
    def find(cls: typing.Type, name: str) -> 'List':
        """Find list by name."""
        for active_campaign_list in cls.filter({'name': name}):
            return active_campaign_list
        raise Http404

    def save(self) -> None:
        raise NotImplementedError
