# -*- coding: utf-8 -*-
import geatpy as ea


class ACHPHoptimizer():
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
    P1（主机功率）, P2（冷冻水泵功率）, total_P（总功率）,total_cop（系统COP）, 
    open_num（设备开启台数）
    """

    def run(self, tempQ=-1, tempG2=-1):
        if self.problem.ifopt is False:
            G2 = self.problem.P20 * self.problem.u1
            P2 = self.A[0] + self.A[1] * G2 + self.A[2] * G2 * G2
            P = P2
            COP = self.problem.Q / P
            T2 = self.problem.T1 + 6 * self.problem.Q / (7 * G2)
            return (
            0, 0, round(self.problem.T1, 3), round(T2, 3), round(G2, 3), round(50 * G2 / self.problem.G20, 3), 0,
            round(P2, 3), round(P, 3), round(COP, 3), 0)
        else:
            Q = self.problem.Q
            T1 = self.problem.T1

            if abs(self.problem.Q * self.problem.n - tempQ) * 100 / tempQ < float(self.problem.yuzhi):
                G2 = tempG2
                T2 = T1 + 6 * Q / (G2 * 7)
            else:
                [BestIndi, population] = self.myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
                T2 = BestIndi.Phen[0, 0]
                G2 = 6 * Q / (7 * (T2 - T1))

            G20 = self.problem.G20
            u1 = self.problem.u1
            if G2 < G20 * u1:
                T2 = T1 + 6 * Q / (7 * G20 * u1)
            if G2 > G20:
                T2 = T1 + 6 * Q / (7 * G20)

            if T2 - T1 < self.problem.t2_tuple[0]:
                T2 = T1 + self.problem.t2_tuple[0]
            if T2 - T1 > self.problem.t2_tuple[1]:
                T2 = T1 + self.problem.t2_tuple[1]

            P1 = self.func_P1((self.problem.TS, T1, Q), self.problem.J)
            A0, A1, A2 = self.problem.A

            G2 = 6 * Q / (7 * (T2 - T1))
            G20 = self.problem.G20
            u1 = self.problem.u1
            G2 = max(G2, G20 * u1)
            G2 = min(G2, G20)
            P2 = A0 + A1 * G2 + A2 * G2 * G2

            total_P = self.problem.n * (P1 + P2)

            loading_ration = Q / self.problem.QS * 100
            system_loading_ration = (Q * self.problem.n * 100) / (self.problem.QS * self.problem.max_n)
            open_num = self.problem.n
            total_cop = Q / (total_P / self.problem.n)

            P1 = self.problem.n * P1
            P2 = self.problem.n * P2
            return (round(loading_ration, 2), round(system_loading_ration, 2), round(T1, 3), round(T2, 3), round(G2, 3),
                    round(50 * G2 / G20, 3), round(P1, 4), round(P2, 3), round(total_P, 3),
                    round(total_cop, 3), open_num)

    def func_P1(self, T, J):
        T0, T1, Q = T
        J0, J1, J2, J3, J4, J5, J6, J7, J8, J9 = J
        P1 = J0 + J1 * T1 + J2 * Q + J3 * Q * Q + J4 * T1 * T1 + J5 * Q * T1 + J6 * T0 + J7 * T0 * T0 + J8 * Q * T0 + J9 * (
                T1 - T0)
        return P1
