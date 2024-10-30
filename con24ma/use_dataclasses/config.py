import argparse
from typing import Optional
from dataclasses import dataclass, fields, replace

from .field import ArgField, PathField


@dataclass
class DataClassConfig:

    def __post_init__(self):
        for _f in fields(self):
            if isinstance(_f.default, ArgField):
                print(_f.name)
                setattr(self, _f.name, _f.type(_f.default))

    @classmethod
    def get_parsercls(cls, **kwargs):
        return argparse.ArgumentParser(**kwargs)
    
    @classmethod
    def get_parser(cls):
        parser = cls.get_parsercls()
        for _f in fields(cls):
            if not isinstance(_f.default, ArgField): continue
            af = _f.default
            dest = ['--' + _f.name.replace('_', '-')]
            if af.dest is not None:
                dest += [af.dest] if isinstance(af.dest, str) else af.dest
            parser.add_argument(*dest, **af.args_add_argument(_f.type))
        return parser
    
    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict: return parsed
    
    @classmethod
    def parse_args(cls, 
                   input_args: Optional[str] = None):
        parser = cls.get_parser()
        parsed, remain = parser.parse_known_args(input_args)
        parsed = cls.prep_parsed(vars(parsed))
        for _f in fields(cls):
            if isinstance(_f.default, DataClassConfig):
                parsed[_f.name] = _f.default.parse_args(_f.default, remain)
        return cls(**parsed)