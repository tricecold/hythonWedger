#Houdini Wedger 2.0 
#Author : Timucin OZGER 
#Date : 23.09.2018

# Importing all needed modules
import multiprocessing
from multiprocessing.pool import ThreadPool
import time, timeit, os , subprocess, resource, threading, sys
from multiprocessing import Process

#pid = str(os.getpid()) #get the pid for this task
#cmd = "psrecord " + pid + " --log oceanFlips.txt --interval 10 --plot oceanFlips.png " #builds the string to run
#p = subprocess.Popen(cmd,shell=True) #launches subprocess

# Starting timer for Parent measurement
start_time = timeit.default_timer()

#My Variables
hou.hipFile.load("/home/tricecold/Work/HoudiniProjects/Masters_of_the_Sea_H17/3_Ocean_Flip_v1.hiplc")
wedger = hou.parm('/obj/OCEAN_TANK/Wedger/wedge')
cache = hou.node('/out/OUT_FLIP_SIM')
flipbook = hou.node('/out/Cam10')
total_tasks =  1 #Wedge Amount
max_number_processes = 1 #Batch Size
#FileRange =  abs(hou.evalParmTuple('/out/cacheme/f')[0] - hou.evalParmTuple('/out/cacheme/f')[1])
#target_dir = os.path.dirname(hou.evalParm('/out/cacheme/sopoutput')) + "/"
#totals = FileRange * total_tasks
#My Variables

#Updates the wedge Value and runs the rop
def cacheHoudini(wedge=total_tasks):
    wedger.set(wedge)
    time.sleep(0.1)
    cache.render(verbose=True,)
    #print('\tWorker maximum memory usage: %.2f (mb)' % (current_mem_usage()))

#Updates the wedge Value and runs the rop
def dailyHoudini(wedge=total_tasks):
    wedger.set(wedge)
    daily = os.path.dirname(hou.evalParm('/out/Cam10/picture')) + "/"
    #print daily
    time.sleep(0.1)
    flipbook.render(verbose=True,)
    sframe = int(hou.evalParmTuple('/out/Cam10/f')[0])
    #print sframe
    cmd = "ffmpeg -start_number 0" + str(sframe) + " -framerate 25 -i " + daily + "%04d.jpg -c:v libx264 -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -pix_fmt yuv420p " + daily + "Daily.mp4"
    #print cmd
    p = subprocess.call(cmd,shell=True)
    #print('\tWorker maximum memory usage: %.2f (mb)' % (current_mem_usage()))

#Prints memory Usage
def current_mem_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.

#Multiprocess Functions Here    
if __name__ == '__main__':
    
    pool = multiprocessing.Pool(max_number_processes) #Defines the Batch Size
    
  
    for wedge in range(0,total_tasks):
        pool.apply_async(cacheHoudini,args=(wedge,)) #Runs an Instance with each adjusted wedge Value
    
    for wedge in range(0,total_tasks):
        pool.apply_async(dailyHoudini,args=(wedge,)) #Runs an Instance with each adjusted wedge Value
    

    pool.close() # After all threads started we close the pool
    pool.join() # And wait until all threads are done
    
print("Parent: this Process ran %s seconds" % str(timeit.default_timer() - start_time))


