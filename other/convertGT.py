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
import csv

#plt.ion()

#fileName = raw_input('Enter file name/path:')
#fileName = '/home/henry/Vikram_stuff/data.dat'
#fileName = '/home/henry/NeslStore/vikram/powcapData/Jason-Drive/mains_130313_030126-chan_1.dat'

#win_size = 1e5 #sets window size to 200ms or 1/5 of 5e5 (1 second at 500Ks/s)
#startpoint = 10 * 5 * (win_size) # startpoint = 10 * (1 second window)
#endpoint = int(1e6)
#num_channels = 2

#fig = plt.figure()
#sub = fig.add_subplot(111)

log = logging.getLogger("To File")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))


def main():

    date = ''   #'2013_04_21'
    file_date = 'home3747_E_'+date+'.txt'
    path = '/home/henry/Vikram_stuff/GroundTruth/EX2-GroundTruth/'
    path_save = '/home/henry/Vikram_stuff/GroundTruth/'
    path_temp = '/home/henry/Vikram_stuff/tools/other/'
    panel_title = "ted5000_mainpanel" 


    for r,d,f in os.walk(path):
        file_list = f

    log.info("Found files: ")
    for f in file_list:
        log.info(f)
    
    if len(date)>0:
        file_list = [k for k in file_list if date in k]

    for file_extract in file_list:

        log.info("Converting file ''"+file_extract+"'' to tabspace format.")
        date = ""+file_extract[13:15]+file_extract[16:18]+file_extract[19:21]

        with open(path+file_extract) as csvobj:
            gT = csv.reader(csvobj, delimiter=",")
            #print gT.next()
            dat_main = [ [] ]

            for row in gT:
                if panel_title in row[2]:
                    temp_row = row
                    for piece in temp_row:
                        piece.replace(" ", "")
                        piece.replace("[", "")
                        piece.replace("]", "")

                    temp_list = [] 
                    temp_list.append(temp_row[0])
                    temp_list.append(temp_row[2])
                    temp_list.append(temp_row[4])
                    temp_list.append(temp_row[6])
                    temp_list.append(temp_row[8]) 

                    dat_main.append([element.strip('[] ') for element in temp_list])
                    #dat_main.append(temp_list)

            #print len(dat_main)
            #print dat_main

        title_list = ['time', 'panel', 'voltage', 'real power', 'apparent power']
        dat_main[0] = title_list

        with open(path_save+date+'_'+panel_title+'.csv', 'w') as writeobj:
            log.info("Writing to: "+date+'_'+panel_title+'.csv')
            write_gT = csv.writer(writeobj, 'excel-tab')
            write_gT.writerows(dat_main)
            

            #for list_temp in dat_main:


main()

'''
class FindFile():
    def __init__(self, folderPath, date, time):

        
        self.path = folderPath
        self.date = date
        self.time = time
        self.datetime = datetime.strptime( self.date + self.time , '%y%m%d%H%M%S' )

        log.info("Searching for file containing data at...")
        log.info(self.datetime)
        log.info("...in path: "+self.path)

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
'''

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
