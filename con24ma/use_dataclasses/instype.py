



class _Optional:

    def __getitem__(self, key: type):
        def _w(value): return key(value)
        return _w


Optional = _Optional()
    

