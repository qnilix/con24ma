import argparse
from typing import Optional, Self, Union
from dataclasses import asdict, dataclass, fields

from .field import ArgField, DictField, PathField


@dataclass
class BaseConfig:

    @classmethod
    def safe_build(cls, 
                   return_unused_kwargs: bool = True, 
                   **kwargs) -> Union[tuple[Self, dict]|Self]:
        safe_kwargs = dict()
        for _f in fields(cls):
            n = _f.name
            if n in kwargs.keys(): safe_kwargs[n] = kwargs.pop(n)
        if return_unused_kwargs: return cls(**safe_kwargs), kwargs
        return cls(**safe_kwargs)
    
    def asdict(self):
        temp = asdict(self)
        for k, v in temp.items():
            if isinstance(v, DataClassConfig): temp[k] = asdict(v)
        return temp


@dataclass
class DataClassConfig(BaseConfig):

    @staticmethod
    def get_parsercls(**kwargs):
        return argparse.ArgumentParser(**kwargs)
    
    @classmethod
    def get_parser(cls) -> argparse.ArgumentParser:
        parser = cls.get_parsercls()
        for _f in fields(cls):
            if not isinstance(_f.default, (ArgField, DictField)): continue
            af = _f.default
            dest = ['--' + _f.name.replace('_', '-')]
            if af.dest is not None:
                dest += [af.dest] if isinstance(af.dest, str) else af.dest
            parser.add_argument(*dest, **af.get_argument(_f.type))
        return parser
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict: return parsed
    
    @classmethod
    def parse_args(cls, 
                   inputs: Optional[str] = None,
                   base_dict: dict = {}):
        parser = cls.get_parser()
        parsed, remain = parser.parse_known_args(inputs)
        parsed = cls.prep_parsed(vars(parsed))
        base_dict.update(parsed)
        for _f in fields(cls):
            default = _f.default_factory
            if not hasattr(default, 'parse_args'): continue
            if issubclass(default, DataClassConfig):
                if _f.name in base_dict.keys():
                    base_dict.update(**base_dict.pop(_f.name))
                base_dict[_f.name], remain = default.parse_args(remain, base_dict)
        temp = dict((k.name, base_dict.pop(k.name, k.default)) for k in fields(cls))
        return cls(**temp), remain