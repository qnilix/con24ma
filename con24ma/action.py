import ast, argparse


def opt_action(key: str):
    if key == 'parse_kwargs': return ParseKwargs
    return key


class ParseKwargs(argparse.Action):

    def __call__(self, parser, namespace, values: list[str], *args, **kwargs):
        kw = {}
        for value in values:
            key, value = value.split('=')
            try:
                kw[key] = ast.literal_eval(value)
            except ValueError:
                kw[key] = str(value)
        setattr(namespace, self.dest, kw)