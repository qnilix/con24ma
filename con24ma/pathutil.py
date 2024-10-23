import re, pathlib
from typing import Optional, Union

def _root(init: Optional[str] = None):
    if init is None: return pathlib.Path()
    if init == '/': return pathlib.Path('/')
    if init == '~/': return pathlib.Path.home()

def joindir(path: pathlib.Path, join: str, mkdir: bool = False) -> pathlib.Path:
    path.joinpath(join)
    path.mkdir(parents=True, exist_ok=mkdir)
    return path

def getpath(path: Union[pathlib.Path|str], mkdir: bool = False) -> pathlib.Path:
    if isinstance(path, pathlib.Path): return path
    init, path = re.match(r"(~?/)?(.*)", path).groups()
    return joindir(_root(init), path, mkdir=mkdir)