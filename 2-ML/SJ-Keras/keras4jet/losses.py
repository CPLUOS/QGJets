import tensorflow as tf
import keras.backend as K


def binary_cross_entropy_with_logits(y_true, logits):
    xent = tf.nn.sigmoid_cross_entropy_with_logits(
        labels=y_true, logits=logits)
    return tf.reduce_mean(xent, axis=-1)
