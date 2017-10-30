from chibi.command import command
from chibi.atlas import Chibi_atlas
import re


def iwconfig():
    """
    ejecuta el comando de iwconfig y lo parsea en dicionarios

    las llaves son las interfaces y los valores la informacion de las
    interfaces

    Returns
    =======
    py:class:`chibi.atlas.Chibi_atlas`
    """
    command_result, error, return_code = command( 'iwconfig', stdout='pipe' )

    regex_separador_for_raw = re.compile( r'\s\s+' )
    regex_separador_items = re.compile( r'[:=]' )
    result = {}
    for raw_interface in command_result.split( '\n\n' ):
        if not raw_interface:
            continue
        list_values_interface = regex_separador_for_raw.split( raw_interface )
        interface_name = list_values_interface.pop( 0 )
        type_ieee = list_values_interface.pop( 0 )
        interface_result = Chibi_atlas( ieee=type_ieee.split()[1] )
        result[ interface_name ] = interface_result

        for item_value in list_values_interface:
            if not item_value:
                continue
            item_value = item_value.lower()
            split_item = tuple( regex_separador_items.split( item_value, 1 ) )
            key, value = split_item
            interface_result[ key.replace( ' ', '_' ) ] = value

    return Chibi_atlas(result)