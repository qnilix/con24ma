import argparse
from typing import Optional, Self
from dataclasses import asdict, dataclass, fields

from .field import ArgField, DictField


@dataclass
class BaseConfig:
    """Dataclass-based config base providing safe instantiation and dict conversion."""

    @classmethod
    def safe_build(cls,
                   return_unused_kwargs: bool = True,
                   **kwargs) -> tuple[Self, dict] | Self:
        """Build an instance using only kwargs that match declared fields.

        Args:
            return_unused_kwargs: If True, also return kwargs not consumed by this class.
            **kwargs: Configuration values; unrecognised keys are left untouched.

        Returns:
            A (instance, unused_kwargs) tuple when return_unused_kwargs is True,
            otherwise the instance alone.
        """
        safe_kwargs = {}
        for _f in fields(cls):
            n = _f.name
            if n in kwargs: safe_kwargs[n] = kwargs.pop(n)
        if return_unused_kwargs: return cls(**safe_kwargs), kwargs
        return cls(**safe_kwargs)

    def asdict(self) -> dict:
        """Return all fields as a plain dictionary."""
        return asdict(self)


@dataclass
class DataClassConfig(BaseConfig):
    """Config class with argparse-based CLI argument parsing.

    Fields annotated with ArgField or DictField are automatically registered
    as command-line arguments on the parser.
    """

    @staticmethod
    def get_parsercls(**kwargs):
        """Return an ArgumentParser instance. Override in subclasses to swap the parser type."""
        return argparse.ArgumentParser(**kwargs)

    @classmethod
    def get_parser(cls) -> argparse.ArgumentParser:
        """Build and return an ArgumentParser from fields declared as ArgField or DictField."""
        parser = cls.get_parsercls()
        for _f in fields(cls):
            if not isinstance(_f.default, (ArgField, DictField)):
                continue
            af = _f.default
            dest = ['--' + _f.name.replace('_', '-')]
            if af.dest is not None:
                dest += [af.dest] if isinstance(af.dest, str) else af.dest
            parser.add_argument(*dest, **af.get_argument(_f.type))
        return parser

    @classmethod
    def prep_parsed(cls, parsed: dict) -> dict:
        """Pre-process the raw parsed dict before instantiation. Override to transform values."""
        return parsed

    @classmethod
    def parse_args(cls, inputs: Optional[list[str]] = None,
                   base_dict: dict = {}):
        """Parse command-line arguments and return a config instance with any remaining args.

        Args:
            inputs: Argument list to parse; defaults to sys.argv when None.
            base_dict: Base dictionary to merge parsed values into.

        Returns:
            A (config instance, remaining unparsed args) tuple.
        """
        parser = cls.get_parser()
        parsed, remain = parser.parse_known_args(inputs)
        parsed = cls.prep_parsed(vars(parsed))
        base_dict.update(parsed)
        for _f in fields(cls):
            default = _f.default_factory
            if not hasattr(default, 'parse_args'): continue
            if _f.name in base_dict:
                base_dict.update(**base_dict.pop(_f.name))
            base_dict[_f.name], remain = default.parse_args(remain, base_dict)
        temp = {k.name: base_dict.pop(k.name, k.default) for k in fields(cls)}
        return cls(**temp), remain