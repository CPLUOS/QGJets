import os
import ROOT
import numpy as np
from sklearn.metrics import roc_curve, auc
from statsmodels.nonparametric.smoothers_lowess import lowess

import matplotlib.pyplot as plt


ROOT.gROOT.SetBatch(True)


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
        
    def plot(self, data_pair_list, title):
        plt.figure(figsize=(8, 6))
        plt.rc("font", size=12)
        
        for x, y in data_pair_list:
            color = self._color(y)
            plt.plot(getattr(self, x), getattr(self, y),
                     color=color, lw=2, alpha=0.2, label=y)
            
            x_filtered, y_filtered = self._smooth(
                getattr(self, x),getattr(self, y))
            
            plt.plot(x_filtered, y_filtered,
                     color=color, lw=2, label=y+'(lowess)')

        plt.xlabel(x)
        plt.ylabel(y)

        plt.title(title)
        plt.legend(loc='best')
        plt.grid()
        #plt.show()
        path = os.path.join(self.dpath, title + ".png")
        plt.savefig(path)
        plt.close()
        
    def prepare(self, data_pair_list, title):
        self.waiting_list.append({"data_pair_list": data_pair_list, "title": title})

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


class ROCMeter(object):
    def __init__(self, dpath, step, title, prefix=""):
        self.dpath = dpath
        self.step = step
        self.title = title
        self._prefix = prefix

        self.labels = np.array([])
        self.preds = np.array([])  # predictions

        # uninitialized attributes
        self.fpr = None
        self.tpr = None
        self.fnr = None
        self.auc = None

    def append(self, labels, preds):
        # self.labels = np.r_[self.labels, labels]
        # self.preds = np.r_[self.preds, preds]
        self.labels = np.append(self.labels, labels)
        self.preds = np.append(self.preds, preds)


    def compute_roc(self):
        self.fpr, self.tpr, _ = roc_curve(self.labels, self.preds)
        self.fnr = 1 - self.fpr
        self.auc = auc(self.fpr, self.tpr)

    def save_roc(self, path):
        logs = np.vstack([self.tpr, self.fnr, self.fpr]).T
        np.savetxt(path, logs, delimiter=',', header='tpr, fnr, fpr')

    def plot_roc_curve(self, path):
        # fig = plt.figure()
        plt.plot(self.tpr, self.fnr, color='darkorange',
                 lw=2, label='ROC curve (area = %0.3f)' % self.auc)
        plt.plot([0, 1], [1, 1], color='navy', lw=2, linestyle='--')
        plt.plot([1, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.1])
        plt.ylim([0.0, 1.1])
        plt.xlabel('Quark Jet Efficiency (TPR)')
        plt.ylabel('Gluon Jet Rejection (FNR)')
        plt.title('%s-%d / ROC curve' % (self.title, self.step))
        plt.legend(loc='lower left')
        plt.grid()
        plt.savefig(path)
        plt.close()

    def finish(self):
        self.compute_roc()

        filename_format = '{prefix}roc_step-{step}_auc-{auc:.3f}.{ext}'.format(
            prefix=self._prefix,
            step=str(self.step).zfill(6),
            auc=self.auc,
            ext='%s'
        )

        csv_path = os.path.join(self.dpath, filename_format % 'csv')
        plot_path = os.path.join(self.dpath, filename_format % 'png')

        self.save_roc(csv_path)
        self.plot_roc_curve(plot_path)



class OutHist(object):
    def __init__(self, dpath, step, dname_list):
        filename = "outhist-step_{step}.root".format(step=step)
        path = os.path.join(dpath, filename)

        self._dname_list = dname_list

        self.root_file = ROOT.TFile(path, "RECREATE")
        self.hists = {}
        for dname in dname_list:
            self.make_dir_and_qg_hists(dname)

    def make_dir_and_qg_hists(self, dname):
        # root file
        self.root_file.mkdir(dname)
        self.root_file.cd(dname)
        # just attributes
        self.hists[dname] = {}
        # histograms
        self.hists[dname]["quark"] = self._make_hist("quark")
        self.hists[dname]["quark"].SetDirectory(self.root_file.Get(dname))
        self.hists[dname]["gluon"] = self._make_hist("gluon")
        self.hists[dname]["gluon"].SetDirectory(self.root_file.Get(dname))


    def _make_hist(self, name):
        return ROOT.TH1F(name, name, 100, 0, 1)

    def cd(self, dname):
        self.root_file.cd(dname)

    def fill(self, dname, labels, preds):
        for is_gluon, gluon_likeness in zip(labels, preds):
            if is_gluon:
                self.hists[dname]["gluon"].Fill(gluon_likeness)
            else:
                self.hists[dname]["quark"].Fill(gluon_likeness)

    def save(self):
        self.root_file.Write()
        self.root_file.Close()

    def finish(self):
        self.save()
