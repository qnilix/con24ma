from typing import Optional, Sequence, Type, Union

from con24ma.action import opt_action


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

    def __init__(self, value, dest: Union[list[str]|str], **kwargs):
        self.value = value
        self.dest = dest

        self.args_add_argument = argument_of_AP(**kwargs)
    
    def __int__(self): return int(self.value)

    def get_argument(self, value_type: Type) -> dict:
        kw = self.args_add_argument
        kw['type'] = value_type
        kw['default'] = self.value
        return kw


def _set_value(default = None, default_factory = None, **kwargs):
    if default is not None: return default, kwargs
    if default_factory is not None: return default_factory, kwargs
    return None, kwargs


def argfield(**kwargs):
    value, kwargs = _set_value(**kwargs)
    return ArgField(value, **kwargs)