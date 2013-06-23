from gnuradio import gr  
import numpy as np
import matplotlib.pyplot as plt
import scipy
from StringIO import StringIO
import time
import logging
import os
import sys
from datetime import datetime , timedelta

log = logging.getLogger("To File")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

def main():
    
    log.info("Searching for files in path "+path)

    for r,d,f in os.walk(self.path):

        #print f

        file_list = f
        
        #we only want to look at given path and not any deeper dirs
        break

    if len(file_list) == 0:
        log.warning("No files found in given path!")
    else:
        log.info("%d files found in path" % len(file_list))
        #check for files with word "mains" in them
        file_list = [k for k in file_list if 'mains' in k]

    #check for files with required start date
    #file_list = [k for k in file_list if self.date in k]

    found_list = []

    file_list.sort()

    #latest files for quick look
    self.latestFiles = [ file_list[-4] , file_list[-3], file_list[-2] , file_list[-1] ]

    for files in file_list:
        datetime_temp = datetime.strptime( files[6:12] + files[13:19] , '%y%m%d%H%M%S' )
        if self.datetime >= datetime_temp:
            found_list.append(files)
            #found_list.append( [k for k in f if files[6:18] in k] )
            #file_list.sort() 

    #print found_list
    #file_list = [k for k in f if found_list in k]
    file_list = found_list
    file_list.sort()
    #print file_list
    #print len(found_list)

    if len(file_list) == 0:
        log.warning("No file found with requested date")
    else:
        self.foundPath = [ file_list[-2] , file_list[-1] ]
        log.info("Found data files: %s" % ' , ' .join(map(str,self.foundPath)))
        self.checkFile()


    winSec = 60
    sample_rate = 1e6
    samp_rate = int(sample_rate/2)     #i and q channels are 1/2 complex rate
    num_channels = 2
    startpoint = startSec * samp_rate   #set startpoint in file
    endpoint = (endSec-startSec) * samp_rate       #set endpoint in file
    fileName = filePath                #set file path
    win_size = int( winSec * samp_rate )#set window size in file
    #note, self.samp_rate = 1 second of samples for each channel

    fileobj = open(fileName[0])
    fileobj2 = open(fileName[1])
    jcount = 0
    count = 0
    chunk_size = self.win_size*16 #reads 200K steps into file = 200ms

    while count < self.endpoint/self.win_size:
        chunk = fileobj.read( chunk_size ) 
        chunk2 = fileobj2.read( chunk_size )
        Data = np.reshape( np.frombuffer(chunk, dtype=scipy.complex64), (-1, 1))#self.num_channels))
        Data2 = np.reshape( np.frombuffer(chunk2, dtype=scipy.complex64), (-1, 1))#self.num_channels))
        #print Data

        count = count+1 

    raw_input("press any key to exit")


def chunk(self, fObject):
    while True:
        segment = fObject.read( int(self.win_size*16) )
        yield segment


def scope_data(self, Data, Data2):
    #dat1 = Data.real[:,0]
    dat1 = Data.real
    dat2 = Data.imag
    #dat3 = np.fft.fft(Data)
    dat3 = Data2.real
    dat4 = Data2.imag
    #dat2 = Data.imag[:,0]
    if not hasattr(self, "run_once"):
        self.run_once = True
        x = np.arange( 0, len(dat1) )
        self.line = self.sub.plot(x, dat1)[0]
        self.line2 = self.sub2.plot(x, dat2)[0]
        self.line3 = self.sub3.plot(x, dat3)[0]
        self.line4 = self.sub4.plot(x, dat4)[0]
        self.sub2.set_title("Line1 Current (C4)")
        self.sub.set_title("Line1 Voltage (V3)")
        self.sub4.set_title("Line2 Current (C2)")
        self.sub3.set_title("Line2 Voltage (V1)")
        #plt.show()
    #Data = scipy.fromfile(open(data_piece), dtype=scipy.complex64)


    log.info( "c_binary length: %d" % len(Data) )
    log.info( "real bin length: %d" % len(dat1) )
    log.info( "imag bin length: %d" % len(dat2) )

    #dat1 = Data.real
    #dat2 = Data.imag

    x = np.arange(0, len(Data))
    #print len(x)
    #import pdb
    #pdb.set_trace()
    self.line.set_data(x, dat1 )
    self.line2.set_data(x, dat2 )
    self.line3.set_data(x, dat3 )
    self.line4.set_data(x, dat4 )
    '''
    self.sub.relim()
    self.sub.autoscale_view(True, True, True)
    self.sub2.relim()
    self.sub2.autoscale_view(True, True, True)
    self.sub3.relim()
    self.sub3.autoscale_view(True, True, True)
    self.sub4.relim()
    self.sub4.autoscale_view(True, True, True)
    '''
    self.fig.canvas.draw()
    #plt.plot(Data[1:self.win_size])
    #plt.plot(dat1[1:self.win_size])
    #plt.plot(dat2[1:self.win_size])
    #raw_input('pause')
    #plt.show()
    #raw_input('press any key')

main()

'''
if __name__ == '__main__':
    try:
        fileName = '/home/henry/NeslStore/vikram/powcapData/Jason-Drive/mains_130313_030126-chan_1.dat'
        start_at_second = 10
        end_at_second = 15
        window_second = 200e-3
        p = ParseData(fileName, start_at_second, end_at_second, window_second)
    except KeyboardInterrupt:
        log.info("Exiting")
'''
