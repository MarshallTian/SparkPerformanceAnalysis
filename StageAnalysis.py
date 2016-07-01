# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import numpy as np
import os.path

class stageAnalysis:
    def __init__(self, filenames, name="default"):
        self.filenames = filenames
        print filenames
        self.name = name
        self.total_time = []
        self.total_gc = []
        self.total_sw = []
        self.total_fr = []
        self.total_et = []


    def get_json(self,line):
        # Need to first strip the trailing newline, and then escape newlines (which can appear
        # in the middle of some of the JSON) so that JSON library doesn't barf.
        return json.loads(line.strip("\n").replace("\n", "\\n")) # transfer to str

    def draw_total(self):
        for filename in self.filenames:
            print filename
            self.analysis(filename)

        gcTimeRatio = map(lambda(a, b): 100*a/b, zip(self.total_gc, self.total_time))
        execTimeRatio = map(lambda(a, b): 100*a/b, zip(self.total_et, self.total_time))
        FetchWaitTimeRatio = map(lambda(a, b): 100*a/b, zip(self.total_fr, self.total_time))
        ShuffleWriteTimeRatio = map(lambda(a, b): 100*a/b, zip(self.total_sw, self.total_time))

        # print self.filenames
        # print gcTimeRatio
        # print execTimeRatio
        # print FetchWaitTimeRatio
        # print ShuffleWriteTimeRatio

        #plt.rc('font', family='SimHei', size=13)
        num1 = np.array(execTimeRatio)
        num2 = np.array(gcTimeRatio)
        num3 = np.array(ShuffleWriteTimeRatio)
        num4 = np.array(FetchWaitTimeRatio)
        width = 0.5
        idx = np.arange(len(self.total_time))
        #plt.figure(figsize=(10, 8))


        plt.bar(idx, num1, width, color='#E6C5DC', label='Executor Run Time', align='center',  hatch="//")
        plt.bar(idx, num2, width, bottom=num1, color='#C0DA99', label='GC Time', align='center', hatch="\\")
        plt.bar(idx, num3, width, bottom=num1+num2, color='#B9DFD4', label='Shuffle Write Time', align='center', hatch="+")
        plt.bar(idx, num4, width, bottom=num1+num2+num3, color='#BFC0BF', label='Fetch Wait Time', align='center',  hatch="-")


        font = {
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }
        plt.xlabel("Workload", fontdict=font)
        plt.ylabel("Time Ratio(%)", fontdict=font)
        #plt.xlim(0, 9)
        plt.ylim(0, 125)
        #plt.barh(np.arange(len(stageID)), num1, align='center', alpha=0.4)
        names = ["WordCount", "Grep", "NaiveBayes", "Kmeans", "PageRank", "CC", "Select", "Aggregation", "Join"]
        plt.xticks(idx, names, fontsize=11, rotation='vertical')
        #plt.margins(0.5)
        plt.subplots_adjust(bottom=0.22)
        plt.legend(loc='upper center', prop={'size': 13}, ncol=2)
        #plt.title(self.name, fontdict=font)
        #plt.subplots_adjust(left=0.05, right=0.95, bottom=0.12, top=0.95)
        #fig = plt.gcf()
        #fig.set_size_inches(18.5, 10.5)
        #plt.savefig("./images/%s.eps" % os.path.basename(self.filenames))
        #plt.savefig("./images/%s.png" % os.path.basename(self.filenames))
        plt.savefig("/Users/XinhuiTian/newwork/benchmark/TPDS/TPDS-BigDataBench-2015/figures/job.ps")
        plt.show()


    def analysis(self, filename):
        print "Parsing %s now" % filename

        f = open(filename, "r")
        test_line = f.readline()

        try:
            self.get_json(test_line)
            is_json = True
            #print ("Parsing file %s as JSON" % self.filenames)
        except:
            is_json = False
            #print ("Parsing file %s as JobLogger output" % self.filenames)
        f.seek(0)

        # count the stage number
        stageNumber = 0
        for line in f:
            if is_json:
                json_data = self.get_json(line)
                event_type = json_data["Event"]

                if event_type == "SparkListenerTaskEnd":
                    stage_id = json_data["Stage ID"]
                    if stage_id > stageNumber:
                        stageNumber = stage_id
        print "total stage number: %s" % (stageNumber+1)
        if stageNumber == 0:
            print "There is only one stage in the log"
            self.singleStageAnalysis(filename)
            return

        f.seek(0)

        stageNumber += 1

        execTime = [0 for x in range(0, stageNumber)]
        gcTime = [0 for x in range(0, stageNumber)]
        FetchWaitTime = [0 for x in range(0, stageNumber)]
        ShuffleWriteTime = [0 for x in range(0, stageNumber)]

        for line in f:
            if is_json:
                json_data = self.get_json(line)
                event_type = json_data["Event"]

                if event_type == "SparkListenerTaskEnd":
                    stage_id = json_data["Stage ID"]
                if json_data.has_key("Task Metrics") == True:
                    task_metrics = json_data["Task Metrics"]

                    for i in range(0, stageNumber):
                        if stage_id == i:
                            execTime[i] += task_metrics["Executor Run Time"]
                            gcTime[i] += task_metrics["JVM GC Time"]
                            if task_metrics.has_key("Shuffle Read Metrics") == True:
                                Shuffle_Read_Metrics = task_metrics["Shuffle Read Metrics"]
                                FetchWaitTime[i] += Shuffle_Read_Metrics["Fetch Wait Time"]
                            elif task_metrics.has_key("Shuffle Write Metrics") == True:
                                Shuffle_Write_Metrics = task_metrics["Shuffle Write Metrics"]
                                ShuffleWriteTime[i] += Shuffle_Write_Metrics["Shuffle Write Time"]

        # convert time unit
        gcTime = [i*10**(-3)for i in gcTime]
        execTime = [i*10**(-3) for i in execTime]
        FetchWaitTime = [i*10**(-3) for i in FetchWaitTime]
        ShuffleWriteTime = [i*10**(-9)for i in ShuffleWriteTime]

        totalTime = np.array(gcTime)+np.array(execTime)+np.array(FetchWaitTime)+np.array(ShuffleWriteTime)
        totalTime = [float('%.3f'% i) for i in totalTime]
        #print "total time:%s"% totalTime

        self.total_time.append(np.sum(totalTime))
        self.total_et.append(np.sum(execTime))
        self.total_gc.append(np.sum(gcTime))
        self.total_fr.append(np.sum(FetchWaitTime))
        self.total_sw.append(np.sum(ShuffleWriteTime))

        #print "self total time: %s %s %s %s %s" % (self.total_time, self.total_et, self.total_fr, self.total_sw, self.total_gc)

        for i in range(0, len(totalTime)):
            if totalTime[i] ==0:
                totalTime[i] =1
        '''
        for i in range(len(totalTime)-1, -1, -1):
            if totalTime[i] == 0:
                totalTime.pop(i)  #delete the one whose time is 0
                gcTime.pop(i)
                execTime.pop(i)
                FetchWaitTime.pop(i)
                ShuffleWriteTime.pop()
                stageNumber -= 1
        '''
        # print "JVM GC Time: %s" % gcTime
        # print "Executor Run Time: %s" % execTime
        # print "Fetch Wait Time:%s"% FetchWaitTime
        # print "Shuffle Write Time:%s"% ShuffleWriteTime
        # print "total time:%s"% totalTime

        gcTimeRatio = map(lambda(a, b): 100*a/b, zip(gcTime, totalTime))
        execTimeRatio = map(lambda(a, b): 100*a/b, zip(execTime, totalTime))
        FetchWaitTimeRatio = map(lambda(a, b): 100*a/b, zip(FetchWaitTime, totalTime))
        ShuffleWriteTimeRatio = map(lambda(a, b): 100*a/b, zip(ShuffleWriteTime, totalTime))

        # print "JVM GC Time Ratio:%s" % gcTimeRatio
        # print "Executor Run Time Ratio:%s" % execTimeRatio
        # print "Fetch Wait Time Ratio:%s"% FetchWaitTimeRatio
        # print "Shuffle Write Time Ratio:%s" % ShuffleWriteTimeRatio

        # stageID =['stage %d' % i for i in range(0, stageNumber)]
        # print stageID
        # #plt.rc('font', family='SimHei', size=13)
        # num1 = np.array(execTimeRatio)
        # num2 = np.array(gcTimeRatio)
        # num3 = np.array(ShuffleWriteTimeRatio)
        # num4 = np.array(FetchWaitTimeRatio)
        # width = 0.5
        # idx = np.arange(len(stageID))
        # plt.figure(figsize=(15, 10))
        #
        # plt.bar(idx, num4, width, color='#BFC0BF', label='Fetch Wait Time', align='center',  hatch="-")
        # plt.bar(idx, num1, width, bottom=num4, color='#E6C5DC', label='Executor Run Time', align='center',  hatch="//")
        # plt.bar(idx, num2, width, bottom=num1 + num4, color='#C0DA99', label='GC Time', align='center', hatch="\\")
        #
        # rects = plt.bar(idx, num3, width, bottom=num1+num2 + num4, color='#B9DFD4', label='Shuffle Write Time', align='center', hatch="+")
        # for i in range(0, len(stageID)):
        #     rect = rects[i]
        #     height = 100
        #     value = totalTime[i]
        #     plt.text(rect.get_x() + rect.get_width()/2., 1.07*height,
        #         '%.2f' % value,
        #         ha='center', va='top', fontsize=8, rotation=60)
        #
        # font = {
        # 'color':  'black',
        # 'weight': 'normal',
        # 'size': 22,
        # }
        #plt.xlabel("stage ID", fontdict=font)
        #plt.ylabel("Time Ratio(%)", fontdict=font)
        #plt.xlim(0, len(stageID) * (41/40))
        #plt.ylim(0, 125)
        #plt.barh(np.arange(len(stageID)), num1, align='center', alpha=0.4)
        #plt.xticks(idx, stageID, fontsize=12, rotation=17)
        #plt.legend(loc='upper center', prop={'size': 12}, ncol=2)
        #plt.title(self.name, fontdict=font)
        #plt.subplots_adjust(left=0.05, right=0.95, bottom=0.12, top=0.95)
        #fig = plt.gcf()
        #fig.set_size_inches(18.5, 10.5)
        #plt.savefig("./images/%s.eps" % os.path.basename(self.filenames))
        #plt.savefig("./images/%s.png" % os.path.basename(self.filenames))
        #plt.savefig("/Users/XinhuiTian/newwork/benchmark/TPDS/TPDS-BigDataBench-2015/figures/stage-%s.eps" % self.name)
        #plt.show()

    def singleStageAnalysis(self, filename):
        f = open(filename, "r")
        execTime = 0
        gcTime = 0
        FetchWaitTime = 0
        ShuffleWriteTime = 0
        for line in f:
            json_data = self.get_json(line)
            event_type = json_data["Event"]
            if event_type == "SparkListenerTaskEnd":
                if json_data.has_key("Task Metrics") == True:
                    task_metrics = json_data["Task Metrics"]
                    execTime += task_metrics["Executor Run Time"]
                    gcTime += task_metrics["JVM GC Time"]
                    if task_metrics.has_key("Shuffle Read Metrics") == True:
                        Shuffle_Read_Metrics = task_metrics["Shuffle Read Metrics"]
                        FetchWaitTime+= Shuffle_Read_Metrics["Fetch Wait Time"]
                    elif task_metrics.has_key("Shuffle Write Metrics") == True:
                        Shuffle_Write_Metrics = task_metrics["Shuffle Write Metrics"]
                        ShuffleWriteTime+= Shuffle_Write_Metrics["Shuffle Write Time"]

        gcTime = gcTime*10**(-3)
        execTime = execTime*10**(-3)
        FetchWaitTime = FetchWaitTime*10**(-3)
        ShuffleWriteTime = ShuffleWriteTime*10**(-9)
        totalTime = gcTime+execTime+FetchWaitTime+ShuffleWriteTime
        totalTime = float('%.3f'% totalTime)

        self.total_time.append(totalTime)
        self.total_et.append(execTime)
        self.total_gc.append(gcTime)
        self.total_fr.append(FetchWaitTime)
        self.total_sw.append(ShuffleWriteTime)

        gcTimeRatio = 100*gcTime/totalTime
        execTimeRatio = 100*execTime/totalTime
        FetchWaitTimeRatio =100* FetchWaitTime/totalTime
        ShuffleWriteTimeRatio = 100*ShuffleWriteTime/totalTime
        # print "JVM GC Time Ratio:%s" % gcTimeRatio
        # print "Executor Run Time Ratio:%s" % execTimeRatio
        # print "Fetch Wait Time Ratio:%s"% FetchWaitTimeRatio
        # print "Shuffle Write Time Ratio:%s" % ShuffleWriteTimeRatio

        # width = 0.3
        # plt.bar(0, execTimeRatio, width, color='#E6C5DC', label='Executor Run Time')
        # plt.bar(1, gcTimeRatio, width, bottom=execTimeRatio, color='#C0DA99', label='GC Time')
        # plt.bar(2, ShuffleWriteTimeRatio, width, bottom=execTimeRatio+gcTimeRatio, color='#B9DFD4', label='Shuffle Write Time')
        # plt.bar(3, FetchWaitTimeRatio, width, bottom=execTimeRatio+gcTimeRatio+ShuffleWriteTimeRatio,  color='#BFC0BF', label='Fetch Wait Time')
        # plt.xlabel("stage ID 0")
        # plt.ylabel("Time Ratio(%)")
        # plt.ylim(0, 100)
        # plt.xticks([1+width/2], 'stage ID 0', rotation=40, fontsize=8)
        # plt.legend(loc='best', prop={'size': 12})
        #plt.savefig("./images/%s.eps" % os.path.basename(self.filenames))
        #plt.show()