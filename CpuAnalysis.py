import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np

class allCpuStats:
    def __init__(self, filenames):
        self.filenames = filenames
        self.cpustats = []
        self.parse()

    def parse(self):
        for filename in self.filenames:
            cstat = cpuStat(filename)
            #cstat.parse()
            self.cpustats.append(cstat)

    @staticmethod
    def draw(cpu_stat, myplt, title="default"):
        timeArray = []
        for i in range(0, len(cpu_stat.user)):
            timeArray.append(i * 2)
            #cpu_stat.sys[i] += cpu_stat.user[i]
            #cpu_stat.wait[i] += cpu_stat.sys[i]

        font = {
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }

        myplt.xlabel("Time (s)", fontdict=font)
        myplt.ylabel("CPU Usage (%)", fontdict=font)
        #myplt.title(title, fontdict=font)
        myplt.ylim(0, 100)
        myplt.xlim(0, timeArray[-1])
        # plt.plot(timeArray, self.used, 'b*')
        #myplt.bar(timeArray, cpu_stat.user, color="blue", label="user")
        red_patch = mpatches.Patch(color="red", label="sys")
        mycolors = ['#336666','#99CCCC','#CCFFFF']
        myplt.stackplot(timeArray, cpu_stat.user, cpu_stat.sys, cpu_stat.wait, colors=mycolors)
        #myplt.hist(cpu_stat.wait, len(timeArray), histtype='stepfilled')
        #myplt.fill_between(timeArray, 0, cpu_stat.wait, facecolor="yellow")
        #myplt.fill_between(timeArray, 0, cpu_stat.sys, facecolor="red")
        #myplt.fill_between(timeArray, 0, cpu_stat.user)
        #myplt.grid(True)
        #myplt.legend((user, ), ("USER", ), 'upper left')
        p_user = mpatches.Rectangle((0, 0), 1, 1, fc="#336666")
        p_sys = mpatches.Rectangle((0, 0), 1, 1, fc="#99CCCC")
        p_wait = mpatches.Rectangle((0, 0), 1, 1, fc="#CCFFFF")
        myplt.legend([p_user, p_sys, p_wait], ["USER", "SYS", "WAIT"])
        myplt.savefig("/Users/XinhuiTian/newwork/benchmark/TPDS/TPDS-BigDataBench-2015/figures/%s-cpu.ps" % title)

        #myplt.show()

    def draw_all(self):
        for i in range(0, len(self.cpustats)):
            ax = plt.subplot(2, len(self.cpustats)/2, i)
            plt.sca(ax)
            self.draw(self.cpustats[i], plt)

        plt.show()

    def draw_avg(self, title="default"):
        user_avg = self.cpustats[0].user
        sys_avg = self.cpustats[0].sys
        wait_avg = self.cpustats[0].wait
        for i in range(1, len(self.cpustats)):
            user_avg = [x + y for (x, y) in zip(user_avg, self.cpustats[i].user)]
            sys_avg = [x + y for (x, y) in zip(sys_avg, self.cpustats[i].sys)]
            wait_avg = [x + y for (x, y) in zip(wait_avg, self.cpustats[i].wait)]
            #print user_avg

        #print user_avg

        user_avg = [user_avg[i] / len(self.cpustats) for i in range(0, len(user_avg))]
        sys_avg = [sys_avg[i] / len(self.cpustats) for i in range(0, len(sys_avg))]
        wait_avg = [wait_avg[i] / len(self.cpustats) for i in range(0, len(wait_avg))]

        #print user_avg

        stat_avg = cpuStat(None, user_avg, sys_avg, wait_avg)
        self.draw(stat_avg, plt, title=title)
        plt.show()

class cpuStat:
    def __init__(self, filename, user=None, sys=None, wait=None):
        self.filename = filename
        if user is None and sys is None and wait is None:
            self.user = []
            self.sys = []
            self.wait = []
        else:
            self.user = user
            self.sys = sys
            self.wait = wait

        if filename is not None:
            self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if lines[0] != "procs":
            print "Error cpu stat file"
            exit(1)

        f.seek(0)
        for line in f:
            stats = line.split()
            if len(stats) == 17 and stats[0] != "r":
                self.user.append(int(stats[12]))
                self.sys.append(int(stats[13]))

                self.wait.append(int(stats[15]))








