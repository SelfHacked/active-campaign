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
        raise RuntimeError(f"{name} django setting is not set properly")
    return value


def singular_form(resource_name: str) -> str:
    """Gets the singular form of the resource_name,
    that is, removing the s at the end of it"""
    if resource_name[-1] == "s":
        return resource_name[:-1]
    else:
        return resource_name


class ActiveCampaignAPI(BaseAPI):
    """Handle marketing campaign tools."""

    def __init__(self) -> None:
        """Initialize active campaign."""
        MARKETING_CAMPAIGN_KEY = require_setting("MARKETING_CAMPAIGN_KEY")
        MARKETING_CAMPAIGN_URL = require_setting("MARKETING_CAMPAIGN_URL")
        MARKETING_CAMPAIGN_REQUEST_TIMEOUT = getattr(
            settings,
            "MARKETING_CAMPAIGN_REQUEST_TIMEOUT",
            None,
        )

        super().__init__(MARKETING_CAMPAIGN_URL, MARKETING_CAMPAIGN_REQUEST_TIMEOUT)
        self.session.headers.update({"Api-Token": MARKETING_CAMPAIGN_KEY})

    # A mapping (from name to id) for lists in ActiveCampaign
    LISTS = {
        "SD: Marketing List": 43,
    }

    def list_resources(
        self,
        resource_name: str,
        resource_id: typing.Optional[int] = None,
        nested_resource_name: typing.Optional[str] = None,
        query_params: typing.Optional[dict] = None,
    ) -> typing.Generator[dict, None, None]:
        """List all the recources of the given name.
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
        # limit = 100 is the maximum amount allowed in ActiveCampaign
        # API v3. If you make a request with limit=1000 as query param,
        # you will get back only 100 results
        limit = 100
        total = 0
        query_params = query_params or {}

        resource_key_in_response = resource_name
        if resource_id and nested_resource_name:
            # We want the list of nested_resource_name
            resource_key_in_response = nested_resource_name

        while offset <= total:
            query_params.update({"limit": limit, "offset": offset})
            path = self._prepare_path(
                resource_name,
                resource_id=resource_id,
                nested_resource_name=nested_resource_name,
                query_params=query_params,
            )

            response = self._send_request(method=HttpMethod.GET, path=path)
            response.raise_for_status()

            for resource_data in response.json()[resource_key_in_response]:
                yield resource_data

            # In here we are getting the actual total of results
            # Not too clean because we are getting the same value
            # over and over again, but we haven't found a cleaner way
            try:
                total = int(response.json()["meta"]["total"])
                offset += limit
            except KeyError:
                # On requests of the form 'contacts/:id/contactTag/
                # there is not 'meta' nor 'total' attributes on the response
                return

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
        return response.json()[singular_form(resource_name)]

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
            singular_form(resource_name): data,
        }

        resp = self._send_request(
            method=HttpMethod.POST,
            path=path,
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()[singular_form(resource_name)]

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
            singular_form(resource_name): data,
        }

        resp = self._send_request(
            method=HttpMethod.PUT,
            path=path,
            data=json.dumps(payload),
        )
        resp.raise_for_status()
        return resp.json()[singular_form(resource_name)]

    def delete_resource(
        self, resource_name: str, resource_id: typing.Optional[int]
    ) -> None:
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

        if not query_params:
            query_string = ""
        else:
            query_string = "?"
            query_params = query_params or {}

            for key, value in query_params.items():
                value = urllib.parse.quote(str(value))
                key = urllib.parse.quote(str(key))
                query_string = f"{query_string}{key}={value}&"

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
        query_string = cls._get_query_string(query_params=query_params)
        path = f"/{resource_name}"

        if resource_id is not None:
            path = f"{path}/{resource_id}"
            if nested_resource_name is not None:
                path = f"{path}/{nested_resource_name}"

        path = f"{path}{query_string}"

        return path
