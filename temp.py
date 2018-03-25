import numpy as np

import matplotlib.pyplot as plt

import matplotlib.mlab as mlab

import math

class_num = 27
classes = []
data = []
data2 = []
ydata = []
ydata2 = []

fin = open('./count.txt')
lines = fin.readlines()
fin.close()

for l in lines:
    l = l.strip('\r\n').split(':')
    classes.append(l[0])
    data.append(int(l[1]))

fin = open('./count1.txt')
lines = fin.readlines()
fin.close()

for l in lines:
    l = l.strip('\r\n').split(':')
    data2.append(int(l[1]))

plt.style.use( 'ggplot')


plt.figure(figsize = (35,20))


for d in data:
    ydata.append(math.log(d,10) if d>0 else 0)
for d in data2:
    ydata2.append(math.log(d,10) if d>0 else 0)

xdata = np.arange(class_num)


p1 = plt.barh(xdata, ydata, edgecolor = 'black')
p2 = plt.barh(xdata, ydata2 ,hatch='/',edgecolor = 'black',facecolor = 'none')    



plt.yticks(xdata+0.5 , classes , size=28,color='black')
plt.xticks([0,1,2,3,4,5],['0','10','10^2','10^3','10^4','10^5'],size =28,color='black')
plt.tick_params(top= 'off', right= 'off')

plt.grid(axis= 'y')

plt.ylabel('classes',size=35,color='black')
plt.xlabel('# of images',size=35,color='black')

plt.subplots_adjust(left = 0.18,bottom = 0.1,top =0.99,right = 0.98)

for i in range(27):
    plt.text(ydata[i]+0.1, i+0.15,str(data[i]), ha='center', va= 'bottom',fontsize=28)
for i in range(27):
    if data2[i] != 0 and data2[i] != data[i]:
        plt.text(ydata2[i]+0.1, i+0.15,str(data2[i]), ha='center', va= 'bottom',fontsize=28)
       

plt.legend((p1[0],p2[0]),('original sample','adjusted sample'),fontsize = 30)

plt.savefig('test1.pdf',dpi=150)
#plt.show()






'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()