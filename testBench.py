from PowCapTools import ParseData
from PowCapTools import FindFile

def main():
        fileName = '/home/henry/NeslStore/vikram/powcapData/Jason-Drive/mains_130313_030126-chan_1.dat'
        start_at_second = 1
        end_at_second = 20
        window_second = 200e-3
        sampRate = 1e6
        analysis = "plot" 
        
        #fileCat = '/home/henry/Vikram_stuff/NASPOW/PowCapData/'
        fileCat = '/home/henry/Vikram_stuff/NASPOW/Data1/EX2-PowCapData/'
        #fileCat = '/home/henry/NeslStore/vikram/powcapData/Jason-Drive/'
        #fileCat = '/home/henry/Vikram_stuff/RAW_DATA/'
        year = '13'
        month = '04'
        day = '20'
        datestr = year+month+day
        hour = '11'
        minute = '15'
        second = '05'
        timestr = hour+minute+second
        f_search =  FindFile(fileCat, datestr, timestr)

        fileCatPath = [ fileCat + f_search.foundPath[0], fileCat + f_search.foundPath[1] ]
        #fileCatPath = [ fileCat + f_search.latestFiles[0], fileCat + f_search.latestFiles[1] ]
        
        p = ParseData(fileCatPath, 0, 20, window_second, sampRate)
        #p = ParseData(fileCatPath, 0, 20, window_second, sampRate, analysis)
        
        #p = ParseData(fileName, start_at_second, end_at_second, window_second)



main()
