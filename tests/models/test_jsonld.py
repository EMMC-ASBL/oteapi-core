import json
from pathlib import Path

import rdflib
from rdflib.plugins.shared.jsonld.context import Context

from oteapi.utils import rdf

thisdir = Path(__file__).resolve().parent
testdir = thisdir.parent
staticdir = testdir / "static"

# s = """
# {
#   "@context": {
#     "@vocab": "http://xmlns.com/foaf/0.1/",
#     "knows": {"@type": "@id"}
#   },
#   "@id": "http://manu.sporny.org/about#manu",
#   "@type": "Person",
#   "name": "Manu Sporny",
#   "knows": {
#     "@id": "https://greggkellogg.net/foaf#me",
#     "@type": "Person",
#     "name": "Gregg Kellogg"
#   }
# }
# """
# g = rdflib.Graph()
# g.parse(data=s, format="json-ld")
# #print(g.serialize(format="turtle"))
# #print("------------------------------------------------")
# #print()
#
#
# conf = """
# {
#   "@context": {
#     "oteio": "https://w3id.org/emmo/domain/oteio#",
#     "dcat": "http://www.w3.org/ns/dcat#",
#     "dcterms": "http://purl.org/dc/terms/",
#
#     "downloadURL": "dcat:downloadURL",
#     "mediaType": "dcat:mediaType",
#     "license": "dcterms:license",
#     "driver": "oteio:driver",
#     "configuration": "oteio:configuration",
#     "dataresource": "oteio:dataresource"
#   },
#   "http://example.com/ex/faithfull": {
#     "@type": "oteio:Source",
#     "@id": "http://example.com/ex/faithfull",
#     "dataresource": {
#       "downloadURL": "http://example.com/datasets/faithfull.csv",
#       "mediaType": "application/csv",
#       "license": "https://creativecommons.org/licenses/by/4.0/legalcode",
#       "configuration": {
#         "driver": "csv"
#       }
#     }
#   }
# }
# """
# #  "http://example.com/ex/faithfull": {
# g = rdflib.Graph()
# #g.bind("ex", "http://example.com/ex/")
# g.parse(data=conf, format="json-ld")
# #print(g.serialize(format="turtle"))
# #print("------------------------------------------------")
# #print()


conf2 = """
{
  "@context": {
    "@version": 1.1,

    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dcterms": "http://purl.org/dc/terms/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "oteio": "https://w3id.org/emmo/domain/oteio#",

    "resources": "@nest",
    "configuration": {
      "@id": "oteio:configuration",
      "@type": "@json"
    },
    "dataresource": {
      "@id": "oteio:dataresource",
      "@type": "oteio:DataResource",
      "@nest": "resources"
    },
    "downloadURL": "dcat:downloadURL",
    "mediaType": "dcat:mediaType",
    "license": "dcterms:license",

    "parse": "oteio:parse",
    "parserType": "oteio:parserType",
    "datamodel": "oteio:datamodel",

    "driver": "oteio:driver"
  },

  "resources": [
    {
      "@type": "oteio:Source",
      "@id": "http://example.com/ex/faithfull",
      "dataresource": {
        "downloadURL": "http://example.com/datasets/faithfull.csv",
        "mediaType": "application/csv",
        "license": "https://creativecommons.org/licenses/by/4.0/legalcode"
      },
      "parse": {
        "parserType": "application/vnd.dlite-parse",
        "datamodel": "http://onto-ns.com/meta/calm/0.1/Composition",
        "configuration": {
          "driver": "csv"
        }
      }
    }
  ]
}
"""
#  "http://example.com/ex/faithfull": {
g = rdflib.Graph()
# g.bind("ex", "http://example.com/ex/")
# print(json.loads(conf2))
g.parse(data=conf2, format="json-ld")
print(g.serialize(format="turtle"))
print("------------------------------------------------")
print()
context_data = json.loads(conf2).get("@context")
context = Context(context_data)
graph_data = json.loads(
    g.serialize(format="json-ld", context_data=context_data, auto_compact=True)
).get("@graph")
# print(json.dumps(graph_data, indent=2))
# print("------------------------------------------------")
# print()


def expand(item):
    """Returns `item` with all all references to blank nodes expanded."""
    d = {}
    for k, v in item.items():
        if k == "@id":
            if v.startswith("_:"):
                dct = iris[v].copy()
                dct.pop("@id")
                d.update(expand(dct))
            else:
                d[k] = v
        elif isinstance(v, dict):
            if "@value" in v:
                if v.get("@type") == "rdf:JSON":
                    d[k] = json.loads(v["@value"])
                else:
                    d[k] = v["@value"]
            else:
                d[k] = expand(v)
        else:
            d[k] = v
    return d


def from_rdf(graph, context_data):
    graph_data = json.loads(
        g.serialize(format="json-ld", context_data=context_data, auto_compact=True)
    ).get("@graph")
    # iris = {d["@id"]: d for d in graph_data if "@id" in d}
    resources = [
        expand(d) for d in graph_data if "@id" in d and not d["@id"].startswith("_:")
    ]
    json_data = {
        "resources": resources,
    }
    return json_data


iris = {d["@id"]: d for d in graph_data if "@id" in d}
assert "http://example.com/ex/faithfull" in iris
# resources = [
#    expand(d) for d in graph_data
#    if "@id" in d and not d["@id"].startswith("_:")
# ]
#
# json_data = {
#    "resources": resources,
# }
# print(json.dumps(json_data, indent=2))
print(json.dumps(from_rdf(g, context_data), indent=2))


# PREFIX ex: <http://example.com/ex/>
res = g.query(
    """
PREFIX ex: <http://example.com/ex/>
CONSTRUCT { ?s ?p ?o }
WHERE {
  ex:faithfull (<>|!<>) ?s .
  ?s ?p ?o .
}
"""
)


# data = """
# @prefix : <urn:ex:> .
#
# :A :p :B, :C .
# :B :q :D .
# :C :r :E .
#
# :F :s :G .
# :G :t :H .
# """
# query = """
# PREFIX x: <urn:ex:>
# PREFIX : <urn:ex:>
#
# CONSTRUCT {
#   ?s ?p ?o
# }
# WHERE {
#   :A (<>|!<>)* ?s .
#   ?s ?p ?o .
# }
# """
# graph = rdflib.Graph()
# graph.parse(data=data)
# res = graph.query(query)


# with open(staticdir / "resources.yaml", "rt", encoding="utf8") as f:
#    data = yaml.safe_load(f)

graph = rdf.add_resource(staticdir / "resources.yaml")
