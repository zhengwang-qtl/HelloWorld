import numpy as np
from numba import jit,float64

@jit("float64(float64[:], float64[:], float64)")
def makeZJvirtualPLine(I, B, vable) :
    T2=I[0]
    T1=I[1]
    T0=I[2]
    Q=I[3]
    value = 0
    value += B[0]
    value += B[1] * T1* vable
    value += B[2] * Q
    value += B[3] * Q * Q
    value += B[4] * T1 * T1
    value += B[5] * Q * T1
    value += B[6] * T0 
    value += B[7] * T0 * T0
    value += B[8] * Q * T0
    value += B[9] * (T1 -T0)
    return value

def makeZJline(i, vable):
    T2=i[0]
    T1=i[1]
    T0=i[2]
    Q=i[3]
    return np.array([1,T1*vable,Q,Q*Q,T1*T1,Q*T1,T0,T0*T0,Q*T0,T1-T0])
    
def makeBadjust(b, vable) :
    b[1]=b[1] * vable
    return b