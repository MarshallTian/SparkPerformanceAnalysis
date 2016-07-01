import matplotlib.pyplot as plt
class memStat:
    def __init__(self, filename):
        self.filename = filename
        self.total = []
        self.used = []
        self.free = []
        self.shared = []
        self.buffers = []
        self.cached = []
    def parse(self):
        f = open(self.filename, "r")
        test_line = f.readline()
        line_num = len(test_line.split())
        print test_line.split()
        if line_num != 7:
            print "Error line numbers of mem stat file"
            exit(1)

        f.seek(0)
        for line in f:
            stats = line.split()
            self.total.append(int(stats[1]))
            self.used.append(int(stats[2]))
            self.free.append(int(stats[3]))
            self.shared.append(int(stats[4]))
            self.buffers.append(int(stats[5]))
            self.cached.append(int(stats[6]))


    def print_total(self):
        print "%d " % self.total[0]

    def draw(self):
        maxMem = self.total[0]
        minMem = self.total[0]
        for use in self.used:
            if use < minMem:
                minMem = use

        for free in self.free:
            if free < minMem:
                minMem = free

        for shared in self.shared:
            if shared < minMem:
                minMem = shared

        for buffer in self.buffers:
            if buffer < minMem:
                minMem = buffer

        for cache in self.cached:
            if cache < minMem:
                minMem = cache


        timeArray = []
        for i in range(0, len(self.used)):
            timeArray.append(i)

        plt.xlabel("Time")
        plt.ylabel("Memory")
        plt.ylim(minMem, maxMem)
        # plt.plot(timeArray, self.used, 'b*')
        plt.plot(timeArray, self.used, "r", color="blue", label="used")
        plt.plot(timeArray, self.free, "r", color="red", label="free")
        plt.plot(timeArray, self.buffers, "r", color="yellow", label="buffers")
        plt.plot(timeArray, self.cached, "r", color="green", label="cached")
        plt.legend()
        plt.show()


