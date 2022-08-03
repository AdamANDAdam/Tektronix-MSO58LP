import pyvisa as visa
import csv
#open scope
rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x0529::C011531::INSTR')
print(scope.query('*idn?'))
scope.timeout = 1000

scope.write('*rst') # reset
scope.query('*opc?') # sync
scope.write('autoset EXECUTE') # autoset


frameSize = scope.query('horizontal:acqlength?') #get frame length
numFrames = 2
scope.write('horizontal:fastframe:count {}'.format(numFrames)) #set number of frames
scope.write('horizontal:fastframe:state 1') #turn on fast frame

#acquire a set of frames and then stop acquiring
scope.write('acquire:state 0')
scope.write('acquire:stopafter SEQUENCE')
scope.write('acquire:state 1')
scope.query('*opc?')

scope.write('save:waveform:fileformat SPREADSHEETCsv') #set format before data start/stop
scope.write('save:waveform:data:start 1') #ensure data range is good
scope.write('save:waveform:data:stop {}'.format(frameSize)) #ensure data range is good

for i in range(1, numFrames+1):

    scope.write('data:framestart {}'.format(i)) #controls starting frame
    scope.write('data:framestop {}'.format(i)) #controls ending frame
    filename = r'E:\MSO58LP\frame{}.csv'.format(i)
    scope.write('save:waveform CH1,"{}"'.format(filename))
    scope.query('*opc?')

print('End')