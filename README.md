# OTEAPI Core
> Framework for accessing data resources, mapping data models describing the data to ontologies and perform data transformations

OTEAPI Core provides the core functionality of OTEAPI, which stands for the *Open Translation Environment API*.


It uses the [strategy](https://en.wikipedia.org/wiki/Strategy_pattern) software design pattern to implement a simple and easy to extend access to a large range of data resources.
Semantic interoperability is supported via mapping of data models describing the data to ontologies.
Transformations, mainly intended to transform data between representations, are also supported.  But transformations can also be used for running simulations in a simple workflow.

OTEAPI Core include:
- a small set of standard strategies
- a plugin system for loading the standard strategies as well as third party strategies
- data models for configuring the strategies
- a Python library through which the data can be accessed
- an efficient data cache module that avoids downloading the same content several times


## Types of strategies

### Download strategy
Download strategy patterns use a given protocol to download content into the data cache.  They are configured with the ResourceConfig data model, using the scheme of the
`downloadUrl` field for strategy selection.  The `configuration` field can be used to configure how the downloaded content is stored in the cache using the DownloadConfig data model.

Standard downloaded strategies: file, https, sftp


### Parse strategy
Parse strategy patterns convert content from the data cache to a Python dict. Like download strategies, they are configured with the ResourceConfig data model, using the
`mediaType` field for strategy selection.  Additional strategy-specific configurations can be provided via the `configuration` field.

Standard parse strategies: text_csv, text_json, image_jpeg, excel_xlsx


### Resource strategy
Resource strategy patterns can retrieve/upload data to external data services.  They are configured with the ResourceConfig data model, using the scheme of the `accessUrl` and `accessService` fields.  The scheme of the `accessUrl` is used for strategy selection.


### Mapping strategy
Strategies for mapping fields/properties in data models to ontological concepts.


### Filter strategy
Filter strategies can update the configuration of other strategies.  They can also update values in the data cache.


### Transformation strategy
Transformation strategies are a special form of a filter strategy intended for long-running transformations.



## Related projects
* [OTEAPI Services](https://github.com/EMMC-ASBL/oteapi-services) - a RESTful interface to OTEAPI Core
* [OTELib](https://github.com/EMMC-ASBL/oteapi-services) - a Python interface to OTEAPI Services
