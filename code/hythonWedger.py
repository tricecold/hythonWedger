# coding: utf8
#Houdini Wedger 2.0 
#Author : Timucin OZGER 
#Date : 23.09.2018

# Importing all needed modules
import multiprocessing
from multiprocessing.pool import ThreadPool
import time, timeit, os , subprocess, resource, threading, sys, psutil
from multiprocessing import Process

#Clear Screen
os.system('clear') # on linux / os x

# Starting timer for Parent measurement
start_time = timeit.default_timer()

#Loads Variables from cmd.txt file
cmdFile = sys.argv[1]
lines = open(cmdFile).read().split('\n')

#Arguements Needed to run the script 
#lines[0] /home/tricecold/Work/tempHoudini/Fire.hiplc        ***File To Run
#lines[1] 10                                                 ***Batch Size
#lines[2] 2                                                  ***Max Simultanious Task Limit
#lines[3] 1                                                  ***Is it a Sim
#lines[4] 0                                                  ***Make Daily (Not Implemented)
#lines[5] /obj/pyro_import/FileCache_2.01/Wedge_Iterate      ***Changes Linked Value in Hython Session
#lines[6] /obj/pyro_import/FileCache_2.01/rop/cache          ***Cache Node
#lines[7] /obj/pyro_import/FileCache_2.01/rop/cache/f        ***Cache Frames Tuple

#My Variables
hou.hipFile.load(lines[0]) # loads the file
wedger = hou.parm(lines[5])
cache = hou.node(lines[6])
flipbook = hou.node(lines[10])
total_tasks =  int(lines[1]) # sets the task amount
max_number_processes = int(lines[2]) # defines the batch size
FileRange =  int(abs(hou.evalParmTuple(lines[7])[0] - hou.evalParmTuple(lines[7])[1]))
isSim = int(lines[3]) # simulate or cache flag
makeDaily = int(lines[4]) # make daily from a camera
logPath = lines[14]
progressFile = logPath + "progress.out"
asciiart = '''
██╗  ██╗ ██╗███████╗    ██╗    ██╗███████╗██████╗  ██████╗ ███████╗██████╗ 
██║  ██║███║╚════██║    ██║    ██║██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔══██╗
███████║╚██║    ██╔╝    ██║ █╗ ██║█████╗  ██║  ██║██║  ███╗█████╗  ██████╔╝
██╔══██║ ██║   ██╔╝     ██║███╗██║██╔══╝  ██║  ██║██║   ██║██╔══╝  ██╔══██╗
██║  ██║ ██║   ██║      ╚███╔███╔╝███████╗██████╔╝╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═╝   ╚═╝       ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
'''
logs = os.listdir(logPath)
for log in logs:
    if log.endswith(".log"):
        os.remove(os.path.join(logPath, log))

if os.path.isfile(progressFile):
    os.remove(progressFile)

class Progress(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            mylist = os.listdir(logPath)
            mylist.remove('cmd.txt')
            mylist= [logPath + s for s in mylist]
                        
            with open(progressFile, 'w') as outfile:
                for fname in sorted(mylist):
                    with open(fname) as (infile):
                        outfile.write(infile.read())    
                     
            f = open(progressFile)
            lines = f.readlines()
            
            print asciiart
            e = "░"
            print '\033[1m'+"⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ Process Summary ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"+'\33[0m'
            print ""
            print '\33[32m'+"File Name: " + hou.hipFile.name() + '\033[0m'
            print '\33[32m'+"Log Path:" + logPath + '\033[0m'
            print "Running " + '\33[36m'+str(total_tasks) +'\033[0m'+ " Tasks in Batches of " + '\33[36m'+str(max_number_processes) + '\033[0m'
            print e*75
            
            bar_length = 100/50
            usageLegend = ['\033[95m','\033[94m','\033[93m','\033[91m']
            percentages = [10,20,50,90,100]
            cpuUsage = psutil.cpu_percent()
            memUsage = psutil.virtual_memory()[2]
            usage = usageLegend[0]
            usageCPU = usageLegend[0]

            if memUsage > 20:
                usage = usageLegend[1]
            if memUsage > 50:
                usage = usageLegend[2]
            if memUsage > 90:
                usage = usageLegend[3]

            if cpuUsage > 20:
                usageCPU = usageLegend[1]
            if cpuUsage > 50:
                usageCPU = usageLegend[2]
            if cpuUsage > 90:
                usageCPU = usageLegend[3]

            
            print "CPU Utilization: " + usageCPU + str(cpuUsage) + "%" + '\33[0m'  + "  Memory Utilization: " + usage + str(memUsage)+ "%" + '\33[0m'                 
            print "" 
            timer = str(int(timeit.default_timer() - start_time))            
            for line in lines:
                member = line.split(',')
                current= int(member[3])
                ProgressBar =  '\33[37m'+"Progress:"+"["+((current/bar_length) * "■" + ("□" * (51 - ((current/bar_length)+1))) ) + "]" +member[3]+ "'%'"  
                
                print '\33[36m'+"Wedge:"+'\33[32m'+member[0] +"   "+'\33[36m'+" Frame:" +'\33[32m'+member[2]+"   "+'\33[36m'+" Mem Usage:" +'\33[32m' + member[6] ,   
                print "Elapsed Time: " + timer + " Loop Time: " + str(time.time()/1000)
                print ProgressBar
                
            
            #print  "Total RAM USAGE: " str(psutil.virtual_memory()) + "%"
            time.sleep(0.3)
            os.system('clear') # on linux / os x
            
            

if(isSim == 1):
    runProgress = Progress() 

#Split Frames for Wedging Non Simulation
def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq

taskList = split_seq(range(FileRange), total_tasks)

#Updates the wedge Value and runs the rop as simulation
def simRops(wedge=total_tasks):
    wedger.set(wedge)
    time.sleep(0.1)
    cache.render(verbose=False,)

#Updates the wedge Value and runs the rop in splitted frame ranges 
def cacheRops(wedge=total_tasks):
    startFrame = taskList[wedge][0] + int(lines[12])
    endFrame = taskList[wedge][-1] + int(lines[12])
    hou.parmTuple(lines[7])[0].set(startFrame)
    hou.parmTuple(lines[7])[1].set(endFrame)
    time.sleep(0.1)
    cache.render(verbose=False,)

#Makes a Flipbooks from Sequence
def dailyHoudini(wedge=total_tasks):
    wedger.set(wedge)
    daily = os.path.dirname(hou.evalParm(lines[8])) + "/"
    videos = lines[11]
    if not os.path.exists(videos):
        os.makedirs(videos)
    time.sleep(0.1)
    flipbook.render(verbose=False,)
    sframe = int(hou.evalParmTuple(lines[9])[0])
    mp4 = "ffmpeg -loglevel panic -y -start_number 0" + str(sframe) + " -framerate 25 -i " + daily + "%*.jpg -c:v libx264 -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -pix_fmt yuv420p " + videos + str(wedge) + ".mp4"
    p = subprocess.call(mp4,shell=True)

#Prints memory Usage
def current_mem_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.

#Multiprocess Functions Here    
if __name__ == '__main__':
    
    
    pool = multiprocessing.Pool(max_number_processes) #Defines the Batch Size
    
    if(isSim == 1):
        for wedge in range(0,total_tasks):
            pool.apply_async(simRops,args=(wedge,)) #Runs an Instance with each adjusted wedge Value
    
    if(isSim == 0):
        for wedge in range(0,total_tasks):
            pool.apply_async(cacheRops,args=(wedge,)) #Runs an Instance with each adjusted wedge Value

    if(makeDaily == 1):
        for wedge in range(0,total_tasks):
            pool.apply_async(dailyHoudini,args=(wedge,)) #Runs an Instance with each adjusted wedge Value

    
    pool.close() # After all threads started we close the pool
    pool.join() # And wait until all threads are done
print ""    
print("This Wedge Process ran %s seconds" % str(int(timeit.default_timer() - start_time)))
