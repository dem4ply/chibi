import logging


__all__ = [ 'basic_config', 'silent' ]


def basic_config( level=logging.INFO ):
    from . import configuration
    logger_formarter = '%(levelname)s %(asctime)s %(name)s %(message)s'
    logging.basicConfig( level=level, format=logger_formarter )
    if configuration.env_vars.PYTHON_UNITTEST_LOGGER:
        level = configuration.env_vars.PYTHON_UNITTEST_LOGGER


def silent():
    basic_config( logging.ERROR )
