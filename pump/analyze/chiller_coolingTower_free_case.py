# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from analyze.schema import *

"""

"""


class CCTFcase:
    def __init__(self, Q, TS, Init: Init, Params):
        arr_A = []
        arr_A.append(Params.chilled_water_pump.min_first.A0)
        arr_A.append(Params.chilled_water_pump.min_first.A1)
        arr_A.append(Params.chilled_water_pump.min_first.A2)

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

        self.G20 = Init.chilled_water_pump.min_first.g20  # G2额定功率
        self.u1 = Init.chilled_water_pump.min_first.u / 50  # G2限定值 u频率 50hz 公频
        self.P20 = Init.chilled_water_pump.min_first.p20
        self.G30 = Init.cooling_water_pump.min.g30  # G3额定功率
        self.u2 = Init.cooling_water_pump.min.u / 50  # G3限定值 u频率 50hz 公频
        self.Q = float(Q)  # 负荷Q
        self.TS = float(TS)  # 湿球温度
        self.lengque_maxn = Init.cooling_tower.min.max_n  # 冷却塔的最大台数
        self.max_n = Init.chilled_water_pump.min_first.max_n2  # 冷却水泵得最大台数

        self.QS = Init.chiller.min.q  # 单台额定冷水机组负荷

        ###
        self.ts = Init.cooling_tower_free_calculation.ts  # 室外湿球温度
        self.bh_td = Init.cooling_tower_free_calculation.bh_td  # 板换温差 1.5
        self.bh_efficiency = Init.cooling_tower_free_calculation.bh_efficiency / 100  # 板换效率
        self.min_load = Init.cooling_tower_free_calculation.min_load  # 最低负荷
        self.w_td = Init.cooling_tower_free_calculation.w_td  # 供回水温差
        self.ct_lqc_hswd = Init.cooling_tower_free_calculation.ct_lqc_hswd  # 冷却塔冷却侧回水温度 (T4)
        self.ct_gsc_hswd = Init.cooling_tower_free_calculation.ct_gsc_hswd  # 冷却塔供水侧回水温度 (T2) 17
        self.unite_ts = Init.cooling_tower_free_calculation.unite_ts  # 主机与冷却塔联合供冷室外湿球温度
        self.ct_td = Init.cooling_tower_free_calculation.ct_td  # 冷却塔温差

        G2 = 6 * Q / (7 * self.w_td)
        m = G2 / self.G20
        print(Q, self.G20, G2, self.w_td, self.max_n)
        self.n = self.max_n  # 冷冻水泵开启台数
        for i in range(int(self.max_n + 1)):
            if i * self.u1 > m:
                self.n = i - 1
                break
        if self.n < 1:
            self.n = 1
        self.z = self.n

        self.Q = self.Q / self.n

        self.autoCalc = False
        # 计算T3
        if self.selectType == 0:
            self.autoCalc = True
            temp = self.lengque_maxn / self.n
            if temp >= 4:
                self.selectType = 4
            elif temp >= 3:
                self.selectType = 3
            elif temp >= 2:
                self.selectType = 2
            elif temp >= 3 / 2:
                self.selectType = 5
            elif temp >= 4 / 3:
                self.selectType = 6
            else:
                self.selectType = 1
        self.freshZ()
        while self.z > self.lengque_maxn and self.selectType != 1:
            if self.selectType <= 4:
                self.selectType -= 1
            else:
                self.selectType = 1

        self.shouldOp = True
        self.T3 = 0
        if self.autoCalc is True:
            self.maxSelectType = self.selectType
            self.selectType = 1
            while self.selectType <= self.maxSelectType:
                self.getT3()
                if self.ct_gsc_hswd - self.bh_td - self.w_td >= self.T3:
                    self.shouldOp = False
                    break
                if self.maxSelectType > 4:
                    if self.selectType == self.maxSelectType :
                        break
                    else :
                        self.selectType = self.maxSelectType
                else:
                    self.selectType = self.selectType + 1
        else:
            self.getT3()
            if self.ct_gsc_hswd - self.bh_td - self.w_td >= self.T3:
                self.shouldOp = False
        print("shouldOP:", self.shouldOp, self.ct_gsc_hswd, self.bh_td, self.w_td, self.T3)
        print("ct num:", self.selectType, self.n, self.z)

    def getT3(self):
        if self.selectType == 4:
            D0, D1, D2, D3 = self.typeToD[self.selectType]
            self.T3 = self.TS + D0 + D1 * self.TS + D2 * self.TS * self.TS + D3 * self.TS * self.TS * self.TS
        else:
            D0, D1, D2 = self.typeToD[self.selectType]
            self.T3 = self.TS + D0 + D1 * self.TS + D2 * self.TS * self.TS
        self.freshZ()

    def freshZ(self):
        if self.selectType <= 4:
            self.z = self.n * self.selectType
        elif self.selectType == 5:
            self.z = self.n * 1.5
        else:
            self.z = self.n * 4 / 3
