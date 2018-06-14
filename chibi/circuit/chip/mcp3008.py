import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


class MCP3008:
    """
    clase para abstraer el uso del chip MCP3008

    Attributes
    ==========
    v_dd: float
        voltaje del chip
    v_ref: float
        voltaje de refencia del chil
    """
    def __init__( self, v_dd=5, v_ref=5, spi_port=0, spi_device=0 ):
        self._chip = Adafruit_MCP3008.MCP3008(
            spi=SPI.SpiDev( SPI_PORT, SPI_DEVICE ) )
        self.v_dd = v_dd
        self.v_ref = v_ref

    def read( self, channel ):
        """
        lee un canal del chip

        Parameters
        ==========
        channel: int

        Returns
        =======
        int
            valor entre 0 y 1024
        """
        return self._chip.read_adc( channel )

    def read_voltage( self, channel ):
        """
        lee el voltaje de un canal del chip

        Parameters
        ==========
        channel: int

        Returns
        =======
        float
            valor entre 0 y v_ref
        """
        return read( channel ) * ( self.v_ref / 1023 )

    def read_analogic_voltage( self, channel ):
        analogic = self.read( channel )
        voltage = analogic * ( self.v_ref / 1023 )
        return analogic, voltage

    def detach_channel( self, channel ):
        return MCP3008_channel( self, channel )

    def __getitem__( self, channel ):
        return self.read( channel )

    def __iter__( self ):
        return ( self.read( i ) for i in range( 8 ) )


class MCP3008_channel:
    """
    clase para leer un canal de manera dedicada de MCP3008
    """
    def __init__( self, chip, channel ):
        self.chip = chip
        self.channel = channel

    def read( self ):
        return self.chip.read( self.channel )

    def read_voltage( self ):
        return self.chip.read_voltage( self.channel )
