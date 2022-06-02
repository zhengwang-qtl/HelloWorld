# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea

"""
    
"""


class CCTFcase(ea.Problem):
    def __init__(self, Q, TS, initParams, fitting):
        self.A = fitting.A
        self.C = fitting.C

        self.D_1to1 = fitting.D_1to1
        self.D_2to1 = fitting.D_2to1
        self.D_3to1 = fitting.D_3to1
        self.D_4to1 = fitting.D_4to1
        self.D_3to2 = fitting.D_3to2
        self.D_4to3 = fitting.D_4to3
        self.typeToD = {1: self.D_1to1, 2: self.D_2to1, 3: self.D_3to1, 4: self.D_4to1, 5: self.D_3to2, 6: self.D_4to3}

        self.E = fitting.E

        self.selectType = initParams.calcType
        self.yuzhi = initParams.yuzhi
        self.G20 = float(initParams.G20)  # G2额定流量
        self.u1 = float(initParams.mu)  # 冷冻水泵变频频率下限值μ
        self.P20 = float(initParams.p20)
        self.G30 = float(initParams.G30)  # G3额定流量
        self.u2 = float(initParams.lamb)  # 冷却水泵频率下限值λ
        self.t3_min = float(initParams.t3_min)
        self.t2_tuple = (float(initParams.delta_t1_range[0]), float(initParams.delta_t1_range[1]))  # t2与t1差值的范围
        self.t4_tuple = (float(initParams.delta_t2_range[0]), float(initParams.delta_t2_range[1]))  # t4与t3差值的范围
        self.P0 = float(initParams.P0)  # 一定条件下P4=P0
        self.Q = float(Q)  # 负荷Q
        self.TS = float(TS)  # 湿球温度
        self.max_n2 = float(initParams.max_n2)  # 冷冻水泵最大台数
        self.max_n3 = float(initParams.max_n3)  # 冷却水泵最大台数
        self.lengque_maxn = initParams.lengque_maxn  # 冷却塔最大台数
        self.T1_range = initParams.t1_range  # ？？？
        self.load_rat = initParams.load_rat

        self.f_ts = initParams.f_ts  # 室外湿球温度
        self.f_bh_td = initParams.f_bh_td  # 板换温差
        self.f_bh_efficiency = initParams.f_bh_efficiency  # 板换效率
        self.f_min_load = initParams.f_min_load  # 最低负荷
        self.f_ct_td = initParams.f_ct_td  # 冷却塔温差
        self.f_w_td = initParams.f_w_td  # 供回水温差

        self.n2 = None  # 冷冻水泵台数
        self.n3 = None  # 冷却水泵台数
        self.T1 = None  # 根据计算选取固定T1，之后的进化T2都是在此基础浮动

        # TODO  计算方式的比对，以及思考可能的借鉴？(怎么计算，这是待思考的。)
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

        # 计算开启冷冻水泵台数
        G2 = 6 * Q / (7 * self.f_w_td)
        n = G2 / self.G20
        for i in range(int(self.max_n2)):
            if (i + 1) * self.u1 <= n < (i + 2) * self.u1:
                self.n2 = i + 1
                break
        if self.n2 is None:
            if n < self.u1:
                self.n2 = 1
            else:
                self.n2 = self.max_n2

        # 计算开启冷却水泵台数
        G3 = 6 * Q / (self.f_bh_efficiency * 7 * self.f_w_td)
        m = G3 / self.G30
        for i in range(int(self.max_n3)):
            if (i + 1) * self.u2 <= m < (i + 2) * self.u2:
                self.n3 = i + 1
                break
        if self.n3 is None:
            if m < self.u2:
                self.n3 = 1
            else:
                self.n3 = self.max_n3


        # 计算T3
        if self.selectType == 0:
            temp = self.lengque_maxn / self.n2
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

        # 计算z
        self.z = self.n2

        if self.selectType <= 4:
            self.z = self.z * self.selectType
        elif self.selectType == 5:
            self.z = self.z * 1.5
        else:
            self.z = self.z * 4 / 3

        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）

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

        A = self.A
        G2 = 6 * Q / (7 * (T2 - T1))

        for index in range(len(G2)):
            G2[index][0] = max(G2[index][0], self.G20 * self.u1)
            G2[index][0] = min(G2[index][0], self.G20)

        P2 = A[0] + A[1] * G2 + A[2] * G2 * G2
        edIdx_P2 = np.where(P2 < 0)[0]

        G3 = 6 * (Q + P1) / (7 * (T4 - T3))  #TODO G3的计算
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

        P = self.n2*P2 + self.n3*P3 + self.z * P4

        alpha = 10000  # 惩罚缩放因子
        beta = 10  # 惩罚最小偏移量
        P[edIdx_P2] += self.maxormins[0] * alpha * (np.max(P) - np.min(P) + beta)
        pop.ObjV = P
