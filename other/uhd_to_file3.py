
#!usr/bin/env python

from gnuradio import gr
from gnuradio import uhd
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import datetime
import tempfile

import sys
import time
import numpy
import logging
import os
import configobj


fconfig = file("uhd_to_file.ini")
config = configobj.ConfigObj(infile = fconfig)

log = logging.getLogger("To File")

log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))

class GetData_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option)
        parser.add_option("-a", "--args", type="string", default="",
                          help="UHD device address args , [default=%default]")
        parser.add_option("", "--spec", type="string", default=None,
                          help="Subdevice of UHD device where appropriate")
        parser.add_option("-A", "--antenna", type="string", default=None,
                          help="select Rx Antenna where appropriate")
        parser.add_option("-s", "--samp-rate", type="eng_float", default=1e6,
                          help="set sample rate (bandwidth) [default=%default]")
        parser.add_option("-f", "--freq", type="eng_float", default=None,
                          help="set frequency to FREQ", metavar="FREQ")
        parser.add_option("-g", "--gain", type="eng_float", default=None,
                          help="set gain in dB (default is midpoint)")
        parser.add_option("", "--avg-alpha", type="eng_float", default=1e-1,
                          help="Set fftsink averaging factor, default=[%default]")
        parser.add_option ("", "--averaging", action="store_true", default=False,
                          help="Enable fftsink averaging, default=[%default]")
        parser.add_option("", "--ref-scale", type="eng_float", default=1.0,
                          help="Set dBFS=0dB input value, default=[%default]")
        parser.add_option("--fft-size", type="int", default=1024,
                          help="Set number of FFT bins [default=%default]")
        parser.add_option("--fft-rate", type="int", default=30,
                          help="Set FFT update rate, [default=%default]")
        parser.add_option("-t","--timeout", type="int", default=3600,
                          help="Set length of data files (seconds), [default=%default]")
        parser.add_option("-p","--filePath", type="string", default="/media/PowCapRawData/testData",
			              help="Set path where you want data saved, [default=%default]")
        (options, args) = parser.parse_args()
        if len(args) != 0:
            parser.print_help()
            sys.exit(1)
        self.options = options
        self.show_debug_info = True

        self.u = uhd.usrp_source(device_addr=options.args,
                stream_args=uhd.stream_args('fc32', channels=range(2) ) )

        #filePath = "/media/PowCapRawData/testData"
        self.filePath = options.filePath
        if self.filePath == "distributed":
            self.filePathID = 1
            print "Drive List (for distributed storage):"
            for drive in config["drives"]:
                print drive
        else:
            self.filePathID = 0

        self.timeout = options.timeout

        #self.u.uhd_usrp_source.set_subdev_spec("A:RX1 A:RX2 B:RX1 B:RX2", 0)
        #self.u.uhd_usrp_source.set_subdev_spec(":A :B", 2)
                
        #self.u.set_subdev_spec(self.u.db(0) + self.u.db(1)
        #self.u.subdev = self.u.db(0) + self.u.db(1)

        # Set the subdevice spec
        #if(options.spec):
        #    self.u.set_subdev_spec(options.spec, 0)
        #self.u.set_subdev_spec("B:AB", 1)
        self.u.set_subdev_spec("A:AB B:AB")

        self.u.set_samp_rate(options.samp_rate)
        input_rate = self.u.get_samp_rate()

        # set initial values
        if options.gain is None:
            # if no gain was specified, use the mid-point in dB
            g = self.u.get_gain_range()
            options.gain = float(g.start()+g.stop())/2

        if options.freq is None:
            # if no freq was specified, use the mid-point
            r = self.u.get_freq_range()
            options.freq = float(r.start()+r.stop())/2
            
        #self.set_gain(options.gain)

        # Set the antenna
        if(options.antenna):
            self.u.set_antenna(options.antenna, 0)

        #mainsdata = gr.file_sink(gr.sizeof_gr_complex, "mains.dat")
        #fname = "/media/PowCapRawData/Wei_Wen_Data/mains_" + datetime.datetime.now().strftime("%yy%mm%H%M")+".dat"
        # "/media/Pandora/PowCapData/mains_"
        self.mainsdatas = [] 
  
        #self.di = gr.deinterleave(gr.sizeof_gr_complex)
        #self.connect(self.u, self.di)
        self.startStream()
  
    def getfname(self):
        date = datetime.datetime.now()

        #filePath = "/media/PowCapRawData/testData/mains_"

        #drives = ['Pandora', 'Box']
        drives = config["drives"]
        #print drives
        driveFound = False 

        if self.filePathID:
            log.info("Running distributed file storage.")
            for drive in drives:
                self.filePath = "/media/" + drive + "/PowCapData"
                log.info("(distributed) Checking drive " + drive + ".")
                if not ( self.getspace() ):
                    log.info("(distributed) Enough space, saving to: " + drive + ".")
                    fname1 = self.filePath + "/mains_" + \
                        date.strftime("%y%m%d_%H%M%S")+ "-chan_%d" % 1 + ".dat"
                    fname2 = self.filePath + "/mains_" + \
                        date.strftime("%y%m%d_%H%M%S")+ "-chan_%d" % 2 + ".dat"
                    driveFound = True
                    break
#                elif x == len(drives):
            if not driveFound:
                log.warning("(distributed) Not enough space in ALL LISTED drives!")
                sys.exit(1)
        elif not ( self.getspace() ):	
            fname1 = self.filePath + "/mains_" + \
                date.strftime("%y%m%d_%H%M%S")+ "-chan_%d" % 1 + ".dat"
            fname2 = self.filePath + "/mains_" + \
                date.strftime("%y%m%d_%H%M%S")+ "-chan_%d" % 2 + ".dat"

        log.debug("Write filename %s,%s" % (fname1,fname2))
        return (fname1,fname2)

    fname = property(getfname)
   
    def getspace(self):
        #returns the number of free Bytes on target drive
        s = os.statvfs(self.filePath)
        space = ( (s.f_bsize * s.f_bavail) / (1024*1024) )
        #switch out bavail for bfree to find free blocks for priviledged and unpriviledged users respectively
        log.info("Check space remaining in target drive: %dMB" % space)
        log.debug("preferred file system block size: %s" % str(s.f_bsize))
        log.debug("number of blocks available to non-super user: %s" % str(s.f_bavail))

        #required space (25MB/s required)
        spaceReq = 25 * self.timeout

        #Data at 1e6 sample rate consumes about 17MB/sec of space, this prevents overloading the HD (with buffer of 25MB/sec)
        if space < ( spaceReq ):
            log.warning("Not enough space in target drive!")
            return 1
        else:
            log.info("Target drive has enough space: (%sMB required)" % spaceReq)
            return 0 

    def startStream(self):
        fnames = self.fname
        for n in range(len(fnames)):
            mainsdata = gr.file_sink(gr.sizeof_gr_complex, fnames[n])
            self.mainsdatas.append(mainsdata)
            self.connect( (self.u, n), self.mainsdatas[n])
    
    def restart(self):
        #stops taking data and restarts the process       
        for n in range(len(self.mainsdatas)):
            self.disconnect( (self.u, n), self.mainsdatas[n])

        self.mainsdatas = []

        #check space in target drive
        #if not self.filePathID:
        #    if self.getspace():
        #        self.stop()
        #        sys.exit(1)


    def run(self, max_noutput_items=100000): 
        log.info("Starting capture")
        self.start(max_noutput_items)
        try:
            log.info("Going to sleep for %d secs" % self.timeout)
            time.sleep(self.timeout)
        except KeyboardInterrupt:
            self.stop()
            sys.exit(1)
        log.info("Capture complete, stopping capture")
        self.stop()
        log.info("Wait for capture to return")
        self.wait() 
        
        self.restart()

        self.startStream()     

        self.run()
    # new file here
    #self.run()


if __name__ == '__main__':
    try:
        GetData_top_block().run()
    except KeyboardInterrupt:
        log.info("Exiting")
