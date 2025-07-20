import os, copy
from contextlib import contextmanager

@contextmanager
def clear_environment():
    """
    A context manager that will temporarily clear environment variables.

    When this context exits, the previous environment variables will be back.

    Example:

    ```python
    >>> import os
    >>> from accelerate.utils import clear_environment

    >>> os.environ["FOO"] = "bar"
    >>> with clear_environment():
    ...     print(os.environ)
    ...     os.environ["FOO"] = "new_bar"
    ...     print(os.environ["FOO"])
    {}
    new_bar

    >>> print(os.environ["FOO"])
    bar
    ```
    """
    _old_os_environ = os.environ.copy()
    os.environ.clear()

    try:
        yield
    finally:
        os.environ.clear()  # clear any added keys,
        os.environ.update(_old_os_environ)  # then restore previous environment


class KwargsHandler:
    """
    Internal mixin that implements a `to_kwargs()` method for a dataclass.
    """

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def to_kwargs(self):
        """
        Returns a dictionary containing the attributes with values different from the default of this class.
        """
        # import clear_environment here to avoid circular import problem

        with clear_environment():
            default_dict = self.__class__().to_dict()
        this_dict = self.to_dict()
        return {k: v for k, v in this_dict.items() if default_dict[k] != v}