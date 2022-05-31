# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""

    目标：max f = 21.5 + x1 * np.sin(4 * np.pi * x1) + x2 * np.sin(20 * np.pi * x2)
    约束条件：
        6<T1<10
        10<T2<20
        21<T3<33
        25<T4<39

            # 4 < T2 - T1 < 10       （4）
            # 4 < T4 - T3 < 6；    （5）

        P1=B0+B1*T1+B2*T2+B3*Q+B4*Q*Q+B5*T1*T1+B6*T2*T2+B7*Q*T1+B8*Q*T2+B9*T1*T2+B10*T3+B11*T4+B12*T3*T3+B13*T4*T4+B14*Q*T3+B15*Q*T4+B16*T3*T4+B17*(T2-T1)+B18*(T4-T3)+B19*(T2-T1)*(T2-T1)+B20*(T4-T3)*(T4-T3)+B21*Q*(T2-T1)+B22*Q*(T4-T3)+B23*(T2-T1)*(T4-T3)。

        G2=Q/(4.2*(T2-T1)*1000)
        P2=A0+A1*G2+A2*G2*G2。

        G3=(Q+P1)/(4.2*(T4-T3)*1000)
        P3=C0+C1*G3+C2*G3*G3

        P4=69.8978*(P1+Q)/(T4-T3)*(P1+Q)/(T4-T3)+83.7279*(P1+Q)/(T4-T3)+0.1554。

        Minf(P)=P1+P2+P3+P4；
————————————————
版权声明：本文为CSDN博主「Strong_wind」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_37790882/article/details/84034956
"""

class CCTcase(ea.Problem):  # 继承Problem父类
    def __init__(self, Q, TS, superP, fittingP):
        self.B = fittingP.B
        self.A = fittingP.A
        self.C = fittingP.C
        self.D_1to1 = fittingP.D_1to1
        self.D_2to1 = fittingP.D_2to1
        self.D_3to1 = fittingP.D_3to1
        self.D_4to1 = fittingP.D_4to1
        self.D_3to2 = fittingP.D_3to2
        self.D_4to3 = fittingP.D_4to3

        self.typeToD = {1: self.D_1to1, 2: self.D_2to1, 3: self.D_3to1, 4: self.D_4to1, 5: self.D_3to2, 6: self.D_4to3}

        self.E = fittingP.E
        self.selectType = superP.calcType
        self.yuzhi = superP.yuzhi

        # 参数初始值============================
        self.G20 = float(superP.G20)  # G2额定功率
        self.u1 = float(superP.mu)  # G2限定值

        self.G30 = float(superP.G30)  # G3额定功率
        self.u2 = float(superP.lamb)  # G3限定值
        self.t3_min = float(superP.t3_min)
        self.t2_tuple = (float(superP.delta_t1_range[0]), float(superP.delta_t1_range[1]))  # t2 与 t1 的范围

        self.t4_tuple = (float(superP.delta_t2_range[0]), float(superP.delta_t2_range[1]))  # t4 与 t3 的范围
        self.P0 = float(superP.P0)  # 一定条件下P4=P0
        self.Q = float(Q)  # 负荷Q
        self.TS = float(TS)  # 湿球温度
        self.QS = float(superP.q)  # 单台额定冷水机组负荷QS
        self.nita = float(superP.efficiency_range)  # η
        self.max_n = float(superP.n)  # 最大台数
        self.lengque_maxn = superP.lengque_maxn
        self.n = None  # 台数
        self.T1_range = superP.t1_range
        self.load_rat = superP.load_rat

        self.T1 = None  # 根据计算选取固定T1，之后的进化T2都是在此基础浮动

        self.q_min = float(superP.q_min)
        self.ifopt = True

        if self.q_min > Q:
            self.ifopt = False
        else:
            self.ifopt = True
        self.P20 = float(superP.p2)

        # 除了计算T1温度时按照原本Q，其他都要Q/n
        temp = ((self.Q) * 100) / (self.QS * self.max_n)
        for index in range(len(self.load_rat)):
            if index == len(self.load_rat) - 1:
                self.T1 = float(self.T1_range[index])
                break

            if (temp < self.load_rat[index] or temp == self.load_rat[index]) and temp > self.load_rat[index + 1]:
                if temp - self.load_rat[index + 1] < self.load_rat[index] - temp:
                    self.T1 = float(self.T1_range[index])
                else:
                    self.T1 = float(self.T1_range[index])
                break

        for i in range(int(self.max_n)):
            if Q * 100 / self.QS > i * float(self.nita) and Q * 100 / self.QS <= (i + 1) * float(self.nita):
                self.n = i + 1
                break
        if self.n is None:
            self.n = int(self.max_n)

        self.n = min(self.n, self.max_n)

        self.Q = self.Q / self.n

        if self.selectType == 0:
            temp = self.lengque_maxn / self.n
            if temp == 1:
                self.selectType = 1
            elif temp == 2:
                self.selectType = 2
            elif temp == 3:
                self.selectType = 3
            elif temp == 4:
                self.selectType = 4
            elif temp == 3 / 2:
                self.selectType = 5
            elif temp == 4 / 3:
                self.selectType = 6
        D3 = 0
        if len(self.typeToD[self.selectType]) == 3:
            D0, D1, D2 = self.typeToD[self.selectType]
        else:
            D0, D1, D2, D3 = self.typeToD[self.selectType]

        self.T3 = self.TS + D0 + D1 * self.TS + D2 * self.TS * self.TS + D3 * self.TS * self.TS * self.TS

        while self.T3 < self.t3_min and self.selectType != 1:
            if self.selectType <= 4:  # 刚好等于4的情况下(4to1)，此时降为3（3to1），此时参数D就为3个
                self.selectType -= 1
                D0, D1, D2 = self.typeToD[self.selectType]
                self.T3 = self.TS + D0 + D1 * self.TS + D2 * self.TS * self.TS + D3 * self.TS * self.TS * self.TS
            else:
                # type=5,6 参数D一定为3个
                self.selectType = 1
                D0, D1, D2 = self.typeToD[self.selectType]
                self.T3 = self.TS + D0 + D1 * self.TS + D2 * self.TS * self.TS

        self.z = None
        for i in range(int(self.max_n)):
            if Q / self.QS > i and Q / self.QS <= (i + 1):
                self.z = i + 1
                break
        if self.z is None:
            self.z = int(self.max_n)

        if self.selectType <= 4:
            self.z = self.z * self.selectType
        elif self.selectType == 5:
            self.z = self.z * 1.5
        else:
            self.z = self.z * 4 / 3

        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        # 4 < T2 - T1 < 10     4+T1<T2<10+T1
        # 4 < T4 - T3 < 6      4+T3<T4<6+T3
        # 如果T3≧18（读入数据）度，P4=P0（22k），否则T3=18，P4==E0+E1*G3+E2*G3*G3+E3*G3*G3*G3

        T2_MIN = self.t2_tuple[0] + self.T1
        T2_MAX = self.t2_tuple[1] + self.T1

        T4_MIN = self.t4_tuple[0] + self.T3
        T4_MAX = self.t4_tuple[1] + self.T3

        Dim = 2  # 初始化Dim（决策变量维数） T2 和 T4
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [T2_MIN, T4_MIN]  # 决策变量下界
        ub = [T2_MAX, T4_MAX]  # 决策变量上界
        lbin = [1, 1]  # 决策变量下边界
        ubin = [1, 1]  # 决策变量上边界
        # 调用父类构造方法完成实例化

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        T2 = pop.Phen[:, [0]]  # 获取表现型矩阵的第一列，得到所有个体的x1的值
        T1 = np.ones(len(T2)) * self.T1
        T1 = T1.reshape((-1, 1))
        T4 = pop.Phen[:, [1]]
        T3 = np.ones(len(T2)) * self.T3
        T3 = T3.reshape((-1, 1))

        Q = self.Q
        B = self.B
        P1 = B[0] + B[1] * T1 + B[2] * T2 + B[3] * Q + B[4] * Q * Q + B[5] * T1 * T1 + B[6] * T2 * T2 + B[7] * Q * T1 + \
             B[8] * Q * T2 + B[9] * T1 * T2 + B[10] * T3 + B[11] * T4 + B[12] * T3 * T3 + B[13] * T4 * T4 + B[
                 14] * Q * T3 + B[15] * Q * T4 + B[16] * T3 * T4 + B[17] * (T2 - T1) + B[18] * (T4 - T3) + B[19] * (
                         T2 - T1) * (T2 - T1) + B[20] * (T4 - T3) * (T4 - T3) + B[21] * Q * (T2 - T1) + B[22] * Q * (
                         T4 - T3) + B[23] * (T2 - T1) * (T4 - T3)
        edIdx_P1 = np.where(P1 < 0)[0]

        A = self.A
        G2 = 6 * Q / (7 * (T2 - T1))

        for index in range(len(G2)):
            G2[index][0] = max(G2[index][0], self.G20 * self.u1)
            G2[index][0] = min(G2[index][0], self.G20)

        P2 = A[0] + A[1] * G2 + A[2] * G2 * G2

        G3 = 6 * (Q + P1) / (7 * (T4 - T3))
        for index in range(len(G3)):
            G3[index][0] = max(G3[index][0], self.G30 * self.u2)
            G3[index][0] = min(G3[index][0], self.G30)

        C = self.C
        P3 = C[0] + C[1] * G3 + C[2] * G3 * G3


        if self.T3 > self.t3_min:
            P4 = np.ones(len(T4)) * self.P0
            P4 = P4.reshape((-1, 1))
        else:
            E = self.E
            P4 = E[0] + E[1] * G3 + E[2] * G3 * G3 + E[3] * G3 * G3 * G3

        P = self.n * (P1 + P2 + P3) + self.z * P4

        alpha = 10000  # 惩罚缩放因子
        beta = 10  # 惩罚最小偏移量
        P[edIdx_P1] += self.maxormins[0] * alpha * (np.max(P) - np.min(P) + beta)
        pop.ObjV = P
