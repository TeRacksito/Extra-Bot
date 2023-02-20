from os import system
import threading as th

task1 = "python main.py"
task2 = "python dashboard.py"

t1 = th.Thread(target=system, args=(task1, ))
t2 = th.Thread(target=system, args=(task2, ))
t1.start()
t2.start()