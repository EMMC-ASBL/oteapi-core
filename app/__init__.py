"""
app init
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_plugins import RedisSettings, redis_plugin
from yaml import safe_load

from app.context import (
    datafilter,
    dataresource,
    mapping,
    redisadmin,
    session,
    transformation,
)
from app.strategy import loader


class AppSettings(RedisSettings):
    """
    Redis settings
    """

    api_name: str = str(__name__)


PREFIX = "/api/v1"


def load_plugins():
    """Load plugins as specified in the plugin.yml file"""
    plugins_file = Path(__file__).parent.parent / "plugins.yml"
    with open(plugins_file, "r", encoding="utf_8") as file:
        data = safe_load(file)
        loader.load_plugins(data["plugins"])


def create_app():
    """
    Create the FastAPI app
    """
    app = FastAPI()
    app.include_router(session.router, prefix=f"{PREFIX}/session")
    app.include_router(dataresource.router, prefix=f"{PREFIX}/datasource")
    app.include_router(transformation.router, prefix=f"{PREFIX}/transformation")
    app.include_router(datafilter.router, prefix=f"{PREFIX}/filter")
    app.include_router(mapping.router, prefix=f"{PREFIX}/mapping")
    app.include_router(redisadmin.router, prefix=f"{PREFIX}/redis")
    print("# Loading plugins")
    load_plugins()

    return app


config = AppSettings()
_app = create_app()


def custom_openapi():
    """Improve the default look&feel when rendering using redocs"""
    if _app.openapi_schema:
        return _app.openapi_schema
    openapi_schema = get_openapi(
        title="OntoTrans Interfaces",
        version="0.0.3-WiP",
        description="""OntoTrans Interfaces OpenAPI schema.
        <p>
        The generic interfaces are implemented in dynamic plugins which
        are concrete strategy implementations of the following types:
        <ul>
        <li><b>Download strategy</b> (access data via different protocols, such as <i>https</i> and <i>sftp</i>)</li>
        <li><b>Parse strategy</b> (data type specific interpreters, such as <i>image/jpeg, text/csv, application/sql</i>)</li>
        <li><b>Resource strategy</b> (Information resource, downloadables or services)</li>
        <li><b>Mapping strategy</b>) (define relations between business data and conceptual information)</li>
        <li><b>Filter operation strategy</b> (defines specify views/operations)</li>
        <li><b>Transformation strategy</b> (asyncronous operations) </li>
        </ul>
        """,
        routes=_app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://ontotrans.eu/wp-content/uploads/2020/05/ot_logo_rosa_gro%C3%9F.svg"
    }
    _app.openapi_schema = openapi_schema
    return _app.openapi_schema


_app.openapi = custom_openapi


@_app.on_event("startup")
async def on_startup() -> None:
    """
    initialization
    """
    await redis_plugin.init_app(_app, config=config)
    await redis_plugin.init()


@_app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    shutdown
    """
    await redis_plugin.terminate()
