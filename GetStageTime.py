import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import numpy as np
import matplotlib
import json

class getStageTime:

    def __init__(self, filenames):
        self.filenames = filenames
        self.stageTime = []
        self.analysis()

    def get_json(self, line):
        return json.loads(line.strip("\n").replace("\n", "\\n"))

    def analysis(self):

        f = open(self.filenames, "r")
        test_line = f.readline()

        try:
            self.get_json(test_line)
            is_json = True
            print ("Parsing file %s as JSON" % self.filenames)
        except:
            is_json = False
            print ("Parsing file %s as JobLogger output" % self.filenames)
        f.seek(0)

        self.stageRuntime =[]
        for line in f:
            if is_json:
                json_data = self.get_json(line)
                event_type = json_data["Event"]
                if event_type =="SparkListenerStageCompleted":
                    stage_info = json_data["Stage Info"]
                    self.stageRuntime.append(int((stage_info["Completion Time"]-stage_info["Submission Time"])*10**(-3)))

        self.stageTime = [0 for x in range(0, len(self.stageRuntime))]
        for i in range(0, len(self.stageRuntime)):
            self.stageTime[i] = self.stageTime[i-1]+self.stageRuntime[i]
        #print self.stageTime


