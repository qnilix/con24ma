import argparse
from typing import Optional
from dataclasses import dataclass, fields

from .field import ArgField


@dataclass
class DataClassConfig:

    def __post_init__(self):
        for _f in fields(self):
            if isinstance(_f.default, ArgField):
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
    
    @staticmethod
    def parse_args(main_cls, input_args: Optional[str] = None):
        parser = main_cls.get_parser()
        parsed, remain = parser.parse_known_args(input_args)
        parsed = vars(parsed)
        for _f in fields(main_cls):
            if isinstance(_f.default, DataClassConfig):
                parsed[_f.name] = _f.default.parse_args(_f.default, remain)
        return main_cls(**parsed)