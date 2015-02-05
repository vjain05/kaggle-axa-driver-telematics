from pylab import *
import pandas as pd
from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D
from threading import Thread
from threading import Semaphore
from threading import Lock
from Queue import Queue
sam = Semaphore(1)

lck = Lock()
q=Queue(10)

def myFunc(z):
    #if z%2==0 and z>1:
    max_dist=[]
    cumm_dist=[]
    endpt_dist=[]
    passible=True
    for i in range(1,201):
        try:
            vecs=pd.read_csv("/Users/vmac/Downloads/drivers/"+str(z)+"/"+str(i)+".csv")
            #print "proceed"
            #ax.plot(vecs['x'], vecs['y'], color=colors[i%6], lw=1)
            max_dist.append(0.0)
            cumm_dist.append(0.0)
            endpt_dist.append(sqrt(vecs['y'][len(vecs)-1]*vecs['y'][len(vecs)-1]+vecs['x'][len(vecs)-1]*vecs['x'][len(vecs)-1]))
            for j in range(0,len(vecs)):
                local_dist=sqrt(vecs['y'][j]*vecs['y'][j]+vecs['x'][j]*vecs['x'][j])
                if j==0:
                    incr_dist=sqrt(vecs['y'][j]*vecs['y'][j]+vecs['x'][j]*vecs['x'][j])
                else:
                    incr_dist=sqrt((vecs['y'][j]-vecs['y'][j-1])*(vecs['y'][j]-vecs['y'][j-1])+(vecs['x'][j]-vecs['x'][j-1])*(vecs['x'][j]-vecs['x'][j-1]))
                if max_dist[i-1]<local_dist:
                    max_dist[i-1]=local_dist
                cumm_dist[i-1]+=incr_dist
        except Exception, e:
            passible=False
            print e

    if passible==True:
        #prob_vals = hist(max_dist, bins=10,cumulative=True,normed=True)
        mean_max_dist=mean(max_dist)
        std_max_dist=std(max_dist)
        #print std_max_dist
        max_dist=(max_dist-mean_max_dist)/std_max_dist
        mean_cumm_dist=mean(cumm_dist)
        std_cumm_dist=std(cumm_dist)
        cumm_dist=(cumm_dist-mean_cumm_dist)/std_cumm_dist
        mean_endpt_dist=mean(endpt_dist)
        std_endpt_dist=std(endpt_dist)
        endpt_dist=(endpt_dist-mean_endpt_dist)/std_endpt_dist

        the_norms=np.sqrt(np.square(max_dist)+np.square(cumm_dist)+np.square(endpt_dist))
        #mean_norms=mean(the_norms)
        #median_norms=median(the_norms)
        #print mean(the_norms),median(the_norms)
        #fig = plt.figure()
        #ax = Axes3D(fig)
        #plt.hist(the_norms)
        #ax.scatter(max_dist, cumm_dist, endpt_dist)
        #plt.show()
        prob_vals=hist(the_norms, bins=10, cumulative=True,normed=True)

        #print max_dist
        #exit(0)
        #print prob_vals[0], prob_vals[1]

        #approach 1: calculate max distance from origin for each path, use histogram to check for anomalies gap
        #approach 2: calculate max_dist, cumulative dist, and endpoint distance,make z score,
        #  use histogram to check for anomalies gap
        threshold1=0
        threshold2=0
        for i in range(0,len(prob_vals[0])-1):
            #print prob_vals[0][i+1]-prob_vals[0][i]
            if prob_vals[0][i+1]-prob_vals[0][i]< 0.1:
                if threshold1==0:
                    threshold1=prob_vals[1][i+1]
                    threshold2=prob_vals[1][i+1]
                else:
                    threshold2=prob_vals[1][i+1]

        if z%1==0:
            bin_classes=[]
        for i in range(0,len(max_dist)):
            if the_norms[i]>=threshold1 and the_norms[i]<=threshold2:
                bin_classes.append({'driver_trip':str(z)+"_"+str(i+1),'prob':0})
            else:
                bin_classes.append({'driver_trip':str(z)+"_"+str(i+1),'prob':1})
        #print bin_classes
        #print "success?"
        outpt=pd.DataFrame(data=bin_classes)
        #print "success2 "
        if z==1:
            outpt.to_csv(path_or_buf="/Users/vmac/PycharmProjects/kaggle-axa-driver-telematics/sampleOutz2.csv", index=False)
        else:
            q.put(outpt)
            #print "queue size ",q.qsize()
            #with open("/Users/vmac/PycharmProjects/kaggle-axa-driver-telematics/sampleOutz2.csv",'a') as f:
                #outpt.to_csv(f,header=False, index=False)
            #f.close()

        print "success ",z
    #sam.release()

def worker():
    while True:
        item = q.get()
        item.to_csv(f, header=False, index=False)
        q.task_done()
        #print "queue size ",q.qsize()

bin_classes=[]
f=[]

for z in range(2762,3613):#up to 3613
    #print "iteration ",z
    if z == 168:
        myFunc(z)
        f = open("/Users/vmac/PycharmProjects/kaggle-axa-driver-telematics/sampleOutz2.csv",'a')
        t=Thread(target=worker)
        t.daemon=True
        t.start()
    else:
        myFunc(z)
        #sam.acquire()
        #t=Thread(target=myFunc,args=(z,))
        #t.start()