"""Resource class for ActiveCampaign"""

import abc
import typing
from .active_campaign_api import ActiveCampaignAPI


class Resource(abc.ABC):
    """An ActiveCampaign API resource."""

    @staticmethod
    @abc.abstractmethod
    def resource_name() -> str:
        """Get resource name."""
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def map_field_name_to_attribute() -> dict:
        """Map between API field names and attribute names."""
        raise NotImplementedError()

    @classmethod
    def _to_api_payload(cls: typing.Type, data: dict) -> dict:
        """Convert a dict containing attribute: value to APIField: value.

        Args:
            data: The data to convert.

        Returns:
            A dict in the format the API will accept.
        """
        result = {}
        field_attribute_map = cls.map_field_name_to_attribute()

        for fieldname in field_attribute_map:
            for attribute in data:
                if field_attribute_map[fieldname] == attribute:
                    result[fieldname] = data[attribute]

        return result

    @classmethod
    def _to_attribute_dict(cls: typing.Type, data: dict) -> dict:
        """Convert API payload into attribute dict.

        Args:
            data: The dictionary containing the payload

        Returns:
            The converted dict.
        """
        field_attribute_map = {'id': '_id'}
        field_attribute_map.update(cls.map_field_name_to_attribute())

        return {
            field_attribute_map[fieldname]: value
            for fieldname, value in data.items()
            if field_attribute_map.get(fieldname) is not None
        }

    def __init__(self, **kwargs) -> None:
        """Initialize the Resource."""
        self._created = False  # whether the resource has been saved to remote.
        self._id = kwargs.pop('id', None) or kwargs.pop('_id', None)

    @property
    def id(self) -> typing.Optional[int]:  # noqa: A003
        """Get id of the resource."""
        return self._id

    @classmethod
    def filter(
        cls: typing.Type,
        filters: dict,
        parent_resource_id: typing.Optional[int] = None,
        parent_resource_name: typing.Optional[str] = None,
    ) -> typing.Generator:  # noqa: A003
        """Filter the list of resources with the given filters.

        Args:
            filters: dict
                key value pairs to filter by
            parent_resource_id: typing.Optional[int]
                The id of the parent recource
            parent_resource_name: typing.Optional[str]
                The name of the parent resource

        Yields:
            One recource at a time matching the filters.
        """
        # Default and most common usage
        resource_name = cls.resource_name()
        nested_resource_name = None

        if parent_resource_id and parent_resource_name:
            # We want to list nested_resource_name
            resource_name = parent_resource_name
            nested_resource_name = cls.resource_name()

        data_list = ActiveCampaignAPI().list_resources(
            resource_name=resource_name,
            resource_id=parent_resource_id,
            nested_resource_name=nested_resource_name,
            query_params=filters,
        )

        for data in data_list:
            resource_data = cls._to_attribute_dict(data)
            resource = cls(**resource_data)
            resource._created = True
            yield resource

    @classmethod
    def all(cls: typing.Type) -> typing.Generator:  # noqa: A003
        """Generate all the resources of this type.

        Yields:
            One recource at a time.
        """
        for resource in cls.filter({}):
            yield resource

    @classmethod
    def get_all_in(
        cls: typing.Type,
        parent_resource_name: str,
        parent_resource_id: int,
    ) -> typing.Generator:
        """Get all instances of this resource inside of the
        parent_resource_name with the given parent_resource_id.

        Args:
            parent_resource_name: str
                The name of the parent resource
            resource_id: int
                The id of the parent recource

        Yields:
            One recource at a time
        """
        for resource in cls.filter(
            {},
            parent_resource_id=parent_resource_id,
            parent_resource_name=parent_resource_name,
        ):
            yield resource

    @classmethod
    def get(cls: typing.Type, resource_id: typing.Optional[int]) -> 'Resource':
        """Get the recource with the given id.

        Args:
            resource_id: The id of the recource.

        Returns:
            An instance of the resource.
        """
        data = ActiveCampaignAPI().get_resource(
            cls.resource_name(),
            resource_id,
        )
        resource_data = cls._to_attribute_dict(data)
        resource = cls(**resource_data)
        resource._created = True
        return resource

    def delete(self) -> None:
        """Delete the resource from the server."""
        ActiveCampaignAPI().delete_resource(self.resource_name(), self.id)
        self._created = False

    def save(self) -> None:
        """Save the resource to the API server."""
        if not self._created:
            self._create()
        else:
            self._update()

    def serialize_data(self) -> dict:
        """Create an API payload from resource attributes.

        Returns:
            A dict containing the serialized data
        """
        field_attribute_map = self.map_field_name_to_attribute()
        return {
            fieldname: getattr(self, attribute)
            for fieldname, attribute in field_attribute_map.items()
        }

    def _create(self) -> None:
        """Create the resource."""
        data = self.serialize_data()
        self._id = ActiveCampaignAPI().create_resource(
            self.resource_name(), data=data,
        )['id']
        self._created = True

    def _update(self) -> None:
        """Update the resource."""
        data = self.serialize_data()
        ActiveCampaignAPI().update_resource(
            self.resource_name(),
            resource_id=self.id,
            data=data,
        )
