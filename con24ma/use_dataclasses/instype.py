from con24ma.pathutil import getpath

from typing import Optional as tOptional


class _List(list):

    def __getitem__(self, key: type):
        def _w(value):
            if not isinstance(value, list): value = list(value)
            return [key(v) for v in value]
        return _w

List = _List()

class _Optional(tOptional):

    def __getitem__(self, key: type):
        def _w(value):
            return key(value) if value is not None else None
        return _w

Optional = _Optional()

