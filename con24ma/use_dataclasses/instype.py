



class _Optional:

    def __getitem__(self, key: type):
        def _w(value):
            return key(value) if value is not None else None
        return _w


Optional = _Optional()
    

