import numpy as np
import scipy
import time
import logging
import os
import sys
from datetime import datetime , timedelta
import csv

log = logging.getLogger("To File")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))



def downsample_to_proportion(rows, proportion):
    
    counter = 0.0
    last_counter = None
    results = []

    for row in rows:

        counter += proportion

        if int(counter) != last_counter:
            results.append(row)
            last_counter = int(counter)

    return results



def main():
    path = "/Users/Vikram/Dropbox/PowCapMobile_Experiments/"
    foundPath = ""
    
    log.info("Searching for files in path "+path)

    for r,d,f in os.walk(path):

        print f

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
    #latestFiles = [ file_list[-4] , file_list[-3], file_list[-2] , file_list[-1] ]

    for files in file_list:
        datetime_temp = datetime.strptime( files[6:12] + files[13:19] , '%y%m%d%H%M%S' )
        if datetime >= datetime_temp:
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
        foundPath = [ file_list[-2] , file_list[-1] ]
        log.info("Found data files: %s" % ' , ' .join(map(str,foundPath)))
        #checkFile()



    winSec = 1       #seconds to sample per window
    sample_rate = 1e6
    samp_rate = int(sample_rate/2)     #i and q channels are 1/2 complex rate
    num_channels = 2
    #startpoint = startSec * samp_rate   #set startpoint in file
    #endpoint = (endSec-startSec) * samp_rate       #set endpoint in file
    #fileName = foundPath                #set file path

    #print path+str(f)
    fileName = [ path+str(f[0]), path+str(f[0]) ]

    log.info("")
    log.info("Files found: %s" % f)
    log.info("")
    
    win_size = int( winSec * samp_rate )#set window size in file
    #note, self.samp_rate = 1 second of samples for each channel

    fileobj = open(fileName[0])
    fileobj2 = open(fileName[1])
    jcount = 0
    count = 0
    chunk_size = win_size*16 #reads winSec * samp_rate * 16 bits into file.
    header_array = ["V1", "C2", "V3", "C4"] 
    #out_array = [ [] ]

    size1 = os.fstat(fileobj.fileno()).st_size 
    size2 = os.fstat(fileobj2.fileno()).st_size 
    #log.info("Size of file1 is %s" % str(size1))
    #log.info("Size of file2 is %s" % str(size2))
    #log.info("Number of windows in file is: %s" % str(size1/chunk_size))
    if size1 == size2:
        wins_in_file = size1/chunk_size
    else:
        log.info("Warning, file size mismatch.")
        wins_in_file = size1/chunk_size

    #open file to begin writing CSV document
    pathSave = '/Users/Vikram/Dropbox/PowCapMobile_scripts/tools/other/' 
    with open(pathSave+'mains'+'.csv', 'w') as writeobj:
        log.info("Writing to: "+'mains.csv')
        write_gT = csv.writer(writeobj, 'excel-tab')

        #ctlimit = 2
        ctlimit = wins_in_file
        for count in range(0, ctlimit):

            if winSec == 1:
                log.info("Using a window size of %d second:" % winSec)
            else:
                log.info("Using a window size of %d seconds:" % winSec)

            log.info("Converting window %d of %d." % (count+1, ctlimit) )

            chunk = fileobj.read( chunk_size ) 
            chunk2 = fileobj2.read( chunk_size )
            Data = np.reshape( np.frombuffer(chunk, dtype=scipy.complex64), (-1, 1))#self.num_channels))
            Data2 = np.reshape( np.frombuffer(chunk2, dtype=scipy.complex64), (-1, 1))#self.num_channels))
            #print len(Data)
            #print len(Data2)

            #count = count+1 
            #count = 60
            
            #down1 = downsample_to_proportion(Data, .001)
            #down2 = downsample_to_proportion(Data2, .001)
            #print len(down1)
            #print len(down2)

            dat1 = []
            dat2 = []
            dat3 = []
            dat4 = []

            dat1 = downsample_to_proportion(Data.real, .001)
            dat2 = downsample_to_proportion(Data.imag, .001)
            dat3 = downsample_to_proportion(Data2.real, .001)
            dat4 = downsample_to_proportion(Data2.imag, .001)

            #print len(dat1)
            #print len(dat2)
            #print len(dat3)
            #print len(dat4)

            if count<1:
                dat1.insert(0, 'V1')
                dat2.insert(0, 'C2')
                dat3.insert(0, 'V3')
                dat4.insert(0, 'C4')

            #out_array = [dat1, dat2, dat3, dat4]
            out_array = [ [] ]
            
            for i in range(0, len(dat1)):
                temp_array = []

                temp_array.append(dat1[i])
                temp_array.append(dat2[i])
                temp_array.append(dat3[i])
                temp_array.append(dat4[i])
                    
                #temp_array = [dat1[i], dat2[i], dat3[i], dat4[i]]
                

                #out_array.append(temp_array)
                out_array.append([str(element).strip('[] ') for element in temp_array])

                #print len(out_array)

            #print len(out_array)
            #print len(out_array[0])

            #remove infuriating blank first index in out_array
            discard = out_array.pop(0)
            #log.info(discard)

            write_gT.writerows(out_array)
    
    raw_input("press any key to exit")

main()



