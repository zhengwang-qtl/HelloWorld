from analyze import db
from analyze.Evoopt import *
from analyze.optimization import *
from analyze.fitting import *


def testCCT():
    """水泵系数拟合测试"""
    pf = fitCCT(db.main_fittings,db.pump2_fittings,db.pump3_fittings,db.wet_bulb_fittings_1to1,
                db.wet_bulb_fittings_2to1,db.wet_bulb_fittings_3to1,db.wet_bulb_fittings_4to1,
                db.wet_bulb_fittings_3to2,db.wet_bulb_fittings_4to3,db.p4_fittings)

    mape, rmse = pf.calc_pre_p1()
    print("B: ", pf.B)
    print("mape: ", mape, " rmse: ", rmse)

    mape, rmse = pf.calc_pre_p2()
    print("A: ", pf.A)
    print("mape: ", mape, " rmse: ", rmse)

    mape, rmse = pf.calc_pre_p3()
    print("C: ", pf.C)
    print("mape: ", mape, " rmse: ", rmse)

    # 冷却塔拟合
    mapD_1to1, mseD_1to1 = pf.calc_pre_Tdelta_1to1()
    mapD_2to1, mseD_2to1 = pf.calc_pre_Tdelta_2to1()
    mapD_3to1, mseD_3to1 = pf.calc_pre_Tdelta_3to1()
    mapD_4to1, mseD_4to1 = pf.calc_pre_Tdelta_4to1()
    mapD_3to2, mseD_3to2 = pf.calc_pre_Tdelta_3to2()
    mapD_4to3, mseD_4to3 = pf.calc_pre_Tdelta_4to3()
    print("D_1to1: ", pf.D_1to1)
    print("mape: ", mapD_1to1, " rmse: ", mseD_1to1)
    print("D_2to1: ", pf.D_2to1)
    print("mape: ", mapD_2to1, " rmse: ", mseD_2to1)
    print("D_3to1: ", pf.D_3to1)
    print("mape: ", mapD_3to1, " rmse: ", mseD_3to1)
    print("D_4to1: ", pf.D_4to1)
    print("mape: ", mapD_4to1, " rmse: ", mseD_4to1)
    print("D_3to2: ", pf.D_3to2)
    print("mape: ", mapD_3to2, " rmse: ", mseD_3to2)
    print("D_4to3: ", pf.D_4to3)
    print("mape: ", mapD_4to3, " rmse: ", mseD_4to3)
    mape, rmse = pf.calc_pre_p4()
    print("E: ", pf.E)
    print("mape: ", mape, " rmse: ", rmse)

    optimize_result=optimizeCCT(db.init_params,pf,db.optimize_result)
    for index in range(len(optimize_result)):
        print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in optimize_result[index].__dict__.items()]))

def testACHP():
    pf_r = fitACHPR(db.pump2_fittings, db.p5_fittings)
    pf_h=fitACHPH(db.pump2_fittings,db.p6_fittings) #TODO 其实这里存在重复计算？

    mape, rmse = pf_r.calc_pre_p5()
    print("K: ", pf_r.K)
    print("mape: ", mape, " rmse: ", rmse)

    J = pf_h.fit_P6(db.p6_fittings)
    mape, rmse = pf_h.calc_pre_p6()
    print("J: ", J)
    print("mape: ", mape, " rmse: ", rmse)

def testOptimizeCalculation(fitResult):
    """优化计算测试"""
    superP = db.init_params
    tempQ = db.optimize_result[0].q * 2
    tempG2 = None
    tempG3 = None
    tempP1 = None

    for index, i in enumerate(db.optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        problem = MyProblem(Q, TS, superP, fitResult) #设置一些可以预先设置的值 & 目标函数 Solution case
        opt = Evoopt(problem) #  GeatpyRunner
        res = opt.run(tempQ,tempG2, tempG3,tempP1)
        tempQ = Q
        tempG2 = opt.G2
        tempG3 = opt.G3
        tempP1 = res[11]

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

if __name__ == '__main__':
    db.load("template.xlsx")  # 加载供拟合的原始数据
    testCCT()
    testACHP()

