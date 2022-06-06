# -*- coding: utf-8 -*-

class CCTFoptimizer():
    def __init__(self, problem):
        self.problem = problem

    """
    返回结果
    T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
    T3（冷却水出水温度）, T4（冷却水回水温度）, G3（冷却水泵流量）, 50 * G3 / G30（冷却水泵频率）,
    t_cooling（冷却塔冷幅）, 
    P2（冷冻水泵功率）, P3（冷却水泵功率）, P4（冷却塔功率）, total_P（总功率）,total_cop（系统COP）, 
    open_num_n1（冷冻水泵开启台数）, open_num_n2（冷却水泵开启台数）, open_num_z (冷却塔开启台数)
    """
    def run(self):
        Q = self.problem.Q
        T3 = self.problem.T3
        Ts = self.problem.TS
        G20 = self.problem.G20
        G30 =self.problem.G30
        t_cooling=T3 -Ts
        T4 = T3 + self.problem.f_ct_td
        T1 = T3 - self.problem.f_bh_td
        T2 = T1 + self.problem.f_w_td

        G2 = 6 * Q / (self.problem.n2 * 7 * self.problem.f_w_td)
        G3 = 6 * Q / (self.problem.f_bh_efficiency * self.problem.n3 * 7 * self.problem.f_ct_td)
        A0, A1, A2 = self.problem.A
        P2 = A0 + A1 * G2 + A2 * G2 * G2
        C0, C1, C2 = self.problem.C
        P3 = C0 + C1 * G3 + C2 * G3 * G3
        E0, E1, E2, E3 = self.problem.E
        P4 = E0 + E1 * G3 + E2 * G3 * G3 + E3 * G3 * G3 * G3

        if T3 >= self.problem.t3_min:
            P4 = self.problem.P0
        total_P2=self.problem.n2*P2
        total_P3 = self.problem.n3 * P3
        total_P4 = self.problem.z * P4
        total_P = total_P2 + total_P3 + total_P4
        total_cop = Q/total_P

        return (round(T1, 3), round(T2, 3), round(G2, 3),round(50 * G2 / G20, 3),
                round(T3, 3), round(T4, 3), round(G3, 3), round(50 * G3 / G30),
                round(t_cooling, 3),
                round(P2, 3), round(P3, 3), round(P4, 3), round(total_P, 3),round(total_cop, 3),
                self.problem.n2,self.problem.n3,int(self.problem.z))

