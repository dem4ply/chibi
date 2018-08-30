from chibi.command import command


def rabbitmqctl( *args ):
    return command( "rabbitmqctl", *args )


def add_user( user, password ):
    rabbitmqctl( 'add_user', user, password )


def delete_user( user ):
    rabbitmqctl( 'delete_user', user )


def set_user_tags( user, tag ):
    rabbitmqctl( 'set_user_tags', user, tag )


def set_permissions( vhost, user, conf='.*', write='.*', read='.*' ):
    rabbitmqctl( 'set_permissions', '-P', vhost, user, conf, write, read )
