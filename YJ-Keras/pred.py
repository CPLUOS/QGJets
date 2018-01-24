'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''
from iter import *
import argparse
import keras
from keras import backend as K
from iter import *
import numpy as np
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from importlib import import_module
from array import array
import matplotlib.pyplot as plt
import ROOT as rt
plt.switch_backend('agg')
config =tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction=0.1
set_session(tf.Session(config=config))

batch_size = 500
num_classes = 2
epochs = 20

parser=argparse.ArgumentParser()
parser.add_argument("--rat",type=float,default=0.6,help='ratio for weak qg batch')
parser.add_argument("--new",type=int,default=1,help='new or old')
parser.add_argument("--result",type=int,default=0,help='save result')
parser.add_argument("--epoch",type=int,default=-1,help='epoch')
parser.add_argument("--load",type=str,default="weakdijet_0.8",help='load name')
parser.add_argument("--save",type=str,default="test",help='rch')
parser.add_argument("--ztest",type=int,default="0",help='rch')
args=parser.parse_args()

# input image dimensions
img_rows, img_cols = 33, 33

input_shape = (3,img_rows, img_cols)

#model.compile(loss=keras.losses.categorical_crossentropy,
#              optimizer=keras.optimizers.Adadelta(),
#              metrics=['accuracy'])
#model=keras.models.load_model('save/fullydijetsame_10')
savename="save/"+args.load
#if(args.result==1):
#	f=open(savename+"/history",'r')
#	args.epoch=int(f.readline())
if(args.epoch==-1):
	f=open(savename+'/history')
	args.epoch=eval(f.readline())+1
	f.close()
model=keras.models.load_model(savename+"/_"+str(args.epoch))

#train=wkiter(["root/cutb/q"+str(int(args.rat*100))+"img.root","root/cutb/g"+str(int(args.rat*100))+"img.root"],batch_size=batch_size,end=1,istrain=1,friend=0)
#test=wkiter("root",friend=20,begin=5./7.,end=1.,batch_size=batch_size)
if(args.result==1):train=wkiter(["root/new/trainq"+str(int(args.rat*100))+"img.root","root/new/traing"+str(int(args.rat*100))+"img.root"],batch_size=batch_size,end=1.,istrain=1,friend=0)
if(args.new==0):test=wkiter(["root/cutb/testq100img.root","root/cutb/testg100img.root"],batch_size=batch_size,end=1.,istrain=0,friend=0)
if(args.new==1):
	if(args.ztest==1):test=wkiter(["root/new/mg5_pp_zq_passed_pt_100_500_sum_img.root","root/new/mg5_p1p_zg_passed_pt_100_500_sum_img.root"],batch_size=batch_size,begin=5./7.,end=1,istrain=0,friend=0)
	else:test=wkiter(["root/new/mg5_pp_qq_balanced_pt_100_500_sum_img.root","root/new/mg5_pp_gg_balanced_pt_100_500_sum_img.root"],batch_size=batch_size,begin=5./7.,end=1,istrain=0,friend=0)
from sklearn.metrics import roc_auc_score, auc,precision_recall_curve,roc_curve,average_precision_score
x=[]
y=[]
g=[]
q=[]
print test.totalnum()
if(args.result==1):
	print train.totalnum()
	f=rt.TFile(savename+"/out.root",'recreate')
	qt=rt.TTree("quark","quark")
	gt=rt.TTree("gluon","gluon")
	l=array('i',[0])
	o=array('f',[0])
	qt.Branch("output",o,"output/F")
	gt.Branch("output",o,"output/F")
	batch_num=batch_size
	nn=0
	for j in range(test.totalnum()+1):
		if(test.endfile==1):break
		a,c=test.test()
		b=model.predict(a,verbose=0)[:,0]
		for i in range(len(b)):
			nn+=1
			o[0]=b[i]
			if(c[i][0]==1):
				gt.Fill()
			else:
				qt.Fill()
		
	"""for j in range(test.totalnum()):
		a,c=test.test()
		b=model.predict(a,verbose=0)[:,0]
		for i in range(batch_num):
			nn+=1
			o[0]=b[i]
			if(c[i][0]==1):
				gt.Fill()
			else:
				qt.Fill()
	"""
	f.Write()
	f.Close()
	print nn
	
entries=300
batch_num=batch_size
print ("eval",test.totalnum())
for j in range(entries):
	a,c=test.test()
	b=model.predict(a,verbose=0)[:,0]
	x=np.append(x,np.array(c[:,0]))
	y=np.append(y,b)
	for i in range(batch_num):
		if(c[i][0]==1):
			g.append(b[i])
		else:
			q.append(b[i])
plt.figure(1)
plt.hist(q,bins=50,weights=np.ones_like(q),histtype='step',alpha=0.7,label='quark')
plt.hist(g,bins=50,weights=np.ones_like(g),histtype='step',alpha=0.7,label='gluon')
plt.legend(loc="upper center")
plt.savefig(savename+"/"+args.save+"out.png")
f=open(savename+"/"+args.save+"out.dat",'w')
f.write(str(q)+"\n")
f.write(str(g))
f.close
t_fpr,t_tpr,_=roc_curve(x,y)
t_fnr=1-t_fpr
test_auc=np.around(auc(t_fpr,t_tpr),4)
plt.figure(2)
plt.plot(t_tpr,t_fnr,alpha=0.5,label="AUC={}".format(test_auc),lw=2)
plt.legend(loc='lower left')
plt.savefig(savename+"/"+args.save+"roc"+str(test_auc)+".png")
f=open(savename+"/"+args.save+"roc.dat",'w')
f.write(str(t_tpr.tolist())+'\n')
f.write(str(t_fnr.tolist()))
f.close()
#print(b,c)

