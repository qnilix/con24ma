from con24ma.pathutil import getpath


class _List:

    def __call__(self, value) -> list: return list(value)

    def __getitem__(self, key: type):
        def _w(value):
            if not isinstance(value, list): value = list(value)
            return [key(v) for v in value]
        return _w

List = _List()

class _Optional:

    def __getitem__(self, key: type):
        def _w(value):
            return key(value) if value is not None else None
        return _w

Optional = _Optional()

