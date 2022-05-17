# -*- coding: utf-8 -*-
"""main.py"""
import geatpy as ea # import geatpy
from analyze.MyPro import MyProblem # 导入自定义问题接口
import numpy as np
import random as rd
from model import schema
from P_pro import PumpFit



class Evoopt():
    def __init__(self,Q,TS,superP,fittingP):
        # print("---test")
        self.problem = MyProblem(Q,TS,superP,fittingP)
        """==================================种群设置=================================="""
        # Encoding = 'BG'       # 编码方式
        self.Encoding = 'RI'  # 编码方式
        self.NIND = 100  # 种群规模
        self.Field = ea.crtfld(self.Encoding, self.problem.varTypes, self.problem.ranges, self.problem.borders)  # 创建区域描述器
        self.population = ea.Population(self.Encoding, self.Field, self.NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """================================算法参数设置================================="""
        # myAlgorithm = ea.soea_EGA_templet(problem, population) # 实例化一个算法模板对象
        # myAlgorithm = ea.soea_studGA_templet(problem, population) # 实例化一个算法模板对象
        # myAlgorithm = ea.soea(problem, population) # 实例化一个算法模板对象
        # myAlgorithm = ea.soea_DE_best_1_bin_templet(problem, population) # 实例化一个算法模板对象
        self.myAlgorithm = ea.soea_DE_best_1_L_templet(self.problem, self.population)  # 实例化一个算法模板对象
        self.myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
        self.myAlgorithm.mutOper.pm = 0.2
        self.myAlgorithm.recOper.XOVR = 0.7  # 设置交叉概率
        self.myAlgorithm.MAXGEN = 25  # 最大进化代数
        self.myAlgorithm.logTras = 0  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
        # self.myAlgorithm.verbose = True  # 设置是否打印输出日志信息
        self.myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
        self.G2 = None
        self.G3 = None
    def run(self,tempG2 = -1,tempG3 = -1):
        # print("==="*20)
        if self.problem.ifopt is False:
            loading_ration = self.problem.Q / self.problem.QS *100
            return (round(loading_ration,2),0,0,0,0,0,0,0,0,0,0,0,0,0,self.problem.P20,0,0)

        else:
            #     if BestIndi.sizes != 0:
            #         # print(BestIndi.sizes)
            #         print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
            #         print('最优的控制变量值为：')
            #         for i in range(BestIndi.sizes):
            #             print(BestIndi.Phen[i, :])


            [BestIndi, population] = self.myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
            # [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
            # BestIndi.save()  # 把最优个体的信息保存到文件中
            # print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])

            T1 = self.problem.T1
            T2 = BestIndi.Phen[0, 0]
            T3 = self.problem.T3
            T4 = BestIndi.Phen[0, 1]
            # print("选到的T1是:", T1)
            # print("选到的T2是:", T2)
            # print("选到的T3是:", T3)
            # print("选到的T4是：", T4)

            Q = self.problem.Q


            P1 = self.func_P1((T1, T2, T3, T4, Q), self.problem.B)
            # print("p1::", P1)
            A0, A1, A2 = self.problem.A

            flag_g2 = 0
            flag_g3 = 0

            G2 = 6 * Q / (7 * (T2 - T1))
            G20 = self.problem.G20
            u1 = self.problem.u1

            if G2 <=G20*u1 or G2 >= G20:
                flag_g2 = 1
            # P2 = A0 + A1 * G2 + A2 * G2 * G2
            # print("p2:", P2)

            # C0, C1, C2 = self.problem.C
            G3 = 6 * (Q + P1) / (7 * (T4 - T3))
            G30 = self.problem.G30
            u2 = self.problem.u2
            if G3 <= G30*u2 or G3 >=G30:
                flag_g3 = 1

            if flag_g2 == 1:
                # print("此时TS={:s},Q = {:s}".format(str(self.problem.TS),str(Q)))
                T2 = T1 + 6*Q/(7*G20*u1)
                if T2 - T1 < self.problem.t2_tuple[0]:
                    T2 = T1 + self.problem.t2_tuple[0]
                    # print("T2被设置的过小{:s}，被设置成了{:s}".format(str(self.problem.TS),str(T2)))
                if T2 - T1 > self.problem.t2_tuple[1]:
                    # print("T2被设置的过大{:s}，被设置成了{:s}".format(str(self.problem.TS),str(T2)))
                    T2 = T1 + self.problem.t2_tuple[1]
            if flag_g3 == 1:
                T4 = T3 + 6*(Q+P1)/(7*G30*u2)
                if T4 - T3 < self.problem.t4_tuple[0]:
                    # print("T4被设置的过小{:s}，被设置成了{:s}".format(str(self.problem.TS),str(T4)))
                    T4 = T3 + self.problem.t4_tuple[0]
                if T4 - T3 > self.problem.t4_tuple[1]:
                    # print("T4被设置的过大{:s}，被设置成了{:s}".format(str(self.problem.TS),str(T4)))
                    T4 = T3 + self.problem.t4_tuple[0]
            # G3 = max(G3, G30 * u2)
            # G3 = min(G3, G30)
            # print(G3)
            # print("P3的G3：", G3)
            # =====
            P1 = self.func_P1((T1,T2,T3, T4,Q), self.problem.B)
            # print("p1::" ,P1)
            A0,A1,A2 = self.problem.A

            G2 = 6 * Q / (7 * (T2 - T1))
            G20 = self.problem.G20
            u1 = self.problem.u1
            G2= max(G2, G20 * u1)
            G2 = min(G2, G20)
            if tempG2 != -1:
                G2 = tempG2
            self.G2 = G2
            P2 = A0+A1*G2+A2*G2*G2
            # print("p2:",P2)

            C0,C1,C2 = self.problem.C
            G3 = 6 * (Q + P1) / (7 * (T4 - T3))
            G30 = self.problem.G30
            u2 = self.problem.u2
            G3 = max(G3, G30 * u2)
            G3 = min(G3, G30)
            if tempG3 != -1:
                G3 = tempG3
            self.G3 = G3
            # print(G3)
            # print("P3的G3：", G3)
            P3 = C0+C1*G3+C2*G3*G3
            # print("p3",P3)

            E0,E1,E2,E3 = self.problem.E
            P4=E0+E1*G3+E2*G3*G3+E3*G3*G3*G3
            if T3 >= self.problem.t3_min:
                P4 = self.problem.P0
            # print("p4:",P4)

            # print(str(P1)+"、"+str(P2)+"、"+str(P3)+"、"+str(P4))
            total_P = self.problem.n * (P1+P2+P3) + self.problem.z * P4

            # print("MINP:",total_P)

            loading_ration = Q/self.problem.QS * 100
            # print("此时Q={:s}".format(str(Q*self.problem.n)))
            system_loading_ration = (Q*self.problem.n*100)/(self.problem.QS*self.problem.max_n)
            cold_flu = T3 - self.problem.TS
            open_num = self.problem.n
            total_cop = Q / (total_P/self.problem.n)

            P1 = self.problem.n * P1
            P2 = self.problem.n * P2
            P3 = self.problem.n * P3
            P4 = self.problem.n * P4
            return (round(loading_ration,2),round(system_loading_ration,2),round(T1,3),round(T2,3),round(G2,3),round(50*G2/G20,3),round(T3,3),round(T4,3),round(G3,3),round(50*G3/G30),round(cold_flu,3),round(P1,4),round(P2,3),round(P3,3),round(P4,3),round(total_P,3),round(total_cop,3),round(open_num,3))


    def func_P1(self,T,B):
        T1, T2, T3, T4, Q = T
        B0, B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16, B17, B18, B19, B20, B21, B22, B23 = B
        P1 = B0 + B1 * T1 + B2 * T2 + B3 * Q + B4 * Q * Q + B5 * T1 * T1 + B6 * T2 * T2 + B7 * Q * T1 + B8 * Q * T2 + B9 * T1 * T2 + B10 * T3 + B11 * T4 + B12 * T3 * T3 + B13 * T4 * T4 + B14 * Q * T3 + B15 * Q * T4 + B16 * T3 * T4 + B17 * (
                T2 - T1) + B18 * (T4 - T3) + B19 * (T2 - T1) * (T2 - T1) + B20 * (T4 - T3) * (T4 - T3) + B21 * Q * (
                     T2 - T1) + B22 * Q * (T4 - T3) + B23 * (T2 - T1) * (T4 - T3)
        return P1


# superP = schema.InitialParameters()
# fittingP = schema.FittingCoefficients()
# opt = Evoopt(Q=421.9,TS=16,superP=superP,fittingP=fittingP)
# res = opt.run()
# if type(res) is float:
#     print(res)
# else:
#     loading_ration,T1,T2,T3,T4,cold_flu,P1,P2,P3,P4,total_P,total_cop,open_num = res
#     print("ration:",loading_ration)

# if __name__ == '__main__':
#     """===============================实例化问题对象================================"""
#     Q = 421.9
#
#     TS = 16
#
#     QS = 2814
#     nita = 80
#     max_n = 3
#     T2_range = (4, 8)
#     T4_range = (4, 8)
#
#     problem = MyProblem(Q, TS, QS, nita,max_n,T2_range,T4_range)  # 生成问题对象
#     # problem = MyProblem(Q, TS, superP,fittingP)  # 生成问题对象
#
#
#     # 2814	28
#     # 2532.6	27
#     # 2251.2	26
#     # 1969.8	25
#     # 1688.4	24
#     # 1407	23
#     # 1125.6	22
#     # 844.2	20
#     # 562.8	18
#     # 281.4	16
#
#     """==================================种群设置=================================="""
#     # Encoding = 'BG'       # 编码方式
#     Encoding = 'RI'  # 编码方式
#     NIND = 100  # 种群规模
#     Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
#     population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
#     """================================算法参数设置================================="""
#     # myAlgorithm = ea.soea_EGA_templet(problem, population) # 实例化一个算法模板对象
#     # myAlgorithm = ea.soea_studGA_templet(problem, population) # 实例化一个算法模板对象
#     # myAlgorithm = ea.soea(problem, population) # 实例化一个算法模板对象
#     # myAlgorithm = ea.soea_DE_best_1_bin_templet(problem, population) # 实例化一个算法模板对象
#     myAlgorithm = ea.soea_DE_best_1_L_templet(problem, population)  # 实例化一个算法模板对象
#     myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
#     myAlgorithm.mutOper.pm = 0.2
#     myAlgorithm.recOper.XOVR = 0.7  # 设置交叉概率
#
#     myAlgorithm.MAXGEN = 25  # 最大进化代数
#     myAlgorithm.logTras = 2  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
#     myAlgorithm.verbose = True  # 设置是否打印输出日志信息
#     myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
#
#     # ============启发式初始化种群==========
#     # 6 < T1 < 10
#     # 10 < T2 < 20
#     # 21 < T3 < 33
#     # 25 < T4 < 39
#
#     # 4 < T2 - T1 < 10       （4）
#     # 4 < T4 - T3 < 6；    （5）
#
#     # =====启发式初始化
#     # initial_chrome = np.zeros((NIND,4))
#     # for i in range(NIND):
#     #     T1 = rd.uniform(6,10)
#     #     T2_MIN =  max(4+T1,10)
#     #     T2_MAX =  min(10+T1,20)
#     #     T2 = rd.uniform(T2_MIN,T2_MAX)
#     #     T3 = rd.uniform(21,33)
#     #     T4_MIN = max(4+T3,25)
#     #     T4_MAX = min(6+T3,39)
#     #     T4 = rd.uniform(T4_MIN,T4_MAX)
#     #     initial_chrome[i][0]=T1
#     #     initial_chrome[i][1]=T2
#     #     initial_chrome[i][2]=T3
#     #     initial_chrome[i][3]=T4
#     # =========================
#     # print(initial_chrome)
#     # popPhet = ea.Population(Encoding, Field, NIND, initial_chrome)
#     # myAlgorithm.call_aimFunc(popPhet)
#     # ======================================
#     """===========================调用算法模板进行种群进化==============--==========="""
#     [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
#     # [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
#     BestIndi.save()  # 把最优个体的信息保存到文件中
#     """==================================输出结果=================================="""
#     print('用时：%f 秒' % myAlgorithm.passTime)
#     print('评价次数：%d 次' % myAlgorithm.evalsNum)
#     if BestIndi.sizes != 0:
#         # print(BestIndi.sizes)
#         print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
#         print('最优的控制变量值为：')
#         for i in range(BestIndi.sizes):
#             print(BestIndi.Phen[i, :])
#
#     else:
#         print('没找到可行解。')
#     print("****" * 20)
#
#     # 输出最优值的P1-P4==========================================================================
#     from fit_P1 import func_P1
#     T1,T3,n,G20,G30,u1,u2 = problem.T1,problem.T3,problem.max_n,problem.G20,problem.G30,problem.u1,problem.u2
#
#     T2,T4  = BestIndi.Phen[i,:]
#
#     P1 = func_P1((T1,	T2,	T3, T4
#     ,Q), 1.25592470e+02, 5.39445250e+01, -5.22395970e+01, 6.29397302e-02, -2.06962469e-05, -3.33850530e+01,
#                 -3.30937615e+01, 1.13915116e+02
#                 , -1.13920754e+02, 6.62996700e+01, -5.43024482e+01, 4.63683510e+01
#                 , -2.01032174e+03, -2.00895336e+03, 1.97466857e+02, -1.97464621e+02
#                 , 4.01945845e+03, 5.63936524e+01, -9.05705574e+01, 3.25980615e+01
#                 , 2.00722896e+03, 1.13929510e+02, 1.97486520e+02, -3.39669822e+00)
#     print("p1::" ,P1)
#
#     A0,A1,A2 = 1.05105606e+02,-6.08574731e-01,1.03989940e-03
#
#     G2 = 6 * Q / (7 * (T2 - T1))
#
#     G2= max(G2, G20 * u1)
#     P2 = A0+A1*G2+A2*G2*G2
#     print("p2:",P2)
#
#     # 10,	16.43171636,	21, 25
#     C0,C1,C2 = -5.40003853e+01,2.96859204e-01,-2.09088412e-04
#     # P1 = -146.63113336006293
#     G3 = 6 * (Q + P1) / (7 * (T4 - T3))
#
#     G3 = max(G3, G30 * u2)
#     # print("P3的G3：", G3)
#     P3 = C0+C1*G3+C2*G3*G3
#
#     print("p3",P3)
#     # print("P4G:",P4G)
#     E0,E1,E2,E3 = 3.27976744e+01, -1.67712441e-01,  2.92380418e-04, -1.11110755e-07
#     P4=E0+E1*G3+E2*G3*G3+E3*G3*G3*G3
#     if T3 >= 18:
#         P4 = 22
#     print("p4:",P4)
#
#     print(str(P1)+"、"+str(P2)+"、"+str(P3)+"、"+str(P4))
#     print("MINP:",problem.n*(P1+P2+P3+P4))
