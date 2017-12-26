'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''
from __future__ import print_function
import argparse
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from iter import *
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from importlib import import_module
import os
config =tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction=0.4
set_session(tf.Session(config=config))

def weakloss(ytrue,ypred):
	a=K.sum(ypred)/ypred.shape[0] 
	b=K.sum(ytrue)/ypred.shape[0]
	loss=a - b
	print(type(loss))
	loss=K.square(loss)
	return loss
def mean_squared_error(y_true,y_pred):
	return K.mean(K.square(y_pred - y_true),axis=-1)
batch_size = 500
num_classes = 2
epochs = 25

parser=argparse.ArgumentParser()
parser.add_argument("--rat",type=float,default=0.6,help='ratio for weak qg batch')
parser.add_argument("--end",type=float,default=1.,help='end ratio')
parser.add_argument("--save",type=str,default="test_",help='save name')
parser.add_argument("--network",type=str,default="asvgg",help='network name on symbols/')
parser.add_argument("--left",type=str,default="qq",help='which train sample (qq,gg,zq,zg)')
parser.add_argument("--right",type=str,default="gg",help='which train sample (qq,gg,zq,zg)')
parser.add_argument("--ztest",type=int,default=0,help='true get zjet test')
parser.add_argument("--loss",type=str,default="categorical_crossentropy",help='network name on symbols/')
args=parser.parse_args()

# input image dimensions
img_rows, img_cols = 33, 33

# the data, shuffled and split between train and test sets
#(x_train, y_train), (x_test, y_test) = mnist.load_data()

#if K.image_data_format() == 'channels_first':
#    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
#    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
#    input_shape = (1, img_rows, img_cols)
#else:
#x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
#x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (3,img_rows, img_cols)

if(args.loss=="weakloss"):args.loss=weakloss
net=import_module('symbols.'+args.network)
model=net.get_symbol(input_shape,num_classes)
#model.compile(loss='mean_squared_error',
model.compile(loss=args.loss,
              optimizer=keras.optimizers.SGD(),
	      metrics=['accuracy'])
"""model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(),
              metrics=['accuracy'])
"""
#ab=int(len(x_train)/10)

train=wkiter(["root/new/train"+args.left+str(int(args.rat*100))+"img.root","root/new/train"+args.right+str(int(args.rat*100))+"img.root"],batch_size=batch_size,end=args.end,istrain=1,friend=0)
#train=wkiter(["root/new/q"+str(int(args.rat*100))+"img.root","root/new/g"+str(int(args.rat*100))+"img.root"],batch_size=batch_size,end=5./7.,istrain=1,friend=0)
if(args.ztest==1):test=wkiter(["root/new/mg5_pp_zq_passed_pt_100_500_sum_img.root","root/new/mg5_pp_zg_passed_pt_100_500_sum_img.root"],batch_size=batch_size,begin=5./7.,end=5./7.+args.end*2./7.,istrain=0,friend=0)
else:test=wkiter(["root/new/mg5_pp_qq_balanced_pt_100_500_sum_img.root","root/new/mg5_pp_gg_balanced_pt_100_500_sum_img.root"],batch_size=batch_size,begin=5./7.,end=5./7.+args.end*2./7.,istrain=0,friend=0)
savename='save/'+str(args.save)+str(args.rat)
os.system("mkdir "+savename)
print ("train",train.totalnum(),"eval",test.totalnum())
#logger=keras.callbacks.CSVLogger(savename+'/log.log',append=True)
logger=keras.callbacks.TensorBoard(log_dir=savename+'/logs',histogram_freq=0, write_graph=True , write_images=True, batch_size=batch_size)
history=0
checkpoint=keras.callbacks.ModelCheckpoint(filepath=savename+'/_{epoch}',monitor='val_loss',verbose=0,save_best_only=False,mode='auto',period=1)
history=model.fit_generator(train.next(),steps_per_epoch=train.totalnum(),validation_data=test.next(),validation_steps=test.totalnum(),epochs=epochs,verbose=1,callbacks=[logger,checkpoint])
#train.reset()
#test.reset()
print(history)
f=open(savename+'/history','w')
f.write(str(history.history['val_acc'].index(max(history.history['acc'])))+'\n')
f.write(str(history.history))
f.close()
