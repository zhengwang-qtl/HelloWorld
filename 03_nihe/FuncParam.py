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
    value += B[1] * T1
    value += B[2] * T2
    value += B[3] * Q;
    value += B[4] * Q * Q;
    value += B[5] * T1 * T1
    value += B[6] * T2 * T2
    value += B[7] * Q * T1
    value += B[8] * Q * T2
    value += B[9] * T1 * T2;
    value += B[10] * (T2 - T1)
    value += B[11] * T0 * vable;
    value += B[12] * (T2 - T1) * (T2 - T1);
    value += B[13] * T0 * T0;
    value += B[14] * Q * (T2 - T1);
    value += B[15] * Q * T0;
    value += B[16] * (T2 - T1) * T0;
    value += B[17] * (T0 - T1);
    return value

def makeZJline(i, vable):
    T2=i[0]
    T1=i[1]
    T0=i[2]
    Q=i[3]
    return np.array([1,T1,T2,Q,Q*Q,T1*T1,T2*T2,Q*T1,Q*T2,T1*T2,T2-T1,T0*vable,(T2-T1)*(T2-T1),T0*T0,Q*(T2-T1),Q*T0,(T2-T1)*T0,(T0-T1)])
    
def makeBadjust(b, vable) :
    b[11]=b[11] * vable
    return b