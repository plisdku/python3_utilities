import timeit

class TopicalTimer:
    def __init__(self):
        self.labels = []
        self.times = []
        self.timer = timeit.default_timer
    
    def tic(self):
        self.labels = ["tic"]
        self.times = [self.timer()]
    
    def toc(self, label=None):
        if label is not None:
            self.labels.append(label)
        else:
            self.labels.append("")
        self.times.append(self.timer())
        
    def durations(self):
        return np.diff(self.times)
    
    def report(self):
        return list(zip(self.labels[1:], self.durations()))
    