# -*- coding: utf-8 -*-
import geatpy as ea
from analyze.MyProblem import MyProblem  # 导入自定义问题接口


class CCTFoptimizer():
    def __init__(self, problem):
        self.problem = problem
        """==================================种群设置=================================="""
        self.Encoding = 'RI'  # 编码方式
        self.NIND = 100  # 种群规模
        self.Field = ea.crtfld(self.Encoding, self.problem.varTypes, self.problem.ranges,
                               self.problem.borders)  # 创建区域描述器
        self.population = ea.Population(self.Encoding, self.Field, self.NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """================================算法参数设置================================="""
        self.myAlgorithm = ea.soea_DE_best_1_L_templet(self.problem, self.population)  # 实例化一个算法模板对象
        self.myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
        self.myAlgorithm.mutOper.pm = 0.2
        self.myAlgorithm.recOper.XOVR = 0.7  # 设置交叉概率
        self.myAlgorithm.MAXGEN = 25  # 最大进化代数
        self.myAlgorithm.logTras = 0  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
        self.myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    """
    返回结果
    loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
    T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
    T3（冷冻水出水温度）, T4（冷冻水回水温度）, G3（冷冻水泵流量）, 50 * G3 / G30（冷冻水泵频率）,
    cold_flu（冷却塔冷幅）, 
    P1（主机功率）, P2（冷冻水泵功率）, P3（冷却水泵功率）, P4（冷却塔功率）, total_P（总功率）,total_cop（系统COP）, 
    open_num（设备开启台数）
    """
    def run(self, tempQ=-1,tempG2=-1,tempG3=-1,tempP1=-1):
        if self.problem.ifopt is False:
            G2 = self.problem.P20 * self.problem.u1
            P2 = self.A[0]+ self.A[1] * G2 + self.A[2] * G2 * G2
            P = P2
            COP = self.problem.Q/P
            T2 = self.problem.T1 + 6 * self.problem.Q / (7 * G2)
            return (0, 0, round(self.problem.T1, 3), round(T2, 3), round(G2, 3), round(50 * G2 / self.problem.G20, 3), 0, 0, 0, 0, 0, round(P2, 3), 0, 0, round(P, 3), round(COP, 3), 0)
        else:
            Q = self.problem.Q
            T1 = self.problem.T1
            T3 = self.problem.T3

            if abs(self.problem.Q - tempQ) * 100 / tempQ < float(self.problem.yuzhi):
                G2 = tempG2
                G3 = tempG3
                T2=T1+6*Q/(G2*7)
                T4 = T3 + 6 * (Q + tempP1) / (G3 * 7)
            else:
                [BestIndi, population] = self.myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
                T2 = BestIndi.Phen[0, 0]
                T4 = BestIndi.Phen[0, 1]

                P1 = self.func_P1((T1, T2, T3, T4, Q), self.problem.B)
                G2 = 6 * Q / (7 * (T2 - T1))
                G3 = 6 * (Q + P1) / (7 * (T4 - T3))

            G20 = self.problem.G20
            u1 = self.problem.u1
            if G2 <= G20 * u1 or G2 >= G20:
                T2 = T1 + 6 * Q / (7 * G20 * u1)

            G30 = self.problem.G30
            u2 = self.problem.u2
            if G3 <= G30 * u2 or G3 >= G30:
                P1 = self.func_P1((T1, T2, T3, T4, Q), self.problem.B)
                T4 = T3 + 6 * (Q + P1) / (7 * G30 * u2)

            if T2 - T1 < self.problem.t2_tuple[0]:
                T2 = T1 + self.problem.t2_tuple[0]
            if T2 - T1 > self.problem.t2_tuple[1]:
                T2 = T1 + self.problem.t2_tuple[1]

            if T4 - T3 < self.problem.t4_tuple[0]:
                T4 = T3 + self.problem.t4_tuple[0]
            if T4 - T3 > self.problem.t4_tuple[1]:
                T4 = T3 + self.problem.t4_tuple[0]
            P1 = self.func_P1((T1, T2, T3, T4, Q), self.problem.B)
            A0, A1, A2 = self.problem.A

            G2 = 6 * Q / (7 * (T2 - T1))
            G20 = self.problem.G20
            u1 = self.problem.u1
            G2 = max(G2, G20 * u1)
            G2 = min(G2, G20)
            P2 = A0 + A1 * G2 + A2 * G2 * G2

            C0, C1, C2 = self.problem.C
            G3 = 6 * (Q + P1) / (7 * (T4 - T3))
            G30 = self.problem.G30
            u2 = self.problem.u2
            G3 = max(G3, G30 * u2)
            G3 = min(G3, G30)
            P3 = C0 + C1 * G3 + C2 * G3 * G3

            E0, E1, E2, E3 = self.problem.E
            P4 = E0 + E1 * G3 + E2 * G3 * G3 + E3 * G3 * G3 * G3
            if T3 >= self.problem.t3_min:
                P4 = self.problem.P0
            total_P = self.problem.n * (P1 + P2 + P3) + self.problem.z * P4

            loading_ration = Q / self.problem.QS * 100
            system_loading_ration = (Q * self.problem.n * 100) / (self.problem.QS * self.problem.max_n)
            cold_flu = T3 - self.problem.TS
            open_num = self.problem.n
            total_cop = Q / (total_P / self.problem.n)

            P1 = self.problem.n * P1
            P2 = self.problem.n * P2
            P3 = self.problem.n * P3
            P4 = self.problem.n * P4
            return (round(loading_ration, 2), round(system_loading_ration, 2), round(T1, 3), round(T2, 3), round(G2, 3),
                    round(50 * G2 / G20, 3), round(T3, 3), round(T4, 3), round(G3, 3), round(50 * G3 / G30),
                    round(cold_flu, 3), round(P1, 4), round(P2, 3), round(P3, 3), round(P4, 3), round(total_P, 3),
                    round(total_cop, 3), round(open_num, 3))

    def func_P1(self, T, B):
        T1, T2, T3, T4, Q = T
        B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18, B19, B20, B21, B22, B23 = B
        P1 = B0 + B1 * T1 + B2 * T2 + B3 * Q + B4 * Q * Q + B5 * T1 * T1 + B6 * T2 * T2 + B7 * Q * T1 + B8 * Q * T2 + B9 * T1 * T2 + B10 * T3 + B11 * T4 + B12 * T3 * T3 + B13 * T4 * T4 + B14 * Q * T3 + B15 * Q * T4 + B16 * T3 * T4 + B17 * (
                T2 - T1) + B18 * (T4 - T3) + B19 * (T2 - T1) * (T2 - T1) + B20 * (T4 - T3) * (T4 - T3) + B21 * Q * (
                     T2 - T1) + B22 * Q * (T4 - T3) + B23 * (T2 - T1) * (T4 - T3)
        return P1