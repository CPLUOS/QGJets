import tensorflow as tf
import keras.backend as K

def accuracy_with_logits(y_true, logits):
    y_pred = K.sigmoid(logits)

    predicted_class = tf.greater(y_pred, 0.5)
    
    correct = tf.equal(predicted_class, tf.equal(y_true, 1.0))
    correct = tf.cast(correct, tf.float32)
    accuracy = tf.reduce_mean(correct)
    return accuracy
    
