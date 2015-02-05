
from pylab import *
import matplotlib.pyplot as plt
import pandas as pd
import threading

class myThread (threading.Thread):
    def __init__(self, plott):
        threading.Thread.__init__(self)
        self.plott=plott
    def run(self):
        self.plott.show()



colors=['blue','green','red','cyan','magenta','black']
#fig = plt.figure(1)
#fign=plt.subplot(211, aspect='equal',xlim=[-20000,20000],ylim=[-20000,20000])
#ax = fig.add_axes([0.05, 0.05, 0.95, 0.95], polar=False)
#circle1 = plt.Circle((0,0),2000,fill=False)
#circle2 = plt.Circle((0,0),15000,fill=False)
    #t = linspace(0, 2 * pi, 100)
max_dist=[]
for i in range(1,201):
    vecs=pd.read_csv("/Users/vmac/Downloads/drivers/154/"+str(i)+".csv")
    #ax.plot(vecs['x'], vecs['y'], color=colors[i%6], lw=1)
    max_dist.append(0.0)
    for j in range(0,len(vecs)):
        local_dist=sqrt(vecs['y'][j]*vecs['y'][j]+vecs['x'][j]*vecs['x'][j])
        if max_dist[i-1]<local_dist:
            max_dist[i-1]=local_dist
#fig.gca().add_artist(circle1)
#fig.gca().add_artist(circle2)
    #thread1 = myThread(plt)
    #thread1.start()
#plt.show()
#fig2 = plt.figure(2)
#plt.subplot(212)
#plt.hist(max_dist, bins=10, normed=True)

#fig3 = plt.figure(3)
#plt.hist(max_dist,bins=10,cumulative=True, normed=True)
#plt.show()
prob_vals = hist(max_dist, bins=10,cumulative=True,normed=True)

print prob_vals[0], prob_vals[1]
threshold1=0
threshold2=0
for i in range(0,len(prob_vals[0])-1):
    print prob_vals[0][i+1]-prob_vals[0][i]
    if prob_vals[0][i+1]-prob_vals[0][i]< 0.1:
        if threshold1==0:
            threshold1=prob_vals[1][i]
        else:
            threshold2=prob_vals[1][i]
print threshold1, threshold2
#print hist(max_dist,bins=10,cumulative=True, normed=True)
#print hist(max_dist,bins=10,cumulative=False, normed=True)

    #thread1.join()

#if __name__ == '__main__':
#    main()