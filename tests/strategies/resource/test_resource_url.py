"""Test the resource strategy for resource/url."""

from __future__ import annotations


def test_resource_url() -> None:
    """Test `resource/url` resource strategy."""
    from oteapi.models.genericconfig import AttrDict
    from oteapi.strategies.resource.resource_url import ResourceURLStrategy

    config = {
        "resourceType": "resource/url",
        "downloadUrl": "https://example.org/sample.json",
        "mediaType": "application/json",
    }
    strategy = ResourceURLStrategy(resource_config=config)

    assert strategy.initialize() == AttrDict()
    assert strategy.get() == AttrDict(
        downloadUrl="https://example.org/sample.json", mediaType="application/json"
    )
