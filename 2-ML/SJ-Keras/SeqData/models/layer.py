from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import keras
from keras.layers import (
    Input,
    Conv1D,
    LSTM,
    GRU,
    Concatenate,
    Dense,
    Activation,
    BatchNormalization as BN
)
from keras.models import (
    Model,
    Sequential
)


def add_an_sigmoid_layer(model, name=None):

    if name is None:
        name = "{}_with_sigmoid".format(model.name)

    sig = Sequential(name=name)
    sig.add(model)
    sig.add(Activation("sigmoid", name="predictions"))
    return sig
