import os, psutil, sys
    
node = hou.pwd()
geo = node.geometry()

########################################################
pid = os.getpid()
py = psutil.Process(pid)
cpuUse = int(psutil.cpu_percent(interval=None))
memory = int(psutil.virtual_memory().total / (1024.0 ** 3))
memoryUse = int((py.memory_info()[0] >> 20))
mPercent = int((memoryUse*100) / memory)
frame = str(int(hou.frame()))
logfile = os.path.dirname(hou.evalParm('../Logs')) + "/" + "log." + str(`chs("../Wedge_Iterate")`).zfill(4) + ".log"
logfolder = os.path.dirname(logfile)
########################################################

########################################################
range = `chs("../f2")` - `chs("../f1")`
correctedStartValue = hou.frame() - `chs("../f1")`
percentage = int(((correctedStartValue * 100) / range))
########################################################

if not os.path.exists(logfolder):
        os.makedirs(logfolder)
       
#LOG FILE TO DEBUG
# WEDGE_ID,PID,FRAME,PERCENTAGE,cpuUSE,MEM,MEMUSE
log = str(`chs("../Wedge_Iterate")`).zfill(4)+","+ str(pid) + "," + frame + "," + str(percentage) + ","  + str(cpuUse) + "," + str(memory) + "," + str(memoryUse) + "\n"

#WRITE TO FILE
f = open(logfile,"w")
f.write(log)
f.close()
#WRITE TO FILE
