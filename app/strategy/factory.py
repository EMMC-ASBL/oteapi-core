""" Factory methods for managing strategy plugins """

from typing import Callable
from app.models.mappingconfig import MappingConfig
from app.models.transformationconfig import TransformationConfig
from app.models.filterconfig import FilterConfig
from app.models.resourceconfig import ResourceConfig

from .iparsestrategy import IParseStrategy
from .idownloadstrategy import IDownloadStrategy
from .itransformationstrategy import ITransformationStrategy
from .ifilterstrategy import IFilterStrategy
from .imappingstrategy import IMappingStrategy
from .irsourcestrategy import IResourceStrategy


# Maps of strategy plugin creation functions
parse_strategy_creation_funcs: dict[str, Callable[..., IParseStrategy]] = {}
downloadstrategy_creation_funcs: dict[str, Callable[..., IDownloadStrategy]] = {}
transformation_strategy_func: dict[str, Callable[..., ITransformationStrategy]] = {}
filter_strategy_creation_func: dict[str, Callable[..., IFilterStrategy]] = {}
mapping_strategy_creation_func: dict[str, Callable[..., IMappingStrategy]] = {}
resource_strategy_creation_func: dict[str, Callable[..., IResourceStrategy]] = {}

# Registration

def register_resource_strategy(
        resource_type: str,
        create_function : Callable[..., IResourceStrategy]
    ) -> None:
    """ Register new resource strategy """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering filter_type "{resource_type}" with plugin {name}')
    resource_strategy_creation_func[resource_type] = create_function


def register_mapping_strategy(
        mapping_type: str,
        create_function : Callable[..., IMappingStrategy]
    ) -> None:
    """ Register new mapping strategy """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering filter_type "{mapping_type}" with plugin {name}')
    mapping_strategy_creation_func[mapping_type] = create_function


def register_filter_strategy(
        filter_type: str,
        create_function : Callable[..., ITransformationStrategy]
    ) -> None:
    """ Register new filter strategy """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering filter_type "{filter_type}" with plugin {name}')
    filter_strategy_creation_func[filter_type] = create_function


def register_transformation_strategy(
        app_type: str,
        create_function : Callable[..., ITransformationStrategy]
    ) -> None:
    """ Register new transformation strategy
    """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering app_type "{app_type}" with plugin {name}')
    transformation_strategy_func[app_type] = create_function


def register_parse_strategy(
        media_type: str,
        create_function : Callable[..., IParseStrategy]
    ) -> None:
    """ Register a new parse strategy """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering media-type "{media_type}" with plugin {name}')
    parse_strategy_creation_funcs[media_type] = create_function


def register_download_strategy(
    scheme: str,
    create_function : Callable[..., IDownloadStrategy]
    ) -> None:
    """ Register a new download strategy """
    name = getattr(create_function, '__name__', 'Unknown')
    print (f'- Registering download schema "{scheme}" with plugin {name}')

    downloadstrategy_creation_funcs[scheme] = create_function


# Unregistration

def unregister_resource_strategy(media_type: str):
    """ Unregister a resource strategy """
    resource_strategy_creation_func.pop(media_type, None)


def unregister_mapping_strategy(mapping_type: str):
    """ Unregister a mapping strategy """
    mapping_strategy_creation_func.pop(mapping_type, None)


def unregister_filter_strategy(filter_type: str):
    """ Unregister a filter strategy """
    filter_strategy_creation_func.pop(filter_type, None)


def unregister_transformation_strategy(app_type: str):
    """ Unregister a transformation strategy """
    downloadstrategy_creation_funcs.pop(app_type, None)


def unregister_parse_strategy(media_type: str):
    """ Unregister a datastorage """
    parse_strategy_creation_funcs.pop(media_type, None)


def unregister_download_strategy(scheme: str):
    """ Unregister a download strategy """
    downloadstrategy_creation_funcs.pop(scheme, None)


# Creation

def create_resource_strategy(config : ResourceConfig) -> IResourceStrategy:
    """ Create a resource strategy """

    media_type = config.mediaType

    try:
        creation_func = resource_strategy_creation_func[media_type]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown mediaType {media_type!r}") from None


def create_mapping_strategy(config : MappingConfig) -> IMappingStrategy:
    """ Create a mapping strategy """

    mapping_type = config.mappingType

    try:
        creation_func = mapping_strategy_creation_func[mapping_type]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown mappingType {mapping_type!r}") from None


def create_filter_strategy(config : FilterConfig) -> IFilterStrategy:
    """ Create a filter strategy """

    filter_type = config.filterType

    try:
        creation_func = filter_strategy_creation_func[filter_type]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown filterType {filter_type!r}") from None


def create_transformation_strategy(config : TransformationConfig) -> ITransformationStrategy:
    """ Create a transformation strategy """
    app_type = config.transformation_type
    try:
        creation_func = transformation_strategy_func[app_type]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown app_type {app_type!r}") from None


def create_parse_strategy(config : ResourceConfig) -> IParseStrategy:
    """ Create a parse strategy, given a dictionary of arguments """

    media_type = config.mediaType


    try:
        creation_func = parse_strategy_creation_funcs[media_type]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown media-type {media_type!r}") from None


def create_download_strategy(config : ResourceConfig) -> IDownloadStrategy:
    """ Create a download strategy, given a dictionary of arguments """

    scheme = config.downloadUrl.scheme

    try:
        creation_func = downloadstrategy_creation_funcs[scheme]
        return creation_func(config)
    except KeyError:
        raise ValueError(f"Unknown scheme {scheme!r}") from None
