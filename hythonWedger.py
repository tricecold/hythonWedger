# Importing all needed modules
import multiprocessing
from multiprocessing.pool import ThreadPool
import time, timeit
import os
import subprocess
import resource
import tqdm


#pid = str(os.getpid()) #get the pid for this task
#cmd = "psrecord " + pid + " --log oceanMistClose.txt --interval 10 --plot oceanMistClose.png " #builds the string to run
#p = subprocess.Popen(cmd,shell=True) #launches subprocess

# Starting timer for Parent measurement
start_time = timeit.default_timer()

#My Variables
hou.hipFile.load("/home/tricecold/pythonTest/HoudiniWedger/HoudiniWedger.hiplc")
wedger =   hou.parm('/obj/geo1/popnet/source_first_input/seed')
cache = hou.node('/out/cacheme')
total_tasks = 64 #Wedge Amount
max_number_processes = 16 #Batch Size
fileRange =  abs(hou.evalParmTuple('/out/cacheme/f')[0] - hou.evalParmTuple('/out/cacheme/f')[1])
target_dir = os.path.dirname(hou.evalParm('/out/cacheme/sopoutput')) + "/"
#My Variables



#Updates the wedge Value and runs the rop
def cacheHoudini(wedge=total_tasks):
    wedger.set(wedge)
    cache.render(verbose=False)
    print('\tWorker maximum memory usage: %.2f (mb)' % (current_mem_usage()))


#Might Come Handy
def files(target_dir):
    num = len([name for name in os.listdir(target_dir)])
    print num

#Prints memory Usage
def current_mem_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.




#Multiprocess Functions Here    
if __name__ == '__main__':
    
    pool = multiprocessing.Pool(max_number_processes) #Defines the Batch Size
    
    for wedge in range(0,total_tasks):
        pool.apply_async(cacheHoudini,args=(wedge,)) #RUns an Instance with each adjusted wedge Value
        
    #pool.apply_async(files,args=(target_dir,))    
    
    pool.close() # After all threads started we close the pool
    pool.join() # And wait until all threads are done
    del pool

print("Parent: this Process ran %s seconds" % str(timeit.default_timer() - start_time))


