![alt text](https://github.com/tricecold/hythonWedger/blob/master/wedger2.jpg)


# hythonWedger
Houdini Wedger 2.0
Author :   Timucin OZGER
Date   :   23.09.2018


This little code wedges a houdini file using multiprocessing.pool . Works especially best with single threaded tasks running in parralel.

I also added functionality to make flipbooks and MP4 out of it.

Initial development stage is to have a strong hython base, then to make an HDA out of it.
Some tests showed that around additional %30 optimized gains were made if POP simulations were run in parralel. I beleive the results will scale much better with non-mnultithreading friendly tasks, such as Solid Solver or Bullet Solver.

This HDA creates a txt file to be run with the main file.

Under the HIP File Folder It creates 

HIPFILE
    geo
       WedgerSOPNAME
                   v_0 (version of the cache)
                      cmd (this is the command that main python file processes)
                      videos
                      wedge_n#Multiprocess Functions Here    

82

if __name__ == '__main__':

83

    

84

    pool = multiprocessing.Pool(max_number_processes) #Defines the Batch Size

85

    

86

    if(isSim == 1):

87

        for wedge in range(0,total_tasks):

88

            pool.apply_async(simRops,args=(wedge,)) #Runs an Instance with each adjusted wedge Value

89

    

90

    if(isSim == 0):

91

        for wedge in range(0,total_tasks):

92

            pool.apply_async(cacheRops,args=(wedge,)) #Runs an Instance with each adjusted wedge Value

93

​

94

    if(makeDaily == 1):

95

        for wedge in range(0,total_tasks):

96

            pool.apply_async(dailyHoudini,args=(wedge,)) #Runs an Instance with each adjusted wedge Value

97

​

98

    

99

    pool.close() # After all threads started we close the pool

100

    pool.join() # And wait until all threads are done

101

    

102

print("Parent: this Process ran %s seconds" % str(timeit.default_timer() - start_time)) (Where The BGEOS are stored)
                            Flipbook (Corresponding jpg files)
             
USAGE
Load the HDA in your scene
Use it instead of a file Cache
Play around batch size and max tasks to optimize performance based on your needs.

TO DO
1) Add fail safes for memory usage , if possible fail pools that go over a limit of memory use and retry once more pools are complete.
2) Autosave a copy of hip file to run instead of master file
3) Design a UI or a html server that can follow up the running tasks with some kind of progress report
4) Create some benchmarks.
6) Create proper versioning tools that is linked to scene file or project





