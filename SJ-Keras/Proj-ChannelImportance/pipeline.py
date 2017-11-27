from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ROOT
import numpy as np


class DataLoader(object):
    def __init__(self, path, channel, batch_size, cyclic, image_shape=(1, 33, 33)):
        self.path = path
        self.channel = channel
        self.batch_size = batch_size
        self.cyclic = cyclic
        self._image_shape = image_shape
        
        c, h, w = image_shpae

        channel = channel.lower()
        if channel == "cpt":
            self._slicing = slice(0, h*w)
        elif channel == "npt":
            self._slicing = slice(h*w, 2*h*w)
        elif channel == "cmu":
            self._slicing = slice(2*h*w, 3*h*w)
        else:
            raise ValueError("")


        self.root_file = ROOT.TFile(path, "READ")
        self.tree = self.root_file.Get("jet")
        
        self._start = 0
        
    def __len__(self):
        return int(self.tree.GetEntries())
    
    def _get_data(self, idx):
        self.tree.GetEntry(idx)
        image = np.array(self.tree.image, dtype=np.float32)
        image = image[self._slicing].reshape(self._image_shape)
        label = np.int64(self.tree.label[1])
        return (image, label)
        
    
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key >= len(self):
                raise IndexError
            return self._get_data(key)
        elif isinstance(key, slice):
            x = []
            y = []
            for idx in xrange(*key.indices(len(self))):
                image, label = self._get_data(idx)
                x.append(image)
                y.append(label)
            x = np.array(x)
            y = np.array(y)
            return (x, y)
        else:
            raise TypeError
            
    def next(self):
        if self.cyclic:
            if self._start + 1 < len(self):
                end = self._start + self.batch_size
                slicing = slice(self._start, end)
                if end <= len(self):
                    self._start = end
                    return self[slicing]
                else:
                    x, y = self[slicing]
                    
                    self._start = 0
                    end = end - len(self)

                    x1, y1 = self[slice(self._start, end)]
                    self._start = end
                    
                    np.append(x, x1, axis=0)
                    np.append(y, y1, axis=0)
                    return x, y
            else:
                self._start = 0
                return self.next()
        else:
            if self._start + 1 < len(self):
                end = self._start + self.batch_size
                slicing = slice(self._start, end)
                self._start = end
                return self[slicing]
            else:
                raise StopIteration
                
    def __next__(self):
        return self.next()

    def __iter__(self):
        for start in xrange(0, len(self), self.batch_size): 
            yield self[slice(start, start+self.batch_size)]



