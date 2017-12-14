"""
Reference:
  - Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun.
    Deep Residual Learning for Image Recognition.
    arXiv:1512.03385 [cs.CV]

  - Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun.
    Identity Mappings in Deep Residual Networks.
    arXiv:1603.05027 [cs.CV] 

- F: residual function
- h: identity skip connection
- f: activation function
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import keras
import keras.backend as K
import tensorflow as tf

from keras import layers
from keras.layers import (
    Input,
    Activation,
    Conv2D,
    BatchNormalization,
    AveragePooling2D,
    GlobalAveragePooling2D,
    Lambda
)

def original_residual_fn(x, filters, activation="relu"):
    """ From arXiv:1512.03385
    Plain Network. Our plain baselines (Fig. 3, middle) are mainly inspired by
    the philosophy of VGG nets [41] (Fig. 3, left). The convolutional layers
    mostly have 3X3 filters and follow two simple design rules: (i) for the same
    output feature map size, the layers have the same number of filters; and
    (ii) if the feature map size is halved, the number of filters is doubled so
    as to preserve the time complexity per layer. We perform downsampling
    directly by convolutional layers that have a stride of 2.
    """
    # strides for first convolution
    s1 = (2, 2) if  x.shape[1].value < filters else (1, 1)

    x = Conv2D(filters, kernel_size=3, strides=s1)
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)

    x = Conv2D(filters, kernel_size=3) # strides=(1, 1)
    x = BatchNormalization(axis=1)(x)
    return x


# Residual function for full pre-activation
def residual_fn(x, filters, activation="relu"):
    # strides for first convolution
    s1 = (2, 2) if  x.shape[1].value < filters else (1, 1)

    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    x = Conv2D(filters, kernel_size=3, strides=s1)

    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    x = Conv2D(filters, kernel_size=3) # strides=(1, 1)
    return x




def original_bottleneck_residual_fn(x, filters, activation="relu"):
    """
    Because of concerns on the training time that we can afford, we modify the
    building block as a bottleneck design.

    The parameter-free identity shortcuts are particularly important for the
    bottleneck architectures. If the identity shortcut in Fig. 5 (right) is
    replaced with projection, one can show that the time complexity and model
    size are doubled, as the shortcut is connected to the two high-dimensional
    ends. So identity shortcuts lead to more efficient models for the bottleneck
    designs.
    """

    # strides for first convolution
    s1 = (2, 2) if  x.shape[1].value < filters else (1, 1)

    bottleneck_filters = int(filters/4)

    #
    x = Conv2D(filters=bottleneck_filters, kernel_size=1, strides=s1, padding="SAME")(x)
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    #
    x = Conv2D(filters=bottleneck_filters, kernel_size=3, strides=1, padding="SAME")(x)
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    #
    x = Conv2D(filters=filters, kernel_size=1, strides=1, padding="SAME")(x)
    x = BatchNormalization(axis=1)(x)
    return x


def bottleneck_residual_fn(x, filters, activation="relu"):
    # strides for first convolution
    s1 = (2, 2) if  x.shape[1].value < filters else (1, 1)

    bottleneck_filters = int(filters/4)

    #
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    x = Conv2D(filters=bottleneck_filters, kernel_size=1, strides=s1, padding="SAME")(x)
    #
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    x = Conv2D(filters=bottleneck_filters, kernel_size=3, strides=1, padding="SAME")(x)
    #
    x = BatchNormalization(axis=1)(x)
    x = Activation(activation)(x)
    x = Conv2D(filters=filters, kernel_size=1, strides=1, padding="SAME")(x)
    return x

##############################
# Shortcut == Identity skip connection
def identity_shortcut(x):
    shortcut = Lambda(lambda t: tf.identity(t))(x)
    return shortcut

def zero_padding_shortcut(x, filters):
    """
    Zero-padding shortcuts are used for increasing dimensions, and all
    shortcuts are parameter free.
    """
    input_channels = x.shape[1].value

    # Decreases height and width of feature maps
    x = AveragePooling2D(pool_size=(2, 2), strides=(2, 2), padding="SAME")(x)

    # Channel-wise padding
    channel_diff = filters - input_channels
    pad0 = int(channel_diff/2)
    pad1 = channel_diff - pad0
    paddings = [[0, 0], [pad0, pad1], [0, 0], [0, 0]] # [B, C, H, W]

    shortcut = Lambda(lambda t: tf.pad(t, paddings))(x)
    return shortcut


def projection_shortcut(x, filters):
    """
    If this is not the case (e.g., when changing the input/output channels), we
    can perform a linear projection W_{s} by the shortcut connections to match
    the dimensions:
        y = F(x, {W_i}) + W_{s}*x
    """
    shortcut = Conv2D(filters=filters, kernel_size=1, strides=2, padding="SAME")(x)
    return shortcut



#####################################################
#   Residual unit
###################################################

def original_residual_unit(x, filters, activation):
    h = shortcut(shortcut_type, x, filters)
    F = residual_function(residual_fn,_type, x, filters)
    y = layers.add([h, F])
    y = Activation(activation)(y)
    return y 

# full pre-activation type
def residual_unit(x, filters, bottleneck, activation="relu"):
    input_channels = x.shape[1].value
    if input_channels < filters:
        h = projection_shortcut(x, filters)
    else:
        h = identity_shortcut(x)


    if bottleneck:
        F = bottleneck_residual_fn(x, filters, activation)
    else:
        F = residual_fn(x, filters, activation)
    y = layers.add([h, F])
    return y
