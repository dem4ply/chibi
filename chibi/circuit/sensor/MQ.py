class Rack_sensor:
    def __init__( self, *sensors ):
        self.sensors = list( sensors )

    def append( self, *sensors ):
        sensors = list( sensors )
        self.sensors += sensors

    def read( self ):
        result = {}
        for sensor in self.sensors:
            result.update( sensor.read() )
        return result


class MQ:
    """
    clase general para leer los sensores de aire MQ

    Attributes
    ==========
    channel: py:class:`chibi.circuit.chip.mcp3008.MCP3008_channel`
    voltage: float
        voltage de entrada del sensor ( default=5 )
    resistence: float
        resistencia del sensor ( default=1000 )
    """
    def __init__( self, channel, voltage=5, resistence=1000 ):
        self.channel = channel
        self.voltage = voltage
        self.resistence = resistence

    def read( self ):
        """
        lee los valores del sensor

        Returns
        =======
        dict
        """
        raise NotImplementedError

    def read_analogic_voltage( self ):
        return self.channel.read_analogic_voltage()

    def read_all_lectures( self ):
        analog, voltage = self.read_analogic_voltage()
        resistence = self.calculate_resistence( voltage )
        return analog, voltage, resistence, value

    def read_voltage( self ):
        return self.channel.read_voltage()

    def resistence( self ):
        voltage_lecture = self.read_voltage()
        return self.calculate_resistence( voltage_lecture )

    def calculate_resistence( self, voltage ):
        return self.resistence * ( ( self.voltage - voltage ) / voltage )


class MQ2( MQ ):
    """
    sensor de gas lp
    """
    name = "MQ-2"
    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_gas_lp( resistence )
        return {
            'gas_lp': {
                "unit": "ppm",
                "description":
                    "Gas licuado del petróleo ( Propano, Butano, ambos )",
                "chemical_formula": [ "C3H8", "C4H10" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_gas_lp( self ):
         return self.calcualte_gas_lp( self.resistence )

    def calculate_gas_lp( self, resistence ):
         return 8555 * pow( resistence / 5463, -1.74 )


class MQ3( MQ ):
    """
    sensor de alcohol
    """
    name = "MQ-3"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_alcohol( resistence )
        return {
            'alchohol': {
                "unit": "mg/L",
                "description": "Alcohol ( Benceno, Propano, Etanol, Metanol )",
                "formula_quimica": [ "C6H6", "C3H8", "C2H6O", "CH3OH" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_alcohol( self ):
        return self.calculate_alcohol( self.resistence )

    def calculate_alcohol( self, resistence ):
        return  1.108 * pow( resistence / 5463, -1.41 )


class MQ4( MQ ):
    """
    sensor de metano
    """
    name = "MQ-4"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_methane( resistence )
        return {
            'alchohol': {
                "unit": "ppm",
                "description": "Gas natural, Metano",
                "chemical_formula": [ "CH4" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_methane( self ):
        return self.calculate_methane( self.resistence )

    def calculate_methane( self, resistence ):
        return 6922 * pow( resistence / 5463, -1.91 )


class MQ6( MQ ):
    """
    sensor de propano
    """
    name = "MQ-6"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_propane( resistence )
        return {
            'propane': {
                "unit": "ppm",
                "description": "Propano",
                "chemical_formula": [ "C3H8" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_propane( self ):
        return self.calculate_propane( self.resistence )

    def calculate_propane( self, resistence ):
        return 2738 * pow( resistence / 5463, -1.81 )


class MQ7( MQ ):
    """
    sensor de monocido de carbono
    """
    name = "MQ-7"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_co( resistence )
        return {
            'propane': {
                "unit": "ppm",
                "description": "Monóxido de Carbono",
                "chemical_formula": [ "CO" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_co( self ):
        return self.calculate_propane( self.resistence )

    def calculate_co( self, resistence ):
        return 233.9 * pow( resistence / 5463, -1.40 )



class MQ8( MQ ):
    """
    sensor de hidrogeno
    """

    name = "MQ-8"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        value = self.calculate_hydrogen( resistence )
        return {
            'propane': {
                "unit": "ppm",
                "description": "Hidrógeno",
                "chemical_formula": [ "H2" ],
                "value": value,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            }
        }

    def read_hydrogen( self ):
        return self.calculate_hydrogen( self.resistence )

    def calculate_hydrogen( self, resistence ):
        return 1803 * pow( resistence / 5463, -0.66 )


class MQ135( MQ ):
    """
    sensor de de CO2, N2O y amoniaco
    """

    name = "MQ-135"

    def read( self ):
        analog, voltage, resistence = self.read_all_lectures()
        co2 = self.calculate_co2( resistence )
        n2o = self.calculate_n2o( resistence )
        ammonia = self.calculate_ammonia( resistence )

        return {
            'co2': {
                "unit": "ppm",
                "description": "Dióxido de carbono",
                "chemical_formula": [ "H2" ],
                "value": co2,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            },
            'n2o': {
                "unit": "ppm",
                "description":
                    "Óxidos de nitrógeno (Óxido nitroso, Óxido nítrico,"
                    "Anhídrido nitroso, Tetraóxido de nitrógeno,"
                    "Peróxido nítrico, Anhídrido nítrico)",
                "chemical_formula":
                    [ "NOx", "N2O", "NO", "N2O3", "N2O4", "NO2", "N2O5" ],
                "value": n2o,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            },
            'ammonia': {
                "unit": "ppm",
                "description": "Amoníaco",
                "chemical_formula": [ "NH3" ],
                "value": ammonia,
                "voltage": voltage,
                "resistence": resistence,
                "analog_value": analog,
                "sensor": self.name
            },
        }

    def read_co2( self ):
        return self.calculate_co2( self.resistence )

    def read_n2o( self ):
        return self.calculate_n2o( self.resistence )

    def read_ammonia( self ):
        return self.calculate_ammonia( self.resistence )

    def calculate_co2( self, resistence ):
        return 245 * pow( resistence / 5463, -2.26 )

    def calculate_n2o( self, resistence ):
        return 132.6 * pow( resistence / 5463, -2.74 )

    def calculate_ammonia( self, resistence ):
        return 161.7 * pow( resistence / 5463, -2.26 )
