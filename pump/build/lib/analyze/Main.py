from analyze import db
from analyze import PumpFit
from analyze.Evoopt import *


def testPumpFit():
    """水泵系数拟合测试"""
    db.load("template.xlsx")  # 加载供拟合的原始数据
    pf = PumpFit.PumpFitting()

    print(db.main_fittings)
    B = pf.fit_P1(db.main_fittings)  # 主机参数拟合
    mape, rmse = pf.calc_pre_p1()
    print("B: ", B)
    print("mape: ", mape, " rmse: ", rmse)

    A = pf.fit_P2(db.pump2_fittings)  # 冷冻泵系数拟合
    mape, rmse = pf.calc_pre_p2()
    print("A: ", A)
    print("mape: ", mape, " rmse: ", rmse)

    C = pf.fit_P3(db.pump3_fittings)  # 冷却泵系数拟合
    mape, rmse = pf.calc_pre_p3()
    print("C: ", C)
    print("mape: ", mape, " rmse: ", rmse)

    # 冷却塔拟合
    D_1to1 = pf.fit_Tdelta_1to1(db.wet_bulb_fittings_1to1)
    D_2to1 = pf.fit_Tdelta_2to1(db.wet_bulb_fittings_2to1)
    D_3to1 = pf.fit_Tdelta_3to1(db.wet_bulb_fittings_3to1)
    D_4to1 = pf.fit_Tdelta_4to1(db.wet_bulb_fittings_4to1)
    D_3to2 = pf.fit_Tdelta_3to2(db.wet_bulb_fittings_3to2)
    D_4to3 = pf.fit_Tdelta_4to3(db.wet_bulb_fittings_4to3)
    mapD_1to1, mseD_1to1 = pf.calc_pre_Tdelta_1to1()
    mapD_2to1, mseD_2to1 = pf.calc_pre_Tdelta_2to1()
    mapD_3to1, mseD_3to1 = pf.calc_pre_Tdelta_3to1()
    mapD_4to1, mseD_4to1 = pf.calc_pre_Tdelta_4to1()
    mapD_3to2, mseD_3to2 = pf.calc_pre_Tdelta_3to2()
    mapD_4to3, mseD_4to3 = pf.calc_pre_Tdelta_4to3()
    print("D_1to1: ", D_1to1)
    print("mape: ", mapD_1to1, " rmse: ", mseD_1to1)
    print("D_2to1: ", D_2to1)
    print("mape: ", mapD_2to1, " rmse: ", mseD_2to1)
    print("D_3to1: ", D_3to1)
    print("mape: ", mapD_3to1, " rmse: ", mseD_3to1)
    print("D_4to1: ", D_4to1)
    print("mape: ", mapD_4to1, " rmse: ", mseD_4to1)
    print("D_3to2: ", D_3to2)
    print("mape: ", mapD_3to2, " rmse: ", mseD_3to2)
    print("D_4to3: ", D_4to3)
    print("mape: ", mapD_4to3, " rmse: ", mseD_4to3)
    E = pf.fit_P4(db.p4_fittings)
    mape, rmse = pf.calc_pre_p4()
    print("E: ", E)
    print("mape: ", mape, " rmse: ", rmse)

    K = pf.fit_P5(db.p5_fittings)
    mape, rmse = pf.calc_pre_p5()
    print("K: ", K)
    print("mape: ", mape, " rmse: ", rmse)

    J = pf.fit_P6(db.p6_fittings)
    mape, rmse = pf.calc_pre_p6()
    print("J: ", J)
    print("mape: ", mape, " rmse: ", rmse)

    testOptimizeCalculation(pf)


def testOptimizeCalculation(fitResult):
    """优化计算测试"""
    superP = db.init_params
    tempQ = db.optimize_result[0].q * 2
    tempG2 = None
    tempG3 = None

    for index, i in enumerate(db.optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        opt = Evoopt(Q, TS, superP, fitResult)
        res = None
        if abs(Q - tempQ) * 100 / tempQ < float(db.init_params.yuzhi):

            res = opt.run(tempG2, tempG3)
            pass
        else:
            res = opt.run()
            tempQ = Q
            tempG2 = opt.G2
            tempG3 = opt.G3

        db.optimize_result[index].load_percentage = res[0]
        db.optimize_result[index].system_load_percentage = res[1]
        db.optimize_result[index].t1 = res[2]
        db.optimize_result[index].t2 = res[3]
        db.optimize_result[index].G2_lendong = res[4]
        db.optimize_result[index].fluency_lendong = res[5]

        db.optimize_result[index].t3 = res[6]
        db.optimize_result[index].t4 = res[7]
        db.optimize_result[index].G3_lenque = res[8]
        db.optimize_result[index].fluency_lenque = res[9]

        db.optimize_result[index].delta_t = res[10]
        db.optimize_result[index].p1 = res[11]
        db.optimize_result[index].p2 = res[12]
        db.optimize_result[index].p3 = res[13]
        db.optimize_result[index].p4 = res[14]
        db.optimize_result[index].p = res[15]
        db.optimize_result[index].cop = res[16]
        db.optimize_result[index].n = res[17]
        print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in db.optimize_result[index].__dict__.items()]))


if __name__ == '__main__':
    testPumpFit()
