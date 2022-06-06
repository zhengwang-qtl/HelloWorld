# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""

"""


class ACHPRcase(ea.Problem):
    def __init__(self, Q, TS, initParams, fitting):
        self.A = fitting.A
        self.K = fitting.K

        self.yuzhi = initParams.yuzhi
        self.G20 = float(initParams.G20)  # G2额定功率
        self.u1 = float(initParams.mu)  # G2限定值
        self.P20 = float(initParams.p20)
        self.t2_tuple = (float(initParams.delta_t1_range[0]), float(initParams.delta_t1_range[1]))  # t2与t1差值的范围
        self.Q = float(Q)  # 负荷Q
        self.TS = float(TS)  # 室外干球温度
        self.QS = float(initParams.q)  # 单台额定冷水机组负荷QS
        self.nita = float(initParams.efficiency_range)  # 单台高效率冷负荷范围η
        self.max_n = float(initParams.n)  # 最大台数
        self.T1_range = initParams.ACHP_r_t1_range
        self.load_rat = initParams.ACHP_r_load_rate

        self.n = None  # 台数

        self.T1 = None  # 根据计算选取固定T1，之后的进化T2都是在此基础浮动

        #  判断是否需要优化计算
        self.q_min = float(initParams.refrigeration_q_min)  # 制热最低负荷Qq,Kw
        self.ifopt = True

        if self.q_min > Q:
            self.ifopt = False
        else:
            self.ifopt = True

        #  计算T1
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
            if i * float(self.nita) < Q * 100 / self.QS <= (i + 1) * float(self.nita):
                self.n = i + 1
                break
        if self.n is None:
            self.n = int(self.max_n)

        self.n = min(self.n, self.max_n)

        self.Q = self.Q / self.n

        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）

        T2_MIN = self.t2_tuple[0] + self.T1
        T2_MAX = self.t2_tuple[1] + self.T1

        Dim = 2  # 初始化Dim（决策变量维数） T2 和 T4
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [T2_MIN]  # 决策变量下界
        ub = [T2_MAX]  # 决策变量上界
        lbin = [1, 1]  # 决策变量下边界
        ubin = [1, 1]  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        T2 = pop.Phen[:, [0]]  # 获取表现型矩阵的第一列，得到所有个体的x1的值
        T1 = np.ones(len(T2)) * self.T1
        T1 = T1.reshape((-1, 1))

        Q = self.Q
        K = self.K
        T0 = self.TS
        P1 = K[0] + K[1] * T1 + K[2] * T2 + K[3] * Q + K[4] * Q * Q + K[5] * T1 * T1 + K[6] * T2 * T2 + K[7] * Q * T1 + \
             K[8] * Q * T2 + K[9] * T1 * T2 + K[10] * (T2 - T1) + K[11] * T0 + K[12] * (T2 - T1) * (T2 - T1) + K[
                 13] * T0 * T0 + K[14] * Q * (T2 - T1) + K[15] * Q * T0 + K[16] * (T2 - T1) * T0 + K[17] * (T0 - T1)

        edIdx_P1 = np.where(P1 < 0)[0]

        A = self.A
        G2 = 6 * Q / (7 * (T2 - T1))

        for index in range(len(G2)):
            G2[index][0] = max(G2[index][0], self.G20 * self.u1)
            G2[index][0] = min(G2[index][0], self.G20)

        P2 = A[0] + A[1] * G2 + A[2] * G2 * G2

        P = self.n * (P1 + P2)

        alpha = 10000  # 惩罚缩放因子
        beta = 10  # 惩罚最小偏移量
        P[edIdx_P1] += self.maxormins[0] * alpha * (np.max(P) - np.min(P) + beta)
        pop.ObjV = P
