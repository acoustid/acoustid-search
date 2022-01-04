from typing import Mapping
from configparser import ConfigParser

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine

from acoustid_search.handlers import routes
from acoustid_search.index import IndexClient
from acoustid_search.backend import Backend, BackendRegistry
from acoustid_search.legacy.backend import LegacySearchBackend


def create_legacy_backend(config: Mapping[str, str]) -> Backend:
    db = create_async_engine(config['db_url'])
    index = IndexClient(config['index_url'])
    catalog_name = config['catalog']
    return LegacySearchBackend(db, index, catalog_name)


def create_default_backend(config: Mapping[str, str]) -> Backend:
    raise NotImplementedError("No default backend")


BACKEND_FACTORIES = {
    'legacy': create_legacy_backend,
    'default': create_default_backend,
}


def create_backends(config: ConfigParser) -> None:
    backends = BackendRegistry()
    for section_name in config.sections():
        if section_name.startswith("backend:"):
            backend_name = section_name[8:]
            backend_config = config[section_name]
            backend_mode = backend_config.get('mode', 'default')
            try:
                backend_factory = BACKEND_FACTORIES[backend_mode]
            except KeyError:
                raise ValueError(f"Unknown backend mode: {backend_mode}")
            backend = backend_factory(backend_config)
            backends.register_backend(backend_name, backend)
            catalog_pattern = backend_config.get('catalog', None)
            if catalog_pattern is not None:
                backends.route(catalog_pattern, backend_name)
            else:
                backend.set_default_backend(backend_name)


def create_app(backends: BackendRegistry) -> web.Application:
    app = web.Application()
    app["backends"] = backends
    app.router.add_routes(routes)
    return app
