import os
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt

class Meter(object):

    def __init__(self, data_list, dpath):
        for name in data_list:
            setattr(self, name, np.array([]))

        self.data_list = data_list
            
        self.dpath = dpath

        self.waiting_list = []

    def prepare(self, x, ys, title, xaxis=None, yaxis=None):
        self.waiting_list.append({
            "x": x,
            "ys": ys, # [(name0, label0), (name1, label1), ...]
            "title": title,
            "xaxis": x if (xaxis is None) else xaxis,
            "yaxis": title if (yaxis is None) else yaxis,
            "color": None,
            "alpha": None
        })

    def append(self, data_dict):
        for k in data_dict.keys():
            setattr(self, k, np.r_[getattr(self, k), data_dict[k]])

    def plot(self, waiting):
        plt.figure(figsize=(8, 6))
        plt.rc("font", size=12)

        x = waiting["x"] 

        for y in waiting["ys"]:
            color = self._color(y)
            plt.plot(getattr(self, x), getattr(self, y["name"]),
                     color=color, lw=2, alpha=0.2, label=y["label"])
            
            x_filtered, y_filtered = self.smooth(
                getattr(self, x[0]), getattr(self, y[0]))
            
            plt.plot(x_filtered, y_filtered,
                     color=color, lw=2, label=y+'(lowess)')

        plt.xlabel(watiing["xaxis"])
        plt.ylabel(y["yaxis"])

        plt.title(waiting["title"])
        plt.legend(loc='best')
        plt.grid()
        #plt.show()
        path = os.path.join(self.dpath, waiting["title"] + ".png")
        plt.savefig(path)
        plt.close()
        
    def save(self):
        data_collection = {} 
        for data_name in self._data_list:
            data_collection[data_name] = getattr(self, data_name)
        path = os.path.join(self.dpath, "loss_and_acc.npz")
        np.savez(path, **data_collection)
        
    def finish(self):
        for waiting in self.waiting_list:
            self.plot(waiting)
        self.save() 
        
    def smooth(self, x, y):
        filtered = lowess(y, x, is_sorted=True, frac=0.075, it=0)
        return filtered[:, 0], filtered[:, 1]
        
    def _color(self, y):
        if ('tr' in y) and ("dijet" in y):
            color = "navy"
        elif ("tr" in y) and ("zjet" in y):
            color = "darkgreen"
        elif ("val" in y) and ("dijet" in y):
            color = 'orange'
        elif ("val" in y) and ("zjet" in y):
            color = "indianred"
        else:
            color = np.random.rand(3,1)
        return color

