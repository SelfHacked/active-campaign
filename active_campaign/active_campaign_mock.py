"""Mocks for the Active Campaign api calls."""

import re
import json
import typing
import pytest
import requests

from pathlib import PurePosixPath
from urllib.parse import urlparse, parse_qs, unquote
from .active_campaign_api import ActiveCampaignAPI


@pytest.fixture()
def mock_active_campaign(requests_mock) -> typing.Callable:  # noqa
    """Mock ActiveCampaign api calls.

    Currently only api calls used by patient app.
    Documentation: https://developers.activecampaign.com/reference
    """
    def _mock_active_campaign() -> None:  # noqa
        root_url = 'https://selfhacked.api-us1.com/api/3'

        def req_json_value(
                req: requests.PreparedRequest,
                value: str) -> str:
            """Return value from request json body.

            Args:
                req: Request object
                value: Key of the value to be returned,
                        using dot syntax for levels
            """
            key_list = value.split('.')
            if not req.body:
                return ''
            result = json.loads(req.body)
            for key in key_list:
                result = result[key]
            return result

        def extract_url_segment(url: str, place: int = -1) -> str:
            """Return a segment from a given url.

            Args:
                url: url string to be parsed
                place: place of the segment to be returned, defaults to -1
            """
            segments = PurePosixPath(unquote(urlparse(url).path)).parts
            return str(segments[place])

        def construct_url_path_param(resource_name: str) -> typing.Pattern:
            """Construct url with id path_param."""
            escaped_root = re.escape(root_url)
            id_segment = r'[\d\w-]+'
            path_re = escaped_root
            path_re += r'\/' + resource_name + r'\/'
            path_re += id_segment
            return re.compile(path_re)

        def write_contact_callback(request: requests.PreparedRequest,
                                   context: typing.Callable) -> dict:
            if(request.method == 'PUT' and request.url):
                contact_id = extract_url_segment(request.url)
            else:
                contact_id = '1'
            recieved_email = req_json_value(request, 'contact.email')
            return {'contact': {
                    'email': recieved_email,
                    'id': contact_id}}

        requests_mock.post(
            f'{root_url}/contacts',
            json=write_contact_callback,
            status_code=201)

        requests_mock.put(
            construct_url_path_param('contacts'),
            json=write_contact_callback,
            status_code=200)

        def find_tag_callback(request: requests.PreparedRequest,
                              context: typing.Callable) -> dict:
            parsed_url = urlparse(request.url)
            query_dict = parse_qs(parsed_url.query) \
                if isinstance(parsed_url.query, str) else {}
            search_query = (query_dict['search'][0]
                            if 'search' in query_dict
                            else 'example tag')
            return {'tags': [
                    {'tagType': 'contact',
                     'tag': search_query,
                     'description': ''},
                    ],
                    'meta': {'total': 1},
                    }

        # without query params so as to match everything
        requests_mock.get(
            f'{root_url}/tags',
            json=find_tag_callback)

        def find_list_callback(request: requests.PreparedRequest,
                               context: typing.Callable) -> dict:
            parsed_url = urlparse(request.url)
            query_dict = parse_qs(parsed_url.query) \
                if isinstance(parsed_url.query, str) else {}
            name_query = (query_dict['filters[name]'][0]
                          if 'filters[name]' in query_dict
                          else 'example list')
            list_id = (ActiveCampaignAPI.LISTS[name_query]
                       if name_query in ActiveCampaignAPI.LISTS
                       else 1)
            return {'lists': [
                    {'string': 'contact',
                     'name': name_query,
                     'stringid': name_query.replace(' ', '-').lower(),
                     'sender_url': 'http://example.com/',
                     'sender_reminder': 'You signed up for my mailing list.',
                     'id': list_id}],
                    'meta': {'total': 1}}

        # without query params so as to match everything
        requests_mock.get(
            f'{root_url}/lists',
            json=find_list_callback)

        def update_contact_list(request: requests.PreparedRequest,
                                context: typing.Callable) -> dict:
            list_id = req_json_value(request, 'contactList.list')
            contact_id = req_json_value(request, 'contactList.contact')
            status = req_json_value(request, 'contactList.status')
            return {
                'contacts': [{
                    'id': contact_id
                }],
                'contactList': {
                    'contact': contact_id,
                    'list': list_id,
                    'id': list_id,
                    'status': status
                }
            }

        requests_mock.post(
            f'{root_url}/contactLists',
            json=update_contact_list)

        def create_contact_tag_callback(request: requests.PreparedRequest,
                                        context: typing.Callable) -> dict:
            contact_id = req_json_value(request, 'contactTag.contact')
            tag_id = req_json_value(request, 'contactTag.tag')
            return {
                'contactTag': {
                    'id': 1,
                    'contact': contact_id,
                    'tag': tag_id
                }
            }

        requests_mock.post(
            f'{root_url}/contactTags',
            json=create_contact_tag_callback,
            status_code=201)

    return _mock_active_campaign
