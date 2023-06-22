# -*- coding: utf-8 -*-

class CCTFoptimizer():
    def __init__(self, problem):
        self.problem = problem

    """
    返回结果
    loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
    T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
    T3（冷却水出水温度）, T4（冷却水回水温度）, G3（冷却水泵流量）, 50 * G3 / G30（冷却水泵频率）,
    cold_flu（冷却塔冷幅）, 
    P1（主机功率）, P2（冷冻水泵功率）, P3（冷却水泵功率）, P4（冷却塔功率）, total_P（总功率）,total_cop（系统COP）, 
    open_num（设备开启台数）
    """

    def run(self):
        Q = self.problem.Q  # 单套
        T3 = self.problem.T3
        G20 = self.problem.G20
        G30 = self.problem.G30
        T2 = self.problem.ct_gsc_hswd
        T4 = self.problem.ct_lqc_hswd
        a = self.problem.bh_efficiency

        T1 = T3 - self.problem.bh_td
        G2 = 6 * Q / (7 * self.problem.w_td)
        if G2 < G20 * self.problem.u1:
            G2 = G20 * self.problem.u1
            T1 = T2 - 6 * Q / (7 * G2)

        G3 = 6 * Q / (a * 7 * self.problem.ct_td)
        if G3 < G30 * self.problem.u2:
            G3 = G30 * self.problem.u2
            T3 = T4 - 6 * Q / (a * 7 * G3)

        A0, A1, A2 = self.problem.A
        P2 = A0 + A1 * G2 + A2 * G2 * G2
        C0, C1, C2 = self.problem.C
        P3 = C0 + C1 * G3 + C2 * G3 * G3
        E0, E1, E2, E3 = self.problem.E
        P4 = E0 + E1 * G3 + E2 * G3 * G3 + E3 * G3 * G3 * G3


        total_P2 = self.problem.n * P2
        total_P3 = self.problem.n * P3
        total_P4 = self.problem.z * P4
        total_P = total_P2 + total_P3 + total_P4
        print("OUT: ", Q * self.problem.n, self.problem.n, self.problem.z, P4, total_P4)
        open_num = self.problem.n
        total_cop = Q / (total_P / self.problem.n)
        cold_flu = T3 - self.problem.TS

        loading_ration = Q / self.problem.QS * 100
        system_loading_ration = (Q * self.problem.n * 100) / (self.problem.QS * self.problem.max_n)

        return (round(loading_ration, 2), round(system_loading_ration, 2), round(T1, 2), round(T2, 2), round(G2, 2),
                round(50 * G2 / self.problem.G20, 2), round(T3, 2), round(T4, 2), round(G3, 2),
                round(50 * G3 / self.problem.G30, 2),
                round(cold_flu, 2), 0, round(total_P2, 2), round(total_P3, 2), round(total_P4, 2), round(total_P, 2),
                round(total_cop, 2), round(open_num, 2), round(self.problem.z, 2),False)
