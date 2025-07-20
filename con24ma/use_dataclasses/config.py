import argparse
from typing import Optional
from dataclasses import asdict, dataclass, fields

from .field import ArgField, DictField, PathField


@dataclass
class BaseConfig:

    @classmethod
    def safe_build(cls, return_unused_kwargs: bool = False, **kwargs):
        safe_kwargs = dict()
        for _f in fields(cls):
            n = _f.name
            if n in kwargs.keys(): safe_kwargs[n] = kwargs.pop(n)
        return cls(**safe_kwargs)


@dataclass
class DataClassConfig:

    def asdict(self):
        temp = asdict(self)
        for k, v in temp.items():
            if isinstance(v, DataClassConfig): temp[k] = asdict(v)
        return temp

    @classmethod
    def get_parsercls(cls, **kwargs):
        return argparse.ArgumentParser(**kwargs)
    
    @classmethod
    def get_parser(cls):
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
                   input_args: Optional[str] = None,
                   kwargs: dict = {}):
        parser = cls.get_parser()
        parsed, remain = parser.parse_known_args(input_args)
        parsed = cls.prep_parsed(vars(parsed))
        kwargs.update(parsed)
        for _f in fields(cls):
            if not hasattr(_f.default_factory, 'parse_args'): continue
            if issubclass(_f.default_factory, DataClassConfig):
                if _f.name in kwargs.keys(): kwargs.update(**kwargs.pop(_f.name))
                kwargs[_f.name], remain = _f.default_factory.parse_args(remain, kwargs)
        temp = dict((k.name, kwargs.pop(k.name, k.default)) for k in fields(cls))
        return cls(**temp), remain