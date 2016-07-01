import matplotlib.pyplot as plt
import math

class allJvmStats:
    def __init__(self, filenames):
        self.filenames = filenames
        self.jstats = []
        self.parse()

    def parse(self):
        for filename in self.filenames:
            jstat = jvmStat(filename)
            #cstat.parse()
            self.jstats.append(jstat)

    @staticmethod
    def draw(jvm_stat, myplt):
        timeArray = []
        maxMem = 0.0
        for i in range(0, len(jvm_stat.ec)):
            timeArray.append(i * 2)
            if jvm_stat.ec[i] > maxMem:
                maxMem = jvm_stat.ec[i]
            if jvm_stat.oc[i] > maxMem:
                maxMem = jvm_stat.oc[i]

        print maxMem

        font = {
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }

        myplt.xlabel("Time (s)", fontdict=font)
        myplt.ylabel("Memory Size (GB)", fontdict=font)
        #myplt.set_xlabel("Time", fontsize=10)
        myplt.ylim(0, maxMem + 2)
        myplt.xlim(0, timeArray[-1])
        mark_length = math.log10(len(timeArray)) ** 3

        # plt.plot(timeArray, self.used, 'b*')
        myplt.plot(timeArray, jvm_stat.ec, "-", color="#003300", label="ec", linewidth=1.5, marker="^", markersize=9,
                   markevery=mark_length)
        myplt.plot(timeArray, jvm_stat.eu, "-", color="#336666", label="eu", linewidth=1.5)
        myplt.plot(timeArray, jvm_stat.oc, "-", color="#cc0033", label="oc", linewidth=1.5, marker="d", markersize=6,
                   markevery=mark_length)
        myplt.plot(timeArray, jvm_stat.ou, "-", color="#990033", label="ou", linewidth=1.5, marker="*", markersize=9,
                   markevery=mark_length)
        myplt.grid(True)
        #myplt.plot(timeArray, self.pc, "r", color="green", label="pc")
        #myplt.plot(timeArray, self.pu, "r", color="black", label="pu")

        myplt.legend()
        #myplt.show()

    def draw_first(self, title="default"):
        font = {
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }
        self.draw(self.jstats[0], plt)
        #plt.title(title, fontdict=font)
        plt.savefig("/Users/XinhuiTian/newwork/benchmark/TPDS/TPDS-BigDataBench-2015/figures/%s-jvm.ps" % title)
        plt.show()

    def draw_all(self):
        for i in range(0, len(self.jstats)):
            ax = plt.subplot(3, len(self.jstats)/3, i)
            plt.sca(ax)
            self.draw(self.jstats[i], plt)

        plt.show()

    def draw_avg(self):
        ec_avg = self.jstats[0].ec
        eu_avg = self.jstats[0].eu
        oc_avg = self.jstats[0].oc
        ou_avg = self.jstats[0].ou
        pc_avg = self.jstats[0].pc
        pu_avg = self.jstats[0].pu

        for i in range(1, len(self.jstats)):
            ec_avg = [x + y for (x, y) in zip(ec_avg, self.jstats[i].ec)]
            eu_avg = [x + y for (x, y) in zip(eu_avg, self.jstats[i].eu)]
            oc_avg = [x + y for (x, y) in zip(oc_avg, self.jstats[i].oc)]
            ou_avg = [x + y for (x, y) in zip(ou_avg, self.jstats[i].ou)]
            pc_avg = [x + y for (x, y) in zip(pc_avg, self.jstats[i].pc)]
            pu_avg = [x + y for (x, y) in zip(pu_avg, self.jstats[i].pu)]

        ec_avg = [ec_avg[i] / len(self.jstats) for i in range(0, len(ec_avg))]
        eu_avg = [eu_avg[i] / len(self.jstats) for i in range(0, len(eu_avg))]
        oc_avg = [oc_avg[i] / len(self.jstats) for i in range(0, len(oc_avg))]
        ou_avg = [ou_avg[i] / len(self.jstats) for i in range(0, len(ou_avg))]
        pc_avg = [pc_avg[i] / len(self.jstats) for i in range(0, len(pc_avg))]
        pu_avg = [pu_avg[i] / len(self.jstats) for i in range(0, len(pu_avg))]

        jstat_avg = jvmStat(None, ec_avg, eu_avg, oc_avg, ou_avg, pc_avg, pu_avg)

        self.draw(jstat_avg, plt)

        plt.show()

    def draw_gc(self):
        gc_stats = []
        for filename in self.filenames:
            gc_stat = gcStat(filename)
            #cstat.parse()
            gc_stats.append(gc_stat)

        ygc_avg = gc_stats[0].ygct
        gct_avg = gc_stats[0].gct

        for i in range(1, len(gc_stats)):
            ygc_avg = [x + y for (x, y) in zip(ygc_avg, gc_stats[i].ygct)]
            gct_avg = [x + y for (x, y) in zip(gct_avg, gc_stats[i].gct)]

        ygc_avg = [ygc_avg[i] / len(gc_stats) for i in range(0, len(ygc_avg))]
        gct_avg = [gct_avg[i] / len(gc_stats) for i in range(0, len(gct_avg))]

        #ygc_avg = [ygc_avg[i] - ygc_avg[i - 1] for i in range(1, len(ygc_avg))]
        #gct_avg = [gct_avg[i] - gct_avg[i - 1] for i in range(1, len(gct_avg))]

        #print ygc_avg

        timeArray = []
        for i in range(0, len(ygc_avg)):
            timeArray.append(i * 2)

        plt.xlabel("Time")
        plt.ylabel("GC Time")
        plt.ylim(0, 10)
        plt.xlim(0, timeArray[-1])

        plt.plot(timeArray, ygc_avg, "r", color="blue", label="young gc", linewidth=2.0)
        plt.plot(timeArray, gct_avg, "r", color="red", label="total gc", linewidth=2.0)

        plt.legend(loc=2)

        plt.show()

class gcStat:
    def __init__(self, filename):
        self.ygct = []
        self.fgct = []
        self.gct = []
        self.filename = filename
        self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if len(lines) != 15:
            print "Error jvm stat file"
            exit(1)

        f.seek(1)
        for line in f:
            stats = line.split()
            if len(stats) == 15 and stats[0] != "S0C":
                self.ygct.append(float(stats[11]))
                self.fgct.append(float(stats[13]))
                self.gct.append(float(stats[14]))

class jvmStat:
    def __init__(self, filename, ec=None, eu=None, oc=None, ou=None, pc=None, pu=None):
        self.filename = filename
        if ec is None and eu is None and oc is None and ou is None and pc is None and pu is None:
            self.ec = []
            self.eu = []
            self.oc = []
            self.ou = []
            self.pc = []
            self.pu = []
        else:
            self.ec = ec
            self.eu = eu
            self.oc = oc
            self.ou = ou
            self.pc = pc
            self.pu = pu

        if filename is not None:
            self.parse()

    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        lines = test_line.split()
        if len(lines) != 15:
            print "Error jvm stat file"
            exit(1)

        f.seek(1)
        for line in f:
            stats = line.split()
            if len(stats) == 15 and stats[0] != "S0C":
                self.ec.append(float(stats[4])/(1024*1024))
                self.eu.append(float(stats[5])/(1024*1024))
                self.oc.append(float(stats[6])/(1024*1024))
                self.ou.append(float(stats[7])/(1024*1024))
                self.pc.append(float(stats[8])/(1024*1024))
                self.pu.append(float(stats[9])/(1024*1024))


