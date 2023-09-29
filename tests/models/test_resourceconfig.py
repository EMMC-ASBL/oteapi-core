"""Tests for `oteapi.models.resourceconfig`"""
import pytest


def test_ensure_unique_url_pairs() -> None:
    """Test the root validator `ensure_unique_url_pairs` for `ResourceConfig`."""
    from pydantic import ValidationError

    from oteapi.models.resourceconfig import ResourceConfig

    valid_parameters = {
        "downloadUrl": "http://example.org",
        "mediaType": "text/html",
        "accessUrl": "http://service.example.org",
        "accessService": "example-service",
    }
    valid_combinations = [
        ["downloadUrl", "mediaType"],
        ["accessUrl", "accessService"],
        ["downloadUrl", "mediaType", "accessUrl"],
        ["downloadUrl", "mediaType", "accessService"],
        ["downloadUrl", "mediaType", "accessUrl", "accessService"],
        ["accessUrl", "accessService", "downloadUrl"],
        ["accessUrl", "accessService", "mediaType"],
    ]
    invalid_combinations = [
        ["downloadUrl"],
        ["mediaType"],
        ["accessUrl"],
        ["accessService"],
        ["downloadUrl", "accessUrl"],
        ["downloadUrl", "accessService"],
        ["mediaType", "accessUrl"],
        ["mediaType", "accessService"],
    ]

    for combination in valid_combinations:
        try:
            ResourceConfig(
                **{
                    key: value
                    for key, value in valid_parameters.items()
                    if key in combination
                }
            )
        except ValidationError as exc:
            pytest.fail(f"Combination:\n{combination}.\n\nException:\n{exc}")
    for combination in invalid_combinations:
        with pytest.raises(ValidationError, match=r"Either of the pairs.*"):
            ResourceConfig(
                **{
                    key: value
                    for key, value in valid_parameters.items()
                    if key in combination
                }
            )
