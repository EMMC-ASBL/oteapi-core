# Open Translation Environment (OTE) API Core

> Framework for accessing data resources, mapping data models, describing the data to ontologies and perform data transformations

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oteapi-core?logo=pypi)](https://pypi.org/project/oteapi-core)
[![PyPI](https://img.shields.io/pypi/v/oteapi-core?logo=pypi)](https://pypi.org/project/oteapi-core)
[![Codecov master](https://img.shields.io/codecov/c/github/EMMC-ASBL/oteapi-core/master?logo=codecov)](https://app.codecov.io/gh/EMMC-ASBL/oteapi-core)
[![CI - Tests](https://github.com/EMMC-ASBL/oteapi-core/actions/workflows/ci_tests.yml/badge.svg?branch=master)](https://github.com/EMMC-ASBL/oteapi-core/actions/workflows/ci_tests.yml?query=branch%3Amaster)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/EMMC-ASBL/oteapi-core?logo=github)](https://github.com/EMMC-ASBL/oteapi-core/pulse)
[![GitHub last commit](https://img.shields.io/github/last-commit/EMMC-ASBL/oteapi-core?logo=github)](https://github.com/EMMC-ASBL/oteapi-core/graphs/commit-activity)
[![DOI](https://zenodo.org/badge/447260507.svg)](https://zenodo.org/badge/latestdoi/447260507)


We highly recommend reading this page in [the official documentation](https://emmc-asbl.github.io/oteapi-core).

## About OTEAPI Core

OTEAPI Core provides the core functionality of OTEAPI, which stands for the *Open Translation Environment API*.

It uses the [strategy](https://en.wikipedia.org/wiki/Strategy_pattern) software design pattern to implement a simple and easy to extend access to a large range of data resources.
Semantic interoperability is supported via mapping of data models describing the data to ontologies.
A set of strategy interfaces that can be considered abstract classes for the implementation of strategies, and data models used in their configuration, are provided.
This repo also contains implementations for several standard strategies, e.g., downloading files, parsing Excel documents.
Transformations, mainly intended to transform data between representations, are also supported, but transformations can also be used for running simulations in a simple workflow.

OTEAPI Core includes:

* A set of standard strategies;
* A plugin system for loading the standard strategies, as well as third party strategies;
* Data models for configuring the strategies;
* A Python library, through which the data can be accessed; and
* An efficient data cache module that avoids downloading the same content several times.

## Types of strategies

### Download strategy

Download strategy patterns use a given protocol to download content into the data cache.
They are configured with the `ResourceConfig` data model, using the scheme of the `downloadUrl` field for strategy selection.
The `configuration` field can be used to configure how the downloaded content is stored in the cache using the `DownloadConfig` data model.

Standard downloaded strategies: *file*, *https*, *http*, *sftp*, *ftp*

### Parse strategy

Parse strategy patterns convert content from the data cache to a Python dict.
Like download strategies, they are configured with the `ResourceConfig` data model, using the `mediaType` field for strategy selection.
Additional strategy-specific configurations can be provided via the `configuration` field.

Standard parse strategies: *application/json*, *image/jpg*, *image/jpeg*, *image/jp2*, *image/png*, *image/gif*, *image/tiff*, *image/eps*, *application/vnd.openxmlformats-officedocument.spreadsheetml.sheet*, *application/vnd.sqlite3*

### Resource strategy

Resource strategy patterns can retrieve/upload data to external data services.
They are configured with the `ResourceConfig` data model, using the scheme of the `accessUrl` and `accessService` fields.
The scheme of the `accessUrl` is used for strategy selection.

### Mapping strategy

Strategies for mapping fields/properties in data models to ontological concepts.

### Filter strategy

Filter strategies can update the configuration of other strategies.
They can also update values in the data cache.

Standard filter strategies: *filter/crop*, *filter/sql*

### Function strategy

Function strategies are synchronous transformations that (normally) run directly on the server hosting the OTE service.

### Transformation strategy

Transformation strategies are a special form of a function strategy intended for long-running transformations.
In this sense, they represent asynchronous functions running in the background or on external resources.

Standard transformation strategies: *celery/remote*

The transformation strategy has consolidated the execution of the
transformation with the `get()` method to unify the strategy interfaces.
`get()` is intended to start an asynchronous process and return a
*task_id* which can be queried using the `status()` method (outside of a pipeline).

## Entry points for plugins

The way strategies are registered and found is through [entry points](https://packaging.python.org/en/latest/specifications/entry-points/).

Special group names allow understanding the strategy type and the entry point values allow understanding of what kind of strategy a specific class implements.
A full overview of recognized entry point group names can be seen in [Table of entry point strategies](#table-of-entry-point-strategies).

### Defining entry points

In the following examples, let's imagine we have a package importable in Python through `my_plugin` and contains two download strategies and a single parse strategy:

1. A peer-2-peer download strategy, implemented in a class named `Peer2PeerDownload` importable from `my_plugin.strategies.download.peer_2_peer`.
2. A MongoDB download strategy, implemented in a class named `MongoRetrieve` importable from `my_plugin.strategies.mongo`.
3. A MongoDB parse strategy, implemented in a class named `MongoParse` importable from `my_plugin.strategies.mongo`.

There are now various different ways to let the Python environment know of these strategies through entry points.

#### `setup.py`

In the package's `setup.py` file, one can specify entry points.
Here, an example snippet is shown using [setuptools](https://setuptools.pypa.io/):

```python
# setup.py
from setuptools import setup

setup(
    # ...,
    entry_points={
        "oteapi.download": [
            "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer:Peer2PeerDownload",
            "my_plugin.mongo = my_plugin.strategies.mongo:MongoRetrieve",
        ],
        "oteapi.parse": [
            "my_plugin.application/vnd.mongo+json = my_plugin.strategies.mongo:MongoParse",
        ]
    },
)
```

#### YAML/JSON custom files

Use custom files that are later parsed and used in a `setup.py` file.

```yaml
entry_points:
  oteapi.download:
  - "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer:Peer2PeerDownload"
  - "my_plugin.mongo = my_plugin.strategies.mongo:MongoRetrieve"
  oteapi.parse:
  - "my_plugin.application/vnd.mongo+json = my_plugin.strategies.mongo:MongoParse"
```

```json
{
  "entry_points": {
    "oteapi.download": [
      "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer:Peer2PeerDownload",
      "my_plugin.mongo = my_plugin.strategies.mongo:MongoRetrieve"
    ],
    "oteapi.parse": [
      "my_plugin.application/vnd.mongo+json = my_plugin.strategies.mongo:MongoParse"
    ]
  }
}
```

#### `setup.cfg`/`pyproject.toml`

A more modern approach is to use `setup.cfg` or `pyproject.toml`.

```ini
[options.entry_points]
oteapi.download =
    my_plugin.p2p = my_plugin.strategies.download.peer_2_peer:Peer2PeerDownload
    my_plugin.mongo = my_plugin.strategies.mongo:MongoRetrieve
oteapi.parse =
    my_plugin.application/vnd.mongo+json = my_plugin.strategies.mongo:MongoParse
```

### Syntax and semantics

As seen above, there are a few different syntactical flavors of how to list the entry points.
However, the "value" stays the same throughout.

#### General Python entry points

The general syntax for entry points is based on `ini` files and parsed using the built-in `configparser` module described [here](https://docs.python.org/3/library/configparser.html#module-configparser).
Specifically for entry points the nomenclature is the following:

```ini
[options.entry_points]
GROUP =
    NAME = VALUE
```

The `VALUE` is then further split into: `PACKAGE.MODULE:OBJECT.ATTRIBUTE [EXTRA1, EXTRA2]`.

#### OTEAPI strategy entry points

From the general syntax outlined above, OTEAPI Core then implements rules and requirements regarding the syntax for strategies.

1. A class *MUST* be specified (as an `OBJECT`).
2. The `NAME` *MUST* consist of exactly two parts: `PACKAGE` and strategy type value in the form of `PACKAGE.STRATEGY_TYPE_VALUE`.
3. The `GROUP` *MUST* be a valid OTEAPI entry point group, see [Table of entry point strategies](#table-of-entry-point-strategies) for a full list of valid OTEAPI entry point group values.

To understand what the strategy type value should be, see [Table of entry point strategies](#table-of-entry-point-strategies).

### Table of entry point strategies

| Strategy Type Name | Strategy Type Value | Entry Point Group | Documentation Reference |
|:---:|:---:|:---:|:--- |
| Download | [`scheme`][oteapi.models.resourceconfig.ResourceConfig.downloadUrl] | `oteapi.download` | [Download strategy](#download-strategy) |
| Filter | [`filterType`][oteapi.models.filterconfig.FilterConfig.filterType] | `oteapi.filter` | [Filter strategy](#filter-strategy) |
| Function | [`functionType`][oteapi.models.functionconfig.FunctionConfig.functionType] | `oteapi.function` | [Function strategy](#function-strategy) |
| Mapping | [`mappingType`][oteapi.models.mappingconfig.MappingConfig.mappingType] | `oteapi.mapping` | [Mapping strategy](#mapping-strategy) |
| Parse | [`mediaType`][oteapi.models.resourceconfig.ResourceConfig.mediaType] | `oteapi.parse` | [Parse strategy](#parse-strategy) |
| Resource | [`accessService`][oteapi.models.resourceconfig.ResourceConfig.accessService] | `oteapi.resource` | [Resource strategy](#resource-strategy) |
| Transformation | [`transformationType`][oteapi.models.transformationconfig.TransformationConfig.transformationType] | `oteapi.transformation` | [Transformation strategy](#transformation-strategy) |

## Other OTEAPI-related repositories

* [OTEAPI Services](https://github.com/EMMC-ASBL/oteapi-services) - a RESTful interface to OTEAPI Core
* [OTELib](https://github.com/EMMC-ASBL/otelib) - a Python interface to OTEAPI Services
* [OTEAPI Plugin Template](https://github.com/EMMC-ASBL/oteapi-plugin-template) - a [cookiecutter](https://cookiecutter.readthedocs.io/) template for OTEAPI Plugins

## Installation

OTEAPI Core can be installed with:

```shell
pip install oteapi-core
```

### For developers

If you want to install OTEAPI Core to have a developer environment, please clone down the repository from GitHub and install:

```shell
git clone https://github.com/EMMC-ASBL/oteapi-core /path/to/oteapi-core
pip install -U --upgrade-strategy=eager -e /path/to/oteapi-core[dev]
```

Note, `/path/to/oteapi-core` can be left out of the first line, but then it must be updated in the second line, either to `./oteapi-core`/`oteapi-core` or `.` if you `cd` into the generated folder wherein the repository has been cloned.

The `--upgrade-strategy=eager` part can be left out.
We recommend installing within a dedicated virtual environment.

To test the installation, you can run:

```shell
cd /path/to/oteapi-core
pytest
```

If you run into issues at this stage, please [open an issue](https://github.com/EMMC-ASBL/oteapi-core/issues/new).



## Using Docker with PostgreSQL
Docker is an effective tool for creating portable, isolated environments for your applications. Here's an example of setting up a PostgreSQL instance using Docker:

1. **Create a Docker volume**: Docker volumes enable data to persist across uses of Docker containers. In this context, we create a volume called pgdata to store database data.

```shell
docker volume create pgdata
```

2. **Start a Docker container**: Use the `docker run` command to initiate a new Docker container using the postgres image. Here's a breakdown of the options used in the command:

   `-d`: Runs the container in the background (detached mode), freeing up your terminal.

   `--name postgres`: Names the container postgres, allowing it to be referenced in future Docker commands.

   `-e POSTGRES_PASSWORD=postgres`: Sets an environment variable in the container to specify the PostgreSQL database password as postgres.

   `-p 5432:5432`: Maps port 5432 of the container to port 5432 of the host machine, letting applications on the host connect to the PostgreSQL database in the container.

   `-v pgdata:/var/lib/postgresql/data`: Mounts the pgdata volume at the path /var/lib/postgresql/data inside the container, which is the storage location for PostgreSQL data files.

   `--restart always`: Ensures the container restarts whenever it stops, unless it is manually stopped, in which case it only restarts when the Docker daemon starts, usually on system boot.

```shell
docker run  -d --name postgres \
                   -e POSTGRES_PASSWORD=postgres \
                   -p 5432:5432 \
                   -v pgdata:/var/lib/postgresql/data \
                   --restart always postgres
```

## License

OTEAPI Core is released under the [MIT license](LICENSE.md) with copyright &copy; SINTEF.

## Acknowledgment

OTEAPI Core has been supported by the following projects:

* __OntoTrans__ (2020-2024) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement no. 862136.

* __VIPCOAT__ (2021-2025) receives funding from the European Union’s Horizon 2020 Research and Innovation Programme - DT-NMBP-11-2020 Open Innovation Platform for Materials Modelling, under Grant Agreement no: 952903.

* __OpenModel__ (2021-2025) receives funding from the European Union’s Horizon 2020 Research and Innovation Programme - DT-NMBP-11-2020 Open Innovation Platform for Materials Modelling, under Grant Agreement no: 953167.
