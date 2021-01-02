""" Tag resource for ActiveCampaign """

import typing
from django.http import Http404
from ..base_resource import Resource


class Tag(Resource):
    """A tag in ActiveCampaign. Allows to:
    - Create a tag
    - Find a tag by name
    - Udate a tag
    - Remove a tag

    Check docs in:
    https://developers.activecampaign.com/reference#tags
    """

    def __init__(
            self,
            tag: str,
            tag_type: str,
            description: typing.Optional[str] = '',
            **kwargs,
    ) -> None:
        """Initialize the tag.

        Args:
            tag: The name of the tag
            tag_type: The type of the tag. Either 'template' or 'contact'
            description: A description of the tag. Defaults to ''.
        """
        super().__init__(**kwargs)
        self.tag = tag
        self.tag_type = tag_type
        self.description = description

    @staticmethod
    def resource_name() -> str:
        """Get the resource name."""
        return 'tags'

    @staticmethod
    def map_field_name_to_attribute() -> dict:  # noqa: D102
        return {
            'tag': 'tag',
            'tagType': 'tag_type',
            'description': 'description',
        }

    @classmethod
    def find(cls: typing.Type, tag_name: str) -> 'Tag':
        """Get the first tag with the given name.

        Args:
            tag: The name of the tag to find

        Returns:
            The tag with the given name.
        """
        for tag in cls.filter({'search': tag_name}):
            return tag
        raise Http404

    def __repr__(self) -> str:
        """Generate internal representation."""
        return f'<Tag {self.tag}>'
