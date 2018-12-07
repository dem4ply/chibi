from chibi.command import command


def mpc( *args ):
    return command( 'mpc', *args )


def pause():
    return mpc( 'pause' )


def play():
    return mpc( 'play' )
