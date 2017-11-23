class Meter(object):
    def __init__(self, data_name_list, dpath):
        for data_name in data_name_list:
            setattr(self, data_name, np.array([]))

        self._data_name_list = data_name_list
            
        self.dpath = dpath
        self.waiting_list = []

    def append(self, data_dict):
        for k in data_dict.keys():
            setattr(self, k, np.r_[getattr(self, k), data_dict[k]])
        
    def save(self):
        raise NotImplementedError("")
        
    def plot(self, waiting, title):
        plt.figure(figsize=(8, 6))
        plt.rc("font", size=12)

        x = waiting["x"] 

        for y in waiting["y_list"]:
            color = self._color(y)
            plt.plot(getattr(self, x), getattr(self, y),
                     color=color, lw=2, alpha=0.2, label=y)
            
            x_filtered, y_filtered = self._smooth(
                getattr(self, x), getattr(self, y))
            
            plt.plot(x_filtered, y_filtered,
                     color=color, lw=2, label=y+'(lowess)')

        plt.xlabel(x)
        plt.ylabel(y)

        plt.title(waiting)
        plt.legend(loc='best')
        plt.grid()
        #plt.show()
        path = os.path.join(self.dpath, waiting["title"] + ".png")
        plt.savefig(path)
        plt.close()
        
    def prepare(self, x, y_list, title):
        self.waiting_list.append({
            "x": x,
            "y_list": y_list,
            "title": title})

    def save(self):
        data_collection = {} 
        for data_name in self._data_name_list:
            data_collection[data_name] = getattr(self, data_name)
        path = os.path.join(self.dpath, "loss_and_acc.npz")
        np.savez(path, **data_collection)
        
    def finish(self):
        for waiting in self.waiting_list:
            self.plot(**waiting)
        self.save() 
        
    def _smooth(self, x, y):
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

