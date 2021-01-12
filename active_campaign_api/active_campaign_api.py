"""Contains ActiceCampaignAPI class"""

import json
import urllib
import typing

from django.conf import settings
from .base_api import BaseAPI, HttpMethod


def require_setting(name: str) -> typing.Any:
    """Check for setting attribute, rise error is does not exist."""

    value = getattr(settings, name)

    if not value:
        raise RuntimeError(
            f'{name} django setting is not set properly, '
            f'current value: "{value}".',
        )

    return value


class ActiveCampaignAPI(BaseAPI):
    """Handle marketing campaign tools."""

    def __init__(self) -> None:
        """Initialize active campaign."""
        MARKETING_CAMPAIGN_KEY = require_setting('MARKETING_CAMPAIGN_KEY')
        MARKETING_CAMPAIGN_URL = require_setting('MARKETING_CAMPAIGN_URL')

        super().__init__(MARKETING_CAMPAIGN_URL)
        self.session.headers.update({
            'Api-Token': MARKETING_CAMPAIGN_KEY,
        })

    # A mapping (from name to id) for lists in ActiveCampaign
    LISTS = {
        'SD: Marketing List': 43,
    }

    def list_resources(
            self,
            resource_name: str,
            resource_id: typing.Optional[int] = None,
            nested_resource_name: typing.Optional[str] = None,
            query_params: typing.Optional[dict] = None,
    ) -> typing.Generator[dict, None, typing.List[dict]]:
        """
        List all the recources of the given name.
        If resource_id and nested_resource_name are passed,
        it lists all the nested_resources of the given name,
        that belong to the resource_name with given resource_id

        Args:
            resource_name: str
                The name of the resource to fetch
            resource_id: typing.Optional[int]
                The id of the resource
            nested_resource_name: typing.Optional[str]
                The name of the nested resource to fetch
            query_params: typing.Optional[dict]
                the key value pairs for the query params.

        Yields:
            A single resource from the server.
        """
        offset = 0
        limit = 100
        total = 0
        query_params = query_params or {}

        while offset <= total:
            query_params.update({'limit': limit, 'offset': offset})
            path = self._prepare_path(
                resource_name,
                resource_id=resource_id,
                nested_resource_name=nested_resource_name,
                query_params=query_params
            )

            response = self._send_request(method=HttpMethod.GET, path=path)
            response.raise_for_status()

            for resource_data in response.json()[resource_name]:
                yield resource_data

            total = int(response.json()['meta']['total'])
            offset += limit

        return response.json()[resource_name]

    def get_resource(
            self,
            resource_name: str,
            resource_id: typing.Optional[int],
    ) -> dict:
        """Get details of the given resource.

        Args:
            resource_name: Name of the resource.
            resource_id: The id of the object.

        Returns:
            The given resource.
        """
        path = self._prepare_path(resource_name, resource_id)
        response = self._send_request(method=HttpMethod.GET, path=path)
        response.raise_for_status()
        return response.json()[resource_name[:-1]]

    def create_resource(self, resource_name: str, data: dict) -> dict:
        """Create a resource with the given data.

        Args:
            resource_name: The name of the resource
            data: The data to create the resource with.

        Returns:
            The newly created resource.
        """
        path = self._prepare_path(resource_name)
        payload = {
            resource_name[:-1]: data,
        }

        resp = self._send_request(
            method=HttpMethod.POST,
            path=path,
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()[resource_name[:-1]]

    def update_resource(
            self,
            resource_name: str,
            resource_id: typing.Optional[int],
            data: dict,
    ) -> dict:
        """Update the given resource with the given data.

        Args:
            resource_name: The name of the recource to update
            resource_id: The id of the resource.
            data: The data to update the resource with.

        Returns:
            The update data.
        """
        path = self._prepare_path(resource_name, resource_id)
        payload = {
            resource_name[:-1]: data,
        }

        resp = self._send_request(
            method=HttpMethod.PUT,
            path=path,
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()[resource_name[:-1]]

    def delete_resource(self, resource_name: str,
                        resource_id: typing.Optional[int]) -> None:
        """Delete the given resource.

        Args:
            resource_name: Name of the resource.
            resource_id: The id of the object.
        """
        path = self._prepare_path(resource_name, resource_id)
        response = self._send_request(method=HttpMethod.DELETE, path=path)
        response.raise_for_status()

    @classmethod
    def _get_query_string(
        cls: typing.Type,
        query_params: typing.Optional[dict] = None,
    ) -> str:
        """Get the url string representation of query_params
        Args:
            query_params: dict
                the key value pairs for the query params.
        Returns:
            query_string: str
                url string representation of query_params
        """
        query_string = '?'
        query_params = query_params or {}

        for key, value in query_params.items():
            value = urllib.parse.quote(str(value))
            key = urllib.parse.quote(str(key))
            query_string = f'{query_string}{key}={value}&'

        # query_string[:-1] to remove the last '&'
        query_string = query_string[:-1]
        return query_string

    @classmethod
    def _prepare_path(
        cls: typing.Type,
        resource_name: str,
        resource_id: typing.Optional[int] = None,
        nested_resource_name: typing.Optional[str] = None,
        query_params: typing.Optional[dict] = None,
    ) -> str:
        """Prepare the url path.

        Args:
            resource_name: The resource being accessed
            resource_id: The id of the resource. Defaults to None.
            query_params: the key value pairs for the query params.

        Returns:
            The request path.
        """
        query_string = cls._get_query_string(
            query_params=query_params
        )
        path = f'/{resource_name}'

        if resource_id is not None:
            path = f'{path}/{resource_id}'
            if nested_resource_name is not None:
                path = f'{path}/{nested_resource_name}'

        path = f'{path}{query_string}'

        return path
