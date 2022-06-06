# -*- coding: utf-8 -*-

"""
    
"""
class CCTFcase():
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
        self.max_n2 = int(initParams.max_n2)  # 冷冻水泵最大台数
        self.max_n3 = int(initParams.max_n3)  # 冷却水泵最大台数
        self.lengque_maxn = int(initParams.lengque_maxn)  # 冷却塔最大台数

        self.f_ts = initParams.f_ts  # 室外湿球温度
        self.f_bh_td = initParams.f_bh_td  # 板换温差
        self.f_bh_efficiency = initParams.f_bh_efficiency  # 板换效率
        self.f_min_load = initParams.f_min_load  # 最低负荷
        self.f_ct_td = initParams.f_ct_td  # 冷却塔温差
        self.f_w_td = initParams.f_w_td  # 供回水温差

        self.n2 = None  # 冷冻水泵台数
        self.n3 = None  # 冷却水泵台数

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
            temp = self.lengque_maxn / self.n3
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
        self.z = self.n3

        if self.selectType <= 4:
            self.z = self.z * self.selectType
        elif self.selectType == 5:
            self.z = self.z * 1.5
        else:
            self.z = self.z * 4 / 3