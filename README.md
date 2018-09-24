# hythonWedger
#Houdini Wedger 2.0
#Author :   Timucin OZGER
#Date   :   23.09.2018

This little code wedges a houdini file using multiprocessing.pool . Works especially best with single threadd tasks runinng in parralel.

Initial development stage is to have a strong hython base, that can run which have been ashieved.

TO DO

1) Add fail safes for memory usage , if possible fail pools that go over a limit of memory use and retry once more pools are complete.
2) Develop an OTL around the Code that can launch processes from Houdini with a new filecache OTL that has wedging controls
3) Design a UI or a html server that can follow up the running tasks with some kind of progress report
4) Create some benchmarks.

Initial testing showed that around additional %30 optimized gains were made if POP simulations were run in parralel. I beleive the results will scale much better with non-mnultithreading friendly tasks, sucj as Solid Solver or Bullet Solver.




