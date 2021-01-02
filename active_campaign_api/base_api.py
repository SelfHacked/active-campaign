""" Generic API class """

import enum
import typing
import requests


class AutoNameEnum(enum.Enum):
    """An Enum that automatically sets the member value equal to the name."""

    @staticmethod
    def _generate_next_value_(
            name: str,
            _start: int,
            _count: int,
            _last_values: typing.List,
    ) -> str:
        """Set the value of the member equal to it name.

        Args:
            name: The name of the member

        Returns:
            The value to set.
        """
        return name


@enum.unique
class HttpMethod(AutoNameEnum):
    """Basic HTTP methods."""

    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    DELETE = enum.auto()


class BaseAPI:
    """Base class for serving different APIs."""

    class Error(BaseException):
        """Generic error class."""

    def __init__(self, root_url: str) -> None:
        """Initialize requests session."""
        self.root_url = root_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })

    def _send_request(
            self, *,
            method: HttpMethod,
            path: str,
            data: typing.Union[str, bytes] = None,
            headers: typing.Dict[str, str] = None,
    ) -> requests.Response:
        """Send request function."""

        req = requests.Request(
            method=method.value,
            url=f'{self.root_url}{path}',
            headers=headers,
            data=data,
        )
        prepared_req = self.session.prepare_request(req)

        resp = self.session.send(prepared_req)
        resp.raise_for_status()
        return resp
