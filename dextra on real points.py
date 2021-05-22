import matplotlib.pyplot as plt
from math import atan
import time

def dextra(points, conn, begPoint, endPoint):
    p = points
    for c in conn:
        d =((p[c[0]][0] - p[c[1]][0])**2 + ( p[c[0]][1] - p[c[1]][1] ) **2)**(0.5)
        c.append(d)
    w = []
    v = []
    for i in p:
        v.append(False)
        w.append(1e10)
    pc = len(p)
    s = []
    beg =begPoint[2]
    v[beg] = True
    w[beg] = 0
    i=beg  # starting point
    fw = [w[:]]
    while pc>0:
        for c in conn:
            if (c[0]==i) or (c[1]==i):
                t = 0
                if c[0]==i:
                    t = c[1]
                else:
                    t = c[0]
                if v[t] == False:
                    d = w[i] + c[2]
                    if d<w[t]:
                        w[t] = d
        s.append(i)
        pc -= 1
        v[i]  = True
        m = max(w)
        for r in range(len(p)):
            if v[r] == False:
                if m>w[r]:
                    m = w[r]
                    i = r
        fw.append(w[:])
    end = endPoint[2]
    e = end
    print('path from ',str(beg), ' to ', str(end), ' is:')
    path = [e]
    for n in range(len(p)-1,0,-1):
        if(fw[n][e] != fw[n-1][e]):
            e = s[n-1]
            path.append(e)
    path.reverse()
    return path

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) **0.5




def findClosest(point, points):
    if len(points) == 0:
        return None
    mn = dist(points[0],point)
    mp = points[0]
    for p in points:
        d = dist(p,point)
        if d < mn:
            mn = d
            mp = p
    return mp


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 100])
ax.set_ylim([0, 100])
p = []
rp = []
conn = []
pointNum = 0
begPoint = None
endPoint = None
done = False
def onclick(event):
    global pointNum
    global rp
    global conn
    global begPoint
    global endPoint
    global done
    global p

    if done == True:
        plt.clf()
        p = []
        rp = []
        conn = []
        pointNum = 0
        begPoint = None
        endPoint = None
        done = False
        ax = fig.add_subplot(111)
        ax.set_xlim([0, 100])
        ax.set_ylim([0, 100])
        fig.canvas.draw()


    if event.button == 1:  # right click mouse
        plt.plot(event.xdata, event.ydata, 'ro')
        p.append([event.xdata, event.ydata, pointNum])
        plt.text(event.xdata+1, event.ydata+1,str(pointNum+1), fontsize =10)
        pointNum += 1
    elif event.button == 3:  # left click mouse
        begPoint = None
        endPoint = None
        pp = findClosest([event.xdata, event.ydata], p)
        if pp !=  None:
            if len(rp) == 0 :
                plt.plot(pp[0], pp[1], 'bX')
                rp.append(pp)
            elif pp != rp[0]:
                a = rp[0][2]
                b = pp[2]
                print(f'a={a}  b={b}')
                print(conn)
                for el in conn:
                    if (el[0]==a and el[1]==b) or (el[0]==b and el[1]==a):
                        rp=[]
                        break
                if len(rp)!=0:
                    conn.append([a,b])
                    plt.plot(pp[0], pp[1], 'bX')
                    plt.plot([pp[0],rp[0][0]],[pp[1],rp[0][1]])
                    rp = []
    elif event.button == 2:  # scroll button pressed
        if begPoint is None:
            begPoint = findClosest([event.xdata, event.ydata], p)
            plt.plot(begPoint[0], begPoint[1],'rs',markersize=10)
        elif endPoint is None:
            endPoint = findClosest([event.xdata, event.ydata], p)
            plt.plot(endPoint[0], endPoint[1],'rs',markersize=10)
            shortestPath = dextra(p,conn,begPoint, endPoint)
            s = ''
            for i in range(len(shortestPath)-1):
                plt.plot([p[shortestPath[i]][0],p[shortestPath[i+1]][0]],[p[shortestPath[i]][1],p[shortestPath[i+1]][1]],
                         color='red',linewidth=5)
                s += str(shortestPath[i]+1) + ' ==> '
                plt.text(10, 10,s, fontsize =10)
                fig.canvas.draw()
                time.sleep(15)
            s += str(shortestPath[-1]+1)
            plt.text(10, 10, s, fontsize =10)
            done =True
    fig.canvas.draw()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()








