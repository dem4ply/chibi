from .config import __all__ as config_all, Configuration
from .logger import *  # noqa


__all__ = config_all + logger.__all__


configuration = Configuration()


def load( path ):
    configuration.load( path )
