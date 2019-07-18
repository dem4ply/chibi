
from chibi.command import command
from chibi.atlas import Chibi_atlas
from chibi.net.network.interface import Network
from chibi.madness.file import make_empty_file
from chibi.command.nmcli import connection
from chibi.file.image import Chibi_image
import re


def qr( *args ):
    return command( 'qrencode', *args )


def wifi( ssid, s=3, f=None ):
    if f is None:
        f = make_empty_file( '.png' )

    connection_atlas = connection.show( ssid )[ ssid ]
    T = connection_atlas[ '802-11-wireless-security.key-mgmt' ]
    if T == 'wpa-psk':
        T = 'WPA'
    data = "WIFI:S:{ssid};T:{T};P:{password};;".format(
        ssid=connection_atlas[ '802-11-wireless.ssid' ],
        password=connection_atlas[ '802-11-wireless-security.psk' ],
        T=T
    )

    qr( '-o', f, '-s', s, data )
    return Chibi_image( f )
