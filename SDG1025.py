import usbtmc
from time import sleep

class OutputWave(object):
    WAVE_SINE = 'SINE'
    WAVE_SQUARE = 'SQUARE'
    WAVE_RAMP = 'RAMP'
    WAVE_PULSE = 'PULSE'
    WAVE_NOISE = 'NOISE'

class SDG1025(object):
    def __init__(self, *args, **kwargs):
        self._debug = kwargs['debug'] if 'debug' in kwargs else None
        # discover the SDG1025 and connect automatically
        devices = usbtmc.list_resources()
        if not devices:
            print('Could not find an SDG1025 device!\n'
            'Make sure the USB cable is connected and the device powered on.')
            quit()
        
        self.__debug('Connecting to the first available device: %s' % devices[0])
        self._sdg = usbtmc.Instrument(devices[0])
        self._sdg.clear()
        dev = self._sdg.ask('*IDN?')
        if not dev:
            print('Could not connect to device: %s' % devices[0])
            quit()
        self._sdg.clear()
        self.__debug('Connected to: %s' % dev.split(',')[2])

    def isConnected(self):
        resp = self.getIDN()
        return(False if not resp else True)

    def getIDN(self):
        self._sdg.clear()
        return(self._sdg.ask('*IDN?'))

    def getChannel(self, ch):
        self._sdg.clear()
        self.__debug('Get channel: %s' % ch)
        cmd = 'C{}:BSWV ?'.format(ch)
        return(self._sdg.ask(cmd))

    def setChannel(self, ch, wave, freq, amplitude, offset):
        cmd = 'C{}:BSWV WVTP,{},FRQ,{},AMP,{},OFST,{}V'.format(
            ch, wave, freq, amplitude, offset
        )
        self.__debug('setChannel: %s' % cmd)
        self._sdg.write(cmd)

    def setChannelFreq(self, ch, freq):
        cmd = 'C{}:BSWV FRQ,{}'.format(ch, freq)
        self.__debug('setChannelFreq: %s' % cmd)
        self._sdg.write(cmd)

    def setChannelWave(self, ch, wave):
        cmd = 'C{}:BSWV WVTP,{}'.format(ch, wave)
        self.__debug('setChannelWave: %s' % cmd)
        self._sdg.write(cmd)

    def setChannelAmplitude(self, ch, amplitude):
        cmd = 'C{}:BSWV AMP,{}'.format(ch, amplitude)
        self.__debug('setChannelAmplitude: %s' % cmd)
        self._sdg.write(cmd)

    def setChannelOffset(self, ch, offset):
        cmd = 'C{}:BSWV OFST,{}V'.format(ch, offset)
        self.__debug('setChannelOffset: %s' % cmd)
        self._sdg.write(cmd)

    def enableChannel(self, ch):
        self.__debug('Enable channel %s' % ch)
        cmd = 'C{}:OUTP ON'.format(ch)
        self._sdg.write(cmd)

    def disableChannel(self, ch):
        self.__debug('Disable channel %s' % ch)
        cmd = 'C{}:OUTP OFF'.format(ch)
        self._sdg.write(cmd)

    def __debug(self, text):
        if self._debug:
            print('[SDG1025]: %s' % text)


if __name__ == '__main__':
    sdg1025 = SDG1025(debug=1)
    if not sdg1025.isConnected:
        print('Couldn\'t connect to SDG1025!')
        quit()
#     # print(sdg1025.getIDN())
#     # sdg1025.setChannel(1, OutputWave.WAVE_SINE, 10000, 3.3, 0)
#     # sdg1025.setChannel(2, OutputWave.WAVE_SQUARE, 100000, 4.687, 0)
    print(sdg1025.getChannel(1))
    print(sdg1025.getChannel(2))
#     # sdg1025.enableChannel(1)
#     # sdg1025.enableChannel(2)
#     # sleep(3)
#     # sdg1025.disableChannel(1)
#     # sdg1025.disableChannel(2)