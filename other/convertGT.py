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
    #path = '/home/henry/Vikram_stuff/GroundTruth/EX2-GroundTruth/'
    path = '/Users/Vikram/Dropbox/PowCapMobile_Experiments/EX2-GroundTruth/'
    #path_save = '/home/henry/Vikram_stuff/GroundTruth/'
    path_save = '/Users/Vikram/Dropbox/PowCapMobile_Experiments/formatted_GT/'
    path_temp = '/home/henry/Vikram_stuff/tools/other/'
    panel_title = "ted5000_mainpanel" 
    #panel_title = "ted5000_subpanel"


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

                    if panel_title == "ted5000_mainpanel":
                        temp_list = [] 
                        temp_list.append(temp_row[0])
                        temp_list.append(temp_row[2])
                        temp_list.append(temp_row[4])
                        temp_list.append(temp_row[6])
                        temp_list.append(temp_row[8]) 
                    elif panel_title == "ted5000_subpanel":
                        temp_list = [] 
                        temp_list.append(temp_row[0])
                        temp_list.append(temp_row[2])
                        temp_list.append(temp_row[4])
                        temp_list.append(temp_row[5])
                        temp_list.append(temp_row[6]) 

                        temp_list.append(temp_row[8])
                        temp_list.append(temp_row[9])
                        temp_list.append(temp_row[10])

                        temp_list.append(temp_row[11])
                        temp_list.append(temp_row[12]) 
                        temp_list.append(temp_row[13]) 


                    dat_main.append([element.strip('[] ') for element in temp_list])
                    #dat_main.append(temp_list)

            #print len(dat_main)
            #print dat_main

        if panel_title == "ted5000_mainpanel":
            title_list = ['time', 'panel', 'voltage', 'real power', 'apparent power']
        elif panel_title == "ted5000_subpanel":
            title_list = ['time', 'panel', 'voltage1', 'voltage2', 'voltage3', 'real power1', 'real power2', 'real power3', 'apparent power1', 'apparent power2', 'apparent power3']

        dat_main[0] = title_list

        with open(path_save+date+'_'+panel_title+'.csv', 'w') as writeobj:
            log.info("Writing to: "+date+'_'+panel_title+'.csv')
            write_gT = csv.writer(writeobj, 'excel-tab')
            write_gT.writerows(dat_main)
            

            #for list_temp in dat_main:


main()
