from analyze.db import *
from analyze import PumpFit1
from analyze.Main import *


def test():
    load("template.xlsx") # 加载数据
    pf = PumpFit1.PumpFitting()
    B = pf.fit_P1(main_fittings)
    mape, rmse = pf.calc_pre_p1()
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in B.__dict__.items()]))
    print ("mape: ", mape," rmse: ",rmse)
    A = pf.fit_P2(pump2_fittings)
    mape, rmse =pf.calc_pre_p2()
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in A.__dict__.items()]))
    print ("mape: ", mape, " rmse: ", rmse)
    C = pf.fit_P3(pump3_fittings)
    mape, rmse = pf.calc_pre_p3()
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in C.__dict__.items()]))
    print ("mape: ", mape, " rmse: ", rmse)
    web_data_1to1 = wet_bulb_fittings_1to1
    web_data_2to1 = wet_bulb_fittings_2to1
    web_data_3to1 = wet_bulb_fittings_3to1
    web_data_4to1 = wet_bulb_fittings_4to1
    web_data_3to2 = wet_bulb_fittings_3to2
    web_data_4to3 = wet_bulb_fittings_4to3
    D_1to1 = pf.fit_Tdelta_1to1(web_data_1to1)
    D_2to1 = pf.fit_Tdelta_2to1(web_data_2to1)
    D_3to1 = pf.fit_Tdelta_3to1(web_data_3to1)
    D_4to1 = pf.fit_Tdelta_4to1(web_data_4to1)
    D_3to2 = pf.fit_Tdelta_3to2(web_data_3to2)
    D_4to3 = pf.fit_Tdelta_4to3(web_data_4to3)
    mapD_1to1, mseD_1to1 = pf.calc_pre_Tdelta_1to1()
    mapD_2to1, mseD_2to1 = pf.calc_pre_Tdelta_2to1()
    mapD_3to1, mseD_3to1 = pf.calc_pre_Tdelta_3to1()
    mapD_4to1, mseD_4to1 = pf.calc_pre_Tdelta_4to1()
    mapD_3to2, mseD_3to2 = pf.calc_pre_Tdelta_3to2()
    mapD_4to3, mseD_4to3 = pf.calc_pre_Tdelta_4to3()
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_1to1.__dict__.items()]))
    print ("mape: ", mapD_1to1, " rmse: ", mseD_1to1)
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_2to1.__dict__.items()]))
    print ("mape: ", mapD_2to1, " rmse: ", mseD_2to1)
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_3to1.__dict__.items()]))
    print ("mape: ", mapD_3to1, " rmse: ", mseD_3to1)
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_4to1.__dict__.items()]))
    print ("mape: ", mapD_4to1, " rmse: ", mseD_4to1)
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_3to2.__dict__.items()]))
    print ("mape: ", mapD_3to2, " rmse: ", mseD_3to2)
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in D_4to3.__dict__.items()]))
    print ("mape: ", mapD_4to3, " rmse: ", mseD_4to3)
    E=pf.fit_P4(p4_fittings)
    mape, rmse = pf.calc_pre_p4()
    print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in E.__dict__.items()]))
    print ("mape: ", mape, " rmse: ", rmse)

def optimizeCalculate():
    superP = init_params
    tempQ = optimize_result[0].q * 2
    tempG2 = None
    tempG3 = None

    for index, i in enumerate(optimize_result):
        # print(index)
        Q = i.q
        TS = i.ts
        # print("Q:", Q)
        # print("TS:", TS)
        if i.q == 0:
            break
        opt = Evoopt(Q, TS, superP, PumpFit1)
        res = None
        if abs(Q - tempQ) * 100 / tempQ < float(init_params.yuzhi):
            # print("-

            res = opt.run(tempG2, tempG3)
            pass
        else:
            res = opt.run()
            tempQ = Q
            tempG2 = opt.G2
            tempG3 = opt.G3
            # print("此时Q：{:s}".format(str(tempQ)))

        optimize_result[index].load_percentage = res[0]
        optimize_result[index].system_load_percentage = res[1]
        optimize_result[index].t1 = res[2]
        optimize_result[index].t2 = res[3]
        optimize_result[index].G2_lendong = res[4]
        optimize_result[index].fluency_lendong = res[5]

        optimize_result[index].t3 = res[6]
        optimize_result[index].t4 = res[7]
        optimize_result[index].G3_lenque = res[8]
        optimize_result[index].fluency_lenque = res[9]

        optimize_result[index].delta_t = res[10]
        optimize_result[index].p1 = res[11]
        optimize_result[index].p2 = res[12]
        optimize_result[index].p3 = res[13]
        optimize_result[index].p4 = res[14]
        optimize_result[index].p = res[15]
        optimize_result[index].cop = res[16]
        optimize_result[index].n = res[17]
        print('\n'.join(['{0}: {1}'.format(item[0], item[1]) for item in res.__dict__.items()]))


if __name__ == '__main__':
    print('hello world!')
    test()
    optimizeCalculate()


