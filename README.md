# Open Translation Environment (OTE) API Core

> Framework for accessing data resources, mapping data models, describing the data to ontologies and perform data transformations

We highly recommend reading this page in [the official documentation](https://emmc-asbl.github.io/oteapi-core).

## About OTEAPI Core

OTEAPI Core provides the core functionality of OTEAPI, which stands for the *Open Translation Environment API*.

It uses the [strategy](https://en.wikipedia.org/wiki/Strategy_pattern) software design pattern to implement a simple and easy to extend access to a large range of data resources.
Semantic interoperability is supported via mapping of data models describing the data to ontologies.
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

Standard parse strategies: *text_csv*, *text_json*, *image_jpeg*, *excel_xlsx*

### Resource strategy

Resource strategy patterns can retrieve/upload data to external data services.
They are configured with the `ResourceConfig` data model, using the scheme of the `accessUrl` and `accessService` fields.
The scheme of the `accessUrl` is used for strategy selection.

### Mapping strategy

Strategies for mapping fields/properties in data models to ontological concepts.

### Filter strategy

Filter strategies can update the configuration of other strategies.
They can also update values in the data cache.

### Transformation strategy

Transformation strategies are a special form of a filter strategy intended for long-running transformations.

## Entry points for plugins

Suggestion: Use setuptools entry points to load plugins.

The entry point groups could be named as something like this:

* `"oteapi.download_strategy"`, `"oteapi.filter_strategy"`
* `"oteapi.download"`, `"oteapi.filter"`
* `"oteapi.interfaces.download"`, `"oteapi.interfaces.filter"`

The value for an entrypoint should then be:

```python
setup(
    # ...,
    entry_points={
        "oteapi.download_strategy": [
            "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer",
            "my_plugin.mongo = my_plugin.strategies.download.mongo_get",
        ],
    },
)
```

or as part of a YAML/JSON/setup.cfg setup files as such:

```yaml
entry_points:
  oteapi.download_strategy:
  - "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer"
  - "my_plugin.mongo = my_plugin.strategies.download.mongo_get"
```

```json
{
  "entry_points": {
    "oteapi.download_strategy": [
      "my_plugin.p2p = my_plugin.strategies.download.peer_2_peer",
      "my_plugin.mongo = my_plugin.strategies.download.mongo_get"
    ]
  }
}
```

```ini
[options.entry_points]
oteapi.download_strategy =
    my_plugin.p2p = my_plugin.strategies.download.peer_2_peer
    my_plugin.mongo = my_plugin.strategies.download.mongo_get
```

The plugins will then automagically load all installed strategy module plugins, registering the strategies according to the `StrategyFactory` decorator.

## Other OTEAPI-related repositories

* [OTEAPI Services](https://github.com/EMMC-ASBL/oteapi-services) - a RESTful interface to OTEAPI Core
* [OTELib](https://github.com/EMMC-ASBL/otelib) - a Python interface to OTEAPI Services
* [OTEAPI Plugin Template](https://github.com/EMMC-ASBL/oteapi-plugin-template) - a [cookiecutter](https://cookiecutter.readthedocs.io/) template for OTEAPI Plugins

## Installation

OTEAPI Core can be installed with:

```console
$ pip install oteapi-core
```

## License

OTEAPI Core is released under the [MIT license](LICENSE) with copyright &copy; SINTEF.

## Acknowledgment

OTEAPI Core has been supported by the following projects:

* __OntoTrans__ (2020-2024) that receives funding from the European Union’s Horizon 2020 Research and Innovation Programme, under Grant Agreement n. 862136.
