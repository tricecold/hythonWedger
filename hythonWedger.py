#Houdini Wedger 2.0 
#Author : Timucin OZGER 
#Date : 23.09.2018

# Importing all needed modules
import multiprocessing
from multiprocessing.pool import ThreadPool
import time, timeit, os , subprocess, resource, threading, sys
from multiprocessing import Process

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
    cache.render(verbose=True,)

#Updates the wedge Value and runs the rop in splitted frame ranges 
def cacheRops(wedge=total_tasks):
    startFrame = taskList[wedge][0] + int(lines[12])
    endFrame = taskList[wedge][-1] + int(lines[12])
    hou.parmTuple(lines[7])[0].set(startFrame)
    hou.parmTuple(lines[7])[1].set(endFrame)
    time.sleep(0.1)
    cache.render(verbose=True,)

#Makes a Flipbooks from Sequence
def dailyHoudini(wedge=total_tasks):
    wedger.set(wedge)
    daily = os.path.dirname(hou.evalParm(lines[8])) + "/"
    videos = lines[11]
    if not os.path.exists(videos):
        os.makedirs(videos)
    time.sleep(0.1)
    flipbook.render(verbose=True,)
    sframe = int(hou.evalParmTuple(lines[9])[0])
    mp4 = "ffmpeg -start_number 0" + str(sframe) + " -framerate 25 -i " + daily + "%04d.jpg -c:v libx264 -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -pix_fmt yuv420p " + videos + str(wedge) + ".mp4"
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
    
print("Parent: this Process ran %s seconds" % str(timeit.default_timer() - start_time))
