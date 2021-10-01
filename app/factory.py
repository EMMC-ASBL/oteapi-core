""" Factory methods for managing strategy plugins """

from typing import Callable, Any
from app.idownloadstrategy import IDownloadStrategy
from app.iparsestrategy import IParseStrategy
from app.itransformationstrategy import ITransformationStrategy


# Maps of strategy plugin creation functions

parse_strategy_creation_funcs: dict[str, Callable[..., IParseStrategy]] = {}
downloadstrategy_creation_funcs: dict[str, Callable[..., IDownloadStrategy]] = {}
transformation_strategy_func: dict[str, Callable[..., ITransformationStrategy]] = {}

# Registration

def register_transformation_strategy(
        app_type: str,
        create_function : Callable[..., ITransformationStrategy]
    ) -> None:
    """ Register new transformation strategy """
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

def create_transformation_strategy(arguments: dict[str, Any]) -> ITransformationStrategy:
    """ Create a transformation strategy """
    args_copy = arguments.copy()
    app_type = args_copy.pop("app_type")

    try:
        creation_func = transformation_strategy_func[app_type]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown app_type {app_type!r}") from None


def create_parse_strategy(arguments: dict[str, Any]) -> IParseStrategy:
    """ Create a parse strategy, given a dictionary of arguments """

    args_copy = arguments.copy()
    media_type = args_copy.pop("media_type")

    try:
        creation_func = parse_strategy_creation_funcs[media_type]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown media-type {media_type!r}") from None


def create_download_strategy(arguments: dict[str, Any]) -> IDownloadStrategy:
    """ Create a download strategy, given a dictionary of arguments """

    args_copy = arguments.copy()
    scheme = args_copy.pop("scheme")

    try:
        creation_func = downloadstrategy_creation_funcs[scheme]
        return creation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown scheme {scheme!r}") from None
