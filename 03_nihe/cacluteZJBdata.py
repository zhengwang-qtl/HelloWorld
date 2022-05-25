import numpy as np
from numba import jit

def cacluteZJBdata(x, p) :
    xT=x.T
    xTx=np.dot(xT,x)
    xTx_inv=np.linalg.inv(xTx)
    xTx_inv_xT=np.dot(xTx_inv,xT)
    b=np.dot(xTx_inv_xT,p)
    return b

def loadx(fname) :
    return np.loadtxt(fname,dtype=np.float,delimiter='\t',skiprows=0,usecols=(0,1,2,3),unpack=False)
    
def loadp(fname) :
    return np.loadtxt(fname,dtype=np.float,delimiter='\t',skiprows=0,usecols=(4),unpack=False)

def makeZJP(fname) :
    return loadp(fname)
    
def makeZJX(Fun, fname, vable) :
    x = loadx(fname)
    return makeX(x.tolist(),Fun, vable)
    
def makeX(xlist, Fun, vable):
    k=0
    a=[]
    size=0
    for i in xlist:
        b = Fun.makeZJline(i, vable)
        a = np.insert(a, k, b, axis=0)
        size=len(b)
        k=k+len(b)
    return a.reshape(len(xlist),size)
    
def makeZJvirtualP(Fun, xlist, B, vable):
    k=0
    a=[]
    size=0
    for i in xlist:
        b = Fun.makeZJvirtualPLine(i, B, vable)
        a = np.append(a, b)
    return a
    
@jit("float64(float64[:], float64[:])")
def makeMAPE(real, virtual):
    n=len(real)
    allsum=0
    for i in range(n):
        allsum += abs((real[i] - virtual[i])/virtual[i])
    allsum *= 100.0
    allsum /= n
    return allsum

@jit("float64(float64[:], float64[:])")
def makeMSE(real, virtual) :
    n=len(real)
    allsum=0
    for i in range(n):
        allsum += (real[i] - virtual[i])*(real[i] - virtual[i])
    allsum /= n
    return allsum
 
 
def makeDepthOptimizetion(Fun, x, p) :
    curk=1
    min=15
    tmpb=[]
    for k in range(1, 100000):
        vable = 0.00001 * k;
        try:
            b = cacluteZJBdata(makeX(x.tolist(), Fun, vable), p)
            pi = makeZJvirtualP(Fun, x, b, vable)
            if(makeMAPE(p, pi) < min):
                min = makeMAPE(p, pi) 
                curk = vable
                tmpb = b
        except Exception:
            A=0
        else:
            A=1
        if(k %10000 == 0) :
            print(k,'min:',min,'curk:', curk)
            
    tmpb = Fun.makeBadjust(tmpb, curk)
    pi = makeZJvirtualP(Fun, x, tmpb, 1)
    return makeMAPE(p, pi), makeMSE(p,pi), tmpb