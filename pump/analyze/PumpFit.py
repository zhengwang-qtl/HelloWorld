import numpy as np

from scipy.optimize import curve_fit
import math


class PumpFitting():
    def __init__(self):
        # 拟合结果
        self.B = [1] * 24
        self.A = [1] * 3
        self.C = [1] * 3
        self.D_1to1 = [1] * 3
        self.D_2to1 = [1] * 3
        self.D_3to1 = [1] * 3
        self.D_4to1 = [1] * 4
        self.D_3to2 = [1] * 3
        self.D_4to3 = [1] * 3
        self.E = [1] * 4
        self.J = [1] * 10
        self.K = [1] * 18

        self.P1_x_data = None
        self.P1 = None

        self.P2_x_data = None
        self.P2 = None

        self.P3_x_data = None
        self.P3 = None

        self.Tdelta_x_data_1to1 = None
        self.Tdelta_1to1 = None

        self.Tdelta_x_data_2to1 = None
        self.Tdelta_2to1 = None

        self.Tdelta_x_data_3to1 = None
        self.Tdelta_3to1 = None

        self.Tdelta_x_data_4to1 = None
        self.Tdelta_4to1 = None

        self.Tdelta_x_data_3to2 = None
        self.Tdelta_3to2 = None

        self.Tdelta_x_data_4to3 = None
        self.Tdelta_4to3 = None

        self.P4_x_data = None
        self.P4 = None

        self.P5_x_data = None
        self.P5 = None

        self.P6_x_data = None
        self.P6 = None

    def func_P1(self, T, B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18, B19, B20,
                B21, B22, B23):
        T1, T2, T3, T4, Q = T
        P1 = B0 + B1 * T1 + B2 * T2 + B3 * Q + B4 * Q * Q + B5 * T1 * T1 + B6 * T2 * T2 + B7 * Q * T1 + B8 * Q * T2 + B9 * T1 * T2 + B10 * T3 + B11 * T4 + B12 * T3 * T3 + B13 * T4 * T4 + B14 * Q * T3 + B15 * Q * T4 + B16 * T3 * T4 + B17 * (
                T2 - T1) + B18 * (T4 - T3) + B19 * (T2 - T1) * (T2 - T1) + B20 * (T4 - T3) * (T4 - T3) + B21 * Q * (
                     T2 - T1) + B22 * Q * (T4 - T3) + B23 * (T2 - T1) * (T4 - T3)
        return P1

    def fit_P1(self, P1_data):  # 主机系数拟合 P1_data -> db.main_fittings
        temp_T1 = []
        temp_T2 = []
        temp_T3 = []
        temp_T4 = []
        temp_Q = []
        temp_P = []
        for i in P1_data:
            temp_T1.append(i.t1)
            temp_T2.append(i.t2)
            temp_T3.append(i.t3)
            temp_T4.append(i.t4)
            temp_Q.append(i.q)
            temp_P.append(i.p1)
        T1 = np.array(temp_T1)
        T2 = np.array(temp_T2)
        T3 = np.array(temp_T3)
        T4 = np.array(temp_T4)
        Q = np.array(temp_Q)
        P1 = np.array(temp_P)
        self.P1_x_data = (T1, T2, T3, T4, Q)
        self.P1 = P1
        a, b = curve_fit(self.func_P1, self.P1_x_data, self.P1)
        self.B = list(a)
        return a

    def calc_pre_p1(self):  # 计算MAPE RMSE

        B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18, B19, B20, B21, B22, B23 = self.B

        predict_P1 = self.func_P1(self.P1_x_data,
                                  B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18,
                                  B19, B20, B21, B22, B23)

        rat = abs(1 - predict_P1 / self.P1)

        mse = np.sum((predict_P1 - self.P1) ** 2) / len(self.P1)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    def func_P2(self, G2, A0, A1, A2):
        P2 = A0 + A1 * G2 + A2 * G2 * G2
        return P2

    def fit_P2(self, P2_data):  # 冷冻水泵拟合 P2_data -> db.pump2_fittings
        temp_G2 = []
        temp_P2 = []
        for i in P2_data:
            temp_G2.append(i.g2)
            temp_P2.append(i.p2)
        G2 = np.array(temp_G2)
        P2 = np.array(temp_P2)
        self.P2_x_data = G2
        self.P2 = P2
        a, b = curve_fit(self.func_P2, G2, P2)
        self.A = a
        return a

    def calc_pre_p2(self, ):
        P2_pre = self.A[0] + self.A[1] * self.P2_x_data + self.A[2] * self.P2_x_data * self.P2_x_data

        rat = abs(1 - P2_pre / self.P2)
        mse = np.sum((P2_pre - self.P2) ** 2) / len(self.P2)

        return sum(rat) / len(rat), math.sqrt(mse)

    def func_P3(self, G3, C0, C1, C2):
        P3 = C0 + C1 * G3 + C2 * G3 * G3
        return P3

    def fit_P3(self, P3_data):  # 冷却水泵拟合 P3_data -> db.pump3_fittings
        temp_P3 = []
        temp_G3 = []
        for i in P3_data:
            temp_P3.append(i.p3)
            temp_G3.append(i.g3)
        G3 = np.array(temp_G3)
        P3 = np.array(temp_P3)
        self.P3_x_data = G3
        self.P3 = P3
        a, b = curve_fit(self.func_P3, G3, P3)

        self.C = a
        return a

    def calc_pre_p3(self, ):
        P3_pre = self.C[0] + self.C[1] * self.P3_x_data + self.C[2] * self.P3_x_data * self.P3_x_data

        rat = abs(1 - P3_pre / self.P3)
        mse = np.sum((P3_pre - self.P3) ** 2) / len(self.P3)

        return sum(rat) / len(rat), math.sqrt(mse)

    # ==
    def func_Tdelta(self, T, D0, D1, D2):
        TS = T
        Tdelta = D0 + D1 * TS + D2 * TS * TS
        return Tdelta

    def fit_Tdelta_1to1(self, WetBulb_data):  # 冷却塔 一对一
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_1to1 = (TS)
        self.Tdelta_1to1 = Tdelta
        a, b = curve_fit(self.func_Tdelta, (TS), Tdelta)

        self.D_1to1 = a
        return a

    def calc_pre_Tdelta_1to1(self):

        predict_Tdelta = self.func_Tdelta(self.Tdelta_x_data_1to1, self.D_1to1[0], self.D_1to1[1], self.D_1to1[2])
        rat = abs(1 - predict_Tdelta / self.Tdelta_1to1)

        mse = np.sum((predict_Tdelta - self.Tdelta_1to1) ** 2) / len(self.Tdelta_1to1)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==

    def fit_Tdelta_2to1(self, WetBulb_data):
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_2to1 = (TS)
        self.Tdelta_2to1 = Tdelta
        a, b = curve_fit(self.func_Tdelta, (TS), Tdelta)

        self.D_2to1 = a
        return a

    def calc_pre_Tdelta_2to1(self):

        predict_Tdelta = self.func_Tdelta(self.Tdelta_x_data_2to1, self.D_2to1[0], self.D_2to1[1], self.D_2to1[2])
        rat = abs(1 - predict_Tdelta / self.Tdelta_2to1)

        mse = np.sum((predict_Tdelta - self.Tdelta_2to1) ** 2) / len(self.Tdelta_2to1)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==
    def fit_Tdelta_3to1(self, WetBulb_data):
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_3to1 = (TS)
        self.Tdelta_3to1 = Tdelta
        a, b = curve_fit(self.func_Tdelta, (TS), Tdelta)

        self.D_3to1 = a
        return a

    def calc_pre_Tdelta_3to1(self):

        predict_Tdelta = self.func_Tdelta(self.Tdelta_x_data_3to1, self.D_3to1[0], self.D_3to1[1], self.D_3to1[2])
        rat = abs(1 - predict_Tdelta / self.Tdelta_3to1)

        mse = np.sum((predict_Tdelta - self.Tdelta_3to1) ** 2) / len(self.Tdelta_3to1)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==
    def func_Tdelta_4to1(self, T, D0, D1, D2, D3):
        TS = T
        Tdelta = D0 + D1 * TS + D2 * TS * TS + D3 * TS * TS * TS
        return Tdelta

    def fit_Tdelta_4to1(self, WetBulb_data):
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_4to1 = (TS)
        self.Tdelta_4to1 = Tdelta
        a, b = curve_fit(self.func_Tdelta_4to1, (TS), Tdelta)

        self.D_4to1 = a
        return a

    def calc_pre_Tdelta_4to1(self):

        predict_Tdelta = self.func_Tdelta_4to1(self.Tdelta_x_data_4to1, self.D_4to1[0], self.D_4to1[1], self.D_4to1[2],
                                               self.D_4to1[3])
        rat = abs(1 - predict_Tdelta / self.Tdelta_4to1)

        mse = np.sum((predict_Tdelta - self.Tdelta_4to1) ** 2) / len(self.Tdelta_4to1)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==
    def fit_Tdelta_3to2(self, WetBulb_data):
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_3to2 = (TS)
        self.Tdelta_3to2 = Tdelta
        a, b = curve_fit(self.func_Tdelta, (TS), Tdelta)

        self.D_3to2 = a
        return a

    def calc_pre_Tdelta_3to2(self):

        predict_Tdelta = self.func_Tdelta(self.Tdelta_x_data_3to2, self.D_3to2[0], self.D_3to2[1], self.D_3to2[2])
        rat = abs(1 - predict_Tdelta / self.Tdelta_3to2)

        mse = np.sum((predict_Tdelta - self.Tdelta_3to2) ** 2) / len(self.Tdelta_3to2)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==
    def fit_Tdelta_4to3(self, WetBulb_data):
        temp_Tdelta = []
        temp_TS = []
        for i in WetBulb_data:
            temp_Tdelta.append(i.td)
            temp_TS.append(i.ts)
        TS = np.array(temp_TS)
        Tdelta = np.array(temp_Tdelta)
        self.Tdelta_x_data_4to3 = (TS)
        self.Tdelta_4to3 = Tdelta
        a, b = curve_fit(self.func_Tdelta, (TS), Tdelta)

        self.D_4to3 = a
        return a

    def calc_pre_Tdelta_4to3(self):

        predict_Tdelta = self.func_Tdelta(self.Tdelta_x_data_4to3, self.D_4to3[0], self.D_4to3[1], self.D_4to3[2])
        rat = abs(1 - predict_Tdelta / self.Tdelta_4to3)

        mse = np.sum((predict_Tdelta - self.Tdelta_4to3) ** 2) / len(self.Tdelta_4to3)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    # ==
    def func_P4(self, T, E0, E1, E2, E3):
        G3 = T
        P4 = E0 + E1 * G3 + E2 * G3 * G3 + E3 * G3 * G3 * G3
        return P4

    def fit_P4(self, P4_data):  # P4功率与流量
        temp_G3_P4 = []
        temp_P4 = []
        for i in P4_data:
            temp_G3_P4.append(i.g)
            temp_P4.append(i.p4)
        G3_P4 = np.array(temp_G3_P4)
        P4 = np.array(temp_P4)
        self.P4_x_data = G3_P4
        self.P4 = P4
        a, b = curve_fit(self.func_P4, (G3_P4), P4)

        self.E = a
        return a

    def calc_pre_p4(self):
        predict_P4 = self.func_P4(self.P4_x_data, self.E[0], self.E[1], self.E[2], self.E[3])
        rat = abs(1 - predict_P4 / self.P4)

        mse = np.sum((predict_P4 - self.P4) ** 2) / len(self.P4)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    def func_P5(self, T, K0, K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13, K14, K15, K16, K17):
        T0, T1, T2, Q = T
        P5 = K0 + K1 * T1 + K2 * T2 + K3 * Q + K4 * Q * Q + K5 * T1 * T1 + K6 * T2 * T2 + K7 * Q * T1 + K8 * Q * T2 + K9 * T1 * T2 + K10 * (
                    T2 - T1) + K11 * T0 + K12 * (T2 - T1) * (T2 - T1) + K13 * T0 * T0 + K14 * Q * (
                         T2 - T1) + K15 * Q * T0 + K16 * (T2 - T1) * T0 + K17 * (T0 - T1)
        return P5

    def fit_P5(self, P5_data):  # 蒸发冷一体机组系数（制冷工况） P5_data -> db.main_fittings
        temp_T0 = []
        temp_T1 = []
        temp_T2 = []
        temp_Q = []
        temp_P = []
        for i in P5_data:
            temp_T0.append(i.t0)
            temp_T1.append(i.t1)
            temp_T2.append(i.t2)
            temp_Q.append(i.q)
            temp_P.append(i.p5)
        T0 = np.array(temp_T0)
        T1 = np.array(temp_T1)
        T2 = np.array(temp_T2)
        Q = np.array(temp_Q)
        P5 = np.array(temp_P)
        self.P5_x_data = (T0, T1, T2, Q)
        self.P5 = P5
        a, b = curve_fit(self.func_P5, self.P5_x_data, self.P5)
        self.K = list(a)
        return a

    def calc_pre_p5(self):  # 计算MAPE RMSE

        K0, K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13, K14, K15, K16, K17 = self.K

        predict_P5 = self.func_P5(self.P5_x_data,
                                  K0, K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13, K14, K15, K16, K17)

        rat = abs(1 - predict_P5 / self.P5)

        mse = np.sum((predict_P5 - self.P5) ** 2) / len(self.P5)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse

    def func_P6(self, T, J0, J1, J2, J3, J4, J5, J6, J7, J8, J9):
        T0, T1, Q = T
        P6 = J0 + J1 * T1 + J2 * Q + J3 * Q * Q + J4 * T1 * T1 + J5 * Q * T1 + J6 * T0 + J7 * T0 * T0 + J8 * Q * T0 + J9 * (
                    T1 - T0)
        return P6

    def fit_P6(self, P6_data):  # 风冷热泵机组系数（制热工况） P6_data -> db.main_fittings
        temp_T0 = []
        temp_T1 = []
        temp_Q = []
        temp_P = []
        for i in P6_data:
            temp_T0.append(i.t0)
            temp_T1.append(i.t1)
            temp_Q.append(i.q)
            temp_P.append(i.p6)
        T0 = np.array(temp_T0)
        T1 = np.array(temp_T1)
        Q = np.array(temp_Q)
        P6 = np.array(temp_P)
        self.P6_x_data = (T0, T1, Q)
        self.P6 = P6
        a, b = curve_fit(self.func_P6, self.P6_x_data, self.P6)
        self.J = list(a)
        return a

    def calc_pre_p6(self):  # 计算MAPE RMSE

        J0, J1, J2, J3, J4, J5, J6, J7, J8, J9 = self.J

        predict_P6 = self.func_P6(self.P6_x_data, J0, J1, J2, J3, J4, J5, J6, J7, J8, J9)

        rat = abs(1 - predict_P6 / self.P6)

        mse = np.sum((predict_P6 - self.P6) ** 2) / len(self.P6)

        rmse = math.sqrt(mse)

        return (sum(rat) / len(rat)), rmse
