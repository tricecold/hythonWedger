def readValues(kwargs):
    import subprocess, os
    #####################################################
    
    node = kwargs['node']
    batchsize = node.evalParm('Batch_Size')
    taskLimit = node.evalParm('Parallel_Task_Limit')
    taskIterate = node.path() + "/Wedge_Iterate"
    filename = hou.hipFile.path()
    filepath = os.path.dirname(filename) + "/"
    logPath = node.evalParm('Logs')  
    cmdFile = node.evalParm('Logs') + "cmd.txt"
    sf = int(node.evalParm('f1'))
    ef = int(node.evalParm('f2'))
    sim = hou.node('rop/cache')
    isSim = node.evalParm('initsim')
    makeDaily = node.evalParm('Make_Daily')
    rop = node.path() + "/rop/cache"
    ropFrame = rop + "/f"
    Flipbook = node.path() + "/rop/Flipbook"
    FlipbookOutput = node.path() + "/rop/Flipbook/picture"
    FlipbookFrame = node.path() + "/rop/Flipbook/f"
    VideoOutput = node.evalParm('Videos')
    script = node.evalParm('scriptPath')
    
    #####################################################
    
    print ""
    print node
    print node.path()
    print "Command Variables"
    print "File Path   : " + filepath
    print "File Name   : " + filename
    print "Wedger      : " + str(taskIterate)
    print "Log Path    : " + logPath
    print "CMD File    : " + cmdFile
    print "Batch Size  : " + str(batchsize)
    print "Start Frame : " + str(sf)
    print "End Frame   : " + str(ef)
    print "Simulate    : " + str(isSim)
    print "ropNode     : " + rop
    print "FlipBook    : " + str(Flipbook)
    print "FlipBookOut : " + str(FlipbookOutput)
    print "FlipBookFR  : " + str(FlipbookFrame)
    print "Videos      : " + str(VideoOutput)
    print "Script      : " + script
    
    #####################################################
    
    arguements = filename + "\n" + str(batchsize) + "\n" + str(taskLimit) + "\n" + str(isSim)  + "\n" + str(makeDaily) + "\n" + str(taskIterate) + "\n" + str(rop) + "\n" + str(ropFrame) + "\n" + str(FlipbookOutput) + "\n" + str(FlipbookFrame) + "\n" + str(Flipbook) + "\n" + str(VideoOutput) + "\n" + str(sf) + "\n" + str(ef)  + "\n" + logPath
    task = "hython " + script + " " + cmdFile
    print task
    
    #####################################################
    
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    a = file(cmdFile, 'w')
    a.write(arguements)
    a.close
    
    p = subprocess.Popen(task,shell=True) #launches subprocess
