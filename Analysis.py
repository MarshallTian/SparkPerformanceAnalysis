from MemAnalysis import *
from CpuAnalysis import *
from JvmAnalysis import *
from StageAnalysis import *
import os
#mstat = memStat("logs/MEM_hw001.log")
#mstat.parse()
#mstat.print_total()
#mstat.draw()

def getFileNames(dirpath, word, filenames):
    for i in os.listdir(dirpath):
        if i.find(word) == 0 and i[0] != '.':
            print i
            filenames.append(dirpath + "/" + i)

logdir = "logs/cc"
cfnames = []
jfnames = []

getFileNames(logdir, "VM", cfnames)
getFileNames(logdir, "JStat", jfnames)
#filenames = ["logs/VM_hw001.log", "logs/VM_hw114.log"]
cstats = allCpuStats(cfnames)
#cstats.parse()
#cstats.draw()
#cstat = cpuStat("logs/VM_hw001.log")
#cstat.parse()
# cstats.draw_all()
#cstats.draw_avg(title="cc")
jstats = allJvmStats(jfnames)
#jstats.draw_first("cc")
#jstats.draw_first()

slogdir = "logs/log"
sanames = []
getFileNames(slogdir, "", sanames)

sa = stageAnalysis(sanames)
sa.draw_total()




