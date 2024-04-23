from pathlib import Path

from aiopenapi3 import OpenAPI, FileSystemLoader

DD = Path(__file__).parent / "description_document" / "openapi.yaml"


def createAPI(addr, **kwargs):
    return OpenAPI.load_file(f"http://{addr}/openapi.yaml", DD.name, loader=FileSystemLoader(DD.parent), **kwargs)


__all__ = ["createAPI"]
