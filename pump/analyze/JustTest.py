import numpy as np

from scipy.optimize import curve_fit


class PumpFitting():
    def func_P2(self, G2, A0, A1, A2):
        '''
            :param G2: 自变量x
            :param A0: 待拟合参数
            :param A1:
            :param A2:
            :return:
            '''
        P2 = A0 + A1 * G2 + A2 * G2 * G2
        return P2

    def fit_P2(self, P2_data):
        temp_G2 = []
        temp_P2 = []

        for i in P2_data:
            temp_G2.append(i.g2)
            print(i.g2)
            temp_P2.append(i.p2)
            print(i.p2)
        G2 = np.array(temp_G2)
        P2 = np.array(temp_P2)
        a, b = curve_fit(self.func_P2, G2, P2)
        return a


def func_P2(G2, A0, A1, A2):
    P2 = A0 + A1 * G2 + A2 * G2 * G2
    return P2


def fit_P2(P2_data):
    temp_G2 = []
    temp_P2 = []
    for i in P2_data:
        temp_G2.append(i.g2)
        temp_P2.append(i.p2)
    G2 = np.array(temp_G2)
    P2 = np.array(temp_P2)
    a, b = curve_fit(func_P2, G2, P2)
    return a


class data:
    g2: float
    p2: float


if __name__ == '__main__':
    print("Hello world!")
    d1 = data()
    d1.g2 = 533.0
    d1.p2 = 78.0
    d2 = data()
    d2.g2 = 498.0
    d2.p2 = 56.8
    d3 = data()
    d3.g2 = 422.0
    d3.p2 = 39.9
    d4 = data()
    d4.g2 = 387.0
    d4.p2 = 26.8
    d5 = data()
    d5.g2 = 331.0
    d5.p2 = 16.8
    arr = [d1, d2, d3, d4, d5]
    print(fit_P2(arr))
    pf = PumpFitting()
    print(pf.fit_P2(arr))
