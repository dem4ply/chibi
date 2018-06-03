import pip


def install(*packages):
    """
    instala los paquetes de python

    Arguments
    =========
    packages: tuple of strings
        lista de paquetes que se quieren instalar
    """
    return pip.main( [ 'install', *packages] )


def upgrade(*packages):
    """
    actualiza los paquetes de python

    Arguments
    =========
    packages: tuple of strings
        lista de paquetes que se quieren actualizar
    """
    return pip.main( [ 'install', '--upgrade', *packages] )


def uninstall(*packages):
    """
    elimina los paquetes de python

    Arguments
    =========
    packages: tuple of strings
        lista de paquetes que se quieren eliminar
    """
    return pip.main( [ 'uninstall', '--yes', *packages] )
