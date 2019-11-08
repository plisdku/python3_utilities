import timeit
import numpy as np

class TopicalTimer:
    def __init__(self):
        """
        Create timer.
        """
        self.labels = []
        self.times = []
        self.timer = timeit.default_timer
    
    def tic(self):
        """
        Clear timing records and start timing.
        """
        self.labels = ["tic"]
        self.times = [self.timer()]
    
    def toc(self, label=None):
        """
        Append the current time to the time records, with an optional string label.

        Args:
            label (str): a name to associate with this time point (optional)
        """
        if label is not None:
            self.labels.append(label)
        else:
            self.labels.append("")
        self.times.append(self.timer())
        
    def durations(self):
        """
        Return durations between time records.

        Returns:
            np.array: durations = np.diff(times)
        """
        return np.diff(self.times)
    
    def report(self):
        """
        Return list of (label, duration) pairs since last call to toc().

        Returns:
            list: (label, duration) pairs
        """
        return list(zip(self.labels[1:], self.durations()))
    