from typing import Optional, Sequence, Type, Union

from con24ma.action import opt_action
from con24ma.pathutil import getpath


def argument_of_AP(action: Optional[str] = None,
                   nargs: Optional[int|str] = None,
                   const = None, 
                   choices: Optional[Sequence] = None,
                   required: Optional[bool] = None,
                   help: Optional[str] = None,
                   metavar: Optional[str] = None):
    kw = dict()
    if action is not None: kw['action'] = opt_action(action)
    if nargs is not None: kw['nargs'] = nargs
    if const is not None: kw['const'] = const
    return kw


class ArgField:

    def __init__(self, value, 
                 dest: Optional[Union[list[str]|str]] = None, **kwargs):
        self.value = value
        self.dest = dest

        self.args_add_argument = argument_of_AP(**kwargs)
    
    def __bool__(self): return bool(self.value)

    def __float__(self): return float(self.value)
    
    def __int__(self): return int(self.value)

    def __str__(self): return str(self.value)

    def get_argument(self, value_type: Type) -> dict:
        kw = self.args_add_argument
        kw['type'] = value_type
        kw['default'] = self.value
        return kw


class PathField:

    def __init__(self, value, 
                 dest: Optional[Union[list[str]|str]] = None, 
                 as_rootdir: bool = False,
                 as_cfgpath: bool = False, **kwargs):
        self.value = getpath(value)
        self.dest = dest

        self.admin = ''
        if self.value.is_file():
            if as_cfgpath: self.admin
        elif as_rootdir:
            self.admin = 'dir' 

        self.args_add_argument = argument_of_AP(**kwargs)


def _set_value(default = None, default_factory = None, **kwargs):
    if default is not None: return default, kwargs
    if default_factory is not None: return default_factory, kwargs
    return None, kwargs


def argfield(**kwargs):
    value, kwargs = _set_value(**kwargs)
    return ArgField(value, **kwargs)