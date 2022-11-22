"""Test mapping strategy."""
# pylint: disable=invalid-name


def test_mapping() -> None:
    """Test mapping strategy."""
    from oteapi.models import MappingConfig
    from oteapi.strategies.mapping.mapping import MappingStrategy

    conf1 = MappingConfig(
        mappingType="triples",
        triples=[
            ("http://onto-ns.com/meta/1.0/Foo#a", "map:mapsTo", "onto:A"),
            ("http://onto-ns.com/meta/1.0/Foo#b", "map:mapsTo", "onto:B"),
            ("http://onto-ns.com/meta/1.0/Foo#c", "map:mapsTo", "onto:C"),
        ],
    )
    conf2 = MappingConfig(
        mappingType="triples",
        prefixes={
            "map": "http://emmo.info/domain-mappings#",
            "onto": "http://example.com/0.1/Myonto#",
        },
        triples=[
            ("http://onto-ns.com/meta/1.0/Bar#a", "map:mapsTo", "onto:A"),
            ("http://onto-ns.com/meta/1.0/Bar#d", "map:mapsTo", "onto:D"),
        ],
    )

    all_prefixes = {}
    all_prefixes.update(conf2.prefixes)

    all_triples = []
    all_triples.extend(conf2.triples)
    all_triples.extend(conf1.triples)

    session = {}

    session.update(MappingStrategy(conf2).initialize(session))

    assert session["prefixes"] == conf2.prefixes
    assert sorted(session["triples"]) == sorted(conf2.triples)

    session.update(MappingStrategy(conf1).initialize(session))

    assert session["prefixes"] == all_prefixes
    assert sorted(session["triples"]) == sorted(all_triples)

    session.update(MappingStrategy(conf1).get(session))
    session.update(MappingStrategy(conf2).get(session))

    assert session["prefixes"] == all_prefixes
    assert sorted(session["triples"]) == sorted(all_triples)
