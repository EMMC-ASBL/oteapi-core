"""General tests for `oteapi.strategies`."""

from __future__ import annotations


def test_registered_entry_point_importability():
    """Ensure all registered entry points (strategies) can be imported."""
    from oteapi.plugins.factories import StrategyFactory

    package_name = "oteapi"

    for entry_points in StrategyFactory.strategy_create_func.values():
        for entry_point in entry_points:
            if entry_point.package != package_name:
                continue
            assert entry_point.implementation
