# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from analyze.schema import *

"""
    
"""


class CCTcase(ea.Problem):
    def __init__(self, Q, TS, Init: Init, Params):
        arr_A = []
        arr_A.append(Params.chilled_water_pump.min_first.A0)
        arr_A.append(Params.chilled_water_pump.min_first.A1)
        arr_A.append(Params.chilled_water_pump.min_first.A2)

        arr_B = []
        arr_B.append(Params.chiller.min.B0)
        arr_B.append(Params.chiller.min.B1)
        arr_B.append(Params.chiller.min.B2)
        arr_B.append(Params.chiller.min.B3)
        arr_B.append(Params.chiller.min.B4)
        arr_B.append(Params.chiller.min.B5)
        arr_B.append(Params.chiller.min.B6)
        arr_B.append(Params.chiller.min.B7)
        arr_B.append(Params.chiller.min.B8)
        arr_B.append(Params.chiller.min.B9)
        arr_B.append(Params.chiller.min.B10)
        arr_B.append(Params.chiller.min.B11)
        arr_B.append(Params.chiller.min.B12)
        arr_B.append(Params.chiller.min.B13)
        arr_B.append(Params.chiller.min.B14)
        arr_B.append(Params.chiller.min.B15)
        arr_B.append(Params.chiller.min.B16)
        arr_B.append(Params.chiller.min.B17)
        arr_B.append(Params.chiller.min.B18)
        arr_B.append(Params.chiller.min.B19)
        arr_B.append(Params.chiller.min.B20)
        arr_B.append(Params.chiller.min.B21)
        arr_B.append(Params.chiller.min.B22)
        arr_B.append(Params.chiller.min.B23)

        arr_C = []
        arr_C.append(Params.cooling_water_pump.min.C0)
        arr_C.append(Params.cooling_water_pump.min.C1)
        arr_C.append(Params.cooling_water_pump.min.C2)

        arr_D_1to1 = []
        arr_D_2to1 = []
        arr_D_3to1 = []
        arr_D_4to1 = []
        arr_D_3to2 = []
        arr_D_4to3 = []
        for s in Params.cooling_tower.min.cooling_amplitude_s:
            if s.type == "1to1":
                arr_D_1to1.append(s.D0)
                arr_D_1to1.append(s.D1)
                arr_D_1to1.append(s.D2)
            elif s.type == "2to1":
                arr_D_2to1.append(s.D0)
                arr_D_2to1.append(s.D1)
                arr_D_2to1.append(s.D2)
            elif s.type == "3to1":
                arr_D_3to1.append(s.D0)
                arr_D_3to1.append(s.D1)
                arr_D_3to1.append(s.D2)
            elif s.type == "4to1":
                arr_D_4to1.append(s.D0)
                arr_D_4to1.append(s.D1)
                arr_D_4to1.append(s.D2)
                arr_D_4to1.append(s.D3)
            elif s.type == "3to2":
                arr_D_3to2.append(s.D0)
                arr_D_3to2.append(s.D1)
                arr_D_3to2.append(s.D2)
            else:  # 4to3
                arr_D_4to3.append(s.D0)
                arr_D_4to3.append(s.D1)
                arr_D_4to3.append(s.D2)

        arr_E = []
        arr_E.append(Params.cooling_tower.min.power.E0)
        arr_E.append(Params.cooling_tower.min.power.E1)
        arr_E.append(Params.cooling_tower.min.power.E2)
        arr_E.append(Params.cooling_tower.min.power.E3)

        self.A = arr_A
        self.B = arr_B
        self.C = arr_C

        self.D_1to1 = arr_D_1to1
        self.D_2to1 = arr_D_2to1
        self.D_3to1 = arr_D_3to1
        self.D_4to1 = arr_D_4to1
        self.D_3to2 = arr_D_3to2
        self.D_4to3 = arr_D_4to3
        self.typeToD = {1: self.D_1to1, 2: self.D_2to1, 3: self.D_3to1, 4: self.D_4to1, 5: self.D_3to2, 6: self.D_4to3}

        self.E = arr_E

        calcType = Init.cooling_tower.min.calcType
        if calcType == "1to1":
            self.selectType = 1
        elif calcType == "2to1":
            self.selectType = 2
        elif calcType == "3to1":
            self.selectType = 3
        elif calcType == "4to1":
            self.selectType = 4
        elif calcType == "3to2":
            self.selectType = 5
        elif calcType == "4to3":
            self.selectType = 6
        else:
            self.selectType = 0

        self.yuzhi = Init.basic.optimize_calculation_set_value
        self.G20 = Init.chilled_water_pump.min_first.g20  # G2额定功率
        self.u1 = Init.chilled_water_pump.min_first.u/50  # G2限定值 u频率 50hz 公频
        self.P20 = Init.chilled_water_pump.min_first.p20
        self.G30 = Init.cooling_water_pump.min.g30  # G3额定功率
        self.u2 = Init.cooling_water_pump.min.u/50  # G3限定值 u频率 50hz 公频
        self.t3_min = Init.chiller.min.t3_min
        self.t2_tuple = (
        Init.basic.first_chilled_water_t_range[0], Init.basic.first_chilled_water_t_range[1])  # t2与t1差值的范围
        self.t4_tuple = (Init.basic.cooling_water_t_range[0], Init.basic.cooling_water_t_range[1])  # t4与t3差值的范围
        self.P0 = Init.cooling_tower.min.p0  # 一定条件下P4=P0
        self.Q = float(Q)  # 负荷Q
        self.TS = float(TS)  # 湿球温度
        self.QS = Init.chiller.min.q  # 单台额定冷水机组负荷
        self.nita = Init.chiller.min.efficiency_range  # 单台高效率冷负荷范围η
        self.max_n = Init.chiller.min.n  # 最大台数
        self.lengque_maxn = Init.cooling_tower.min.max_n  # 冷却塔的最大台数
        t1_range = []
        load_rate = []
        for item in Init.chiller.load_rate_with_t_c:
            t1_range.append(item.cold_out_first_t)
            load_rate.append(item.load_rate)
        self.T1_range = t1_range
        self.load_rat = load_rate

        self.n = None  # 台数

        self.T1 = None  # 根据计算选取固定T1，之后的进化T2都是在此基础浮动

        #  判断是否需要优化计算
        self.q_min = float(Init.chiller.min.q_min)  # 单台冷水机组最低负荷Qq,Kw
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

        # 计算T3
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
        else:
            if self.selectType <= 4:
                self.z = self.n * self.selectType
            elif self.selectType == 5:
                self.z = self.n * 1.5
            else:
                self.z = self.n * 4 / 3
            while self.z > self.lengque_maxn and self.selectType != 1:
                if self.selectType <= 4:
                    self.selectType -= 1
                    self.z = self.n * self.selectType
                else:
                    self.selectType = 1
                    self.z = self.n

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

        if self.T3 < self.t3_min:
            self.T3 = self.t3_min
        """
        self.z = None
        for i in range(int(self.max_n)):
            if i < Q / self.QS <= (i + 1):
                self.z = i + 1
                break
        if self.z is None:
            self.z = int(self.max_n)
        """
        # 计算z
        if self.selectType <= 4:
            self.z = self.n * self.selectType
        elif self.selectType == 5:
            self.z = self.n * 1.5
        else:
            self.z = self.n * 4 / 3

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
