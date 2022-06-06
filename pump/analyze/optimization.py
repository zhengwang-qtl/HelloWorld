from analyze.chiller_coolingTower_optimizer import CCToptimizer
from analyze.chiller_coolingTower_case import CCTcase
from analyze.chiller_coolingTower_free_optimizer import CCTFoptimizer
from analyze.chiller_coolingTower_free_case import CCTFcase
from analyze.airCooled_heatPump_refrigeration_case import ACHPRcase
from analyze.airCooled_heatPump_refrigeration_optimizer import ACHPRoptimizer
from analyze.airCooled_heatPump_heating_case import ACHPHcase
from analyze.airCooled_heatPump_heating_optimizer import ACHPHoptimizer
from analyze.integrated_evaporative_chiller_refrigeration_case import IECRcase
from analyze.integrated_evaporative_chiller_refrigeration_optimizer import IECRoptimizer
from analyze.integrated_evaporative_chiller_heating_case import IECHcase
from analyze.integrated_evaporative_chiller_heating_optimizer import IECHoptimizer


def optimizeCCT(init_params, fit_result, optimize_result):
    tempQ = optimize_result[0].q * 2
    tempG2 = None
    tempG3 = None
    tempP1 = None

    for index, i in enumerate(optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        case = CCTcase(Q, TS, init_params, fit_result)
        optimizer = CCToptimizer(case)
        res = optimizer.run(tempQ, tempG2, tempG3, tempP1)
        tempQ = Q
        tempG2 = res[4]
        tempG3 = res[8]
        tempP1 = res[11]

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

    return optimize_result


def optimizeCCTF(init_params, fit_result, optimize_result):
    for index, i in enumerate(optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        case = CCTFcase(Q, TS, init_params, fit_result)
        optimizer = CCTFoptimizer(case)
        res = optimizer.run()
        """
        返回结果
        T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
        T3（冷却水出水温度）, T4（冷却水回水温度）, G3（冷却水泵流量）, 50 * G3 / G30（冷却水泵频率）,
        t_cooling（冷却塔冷幅）, 
        P2（冷冻水泵功率）, P3（冷却水泵功率）, P4（冷却塔功率）, total_P（总功率）,total_cop（系统COP）, 
        open_num_n1（冷冻水泵开启台数）, open_num_n2（冷却水泵开启台数）, open_num_z (冷却塔开启台数)
        """
        optimize_result[index].t1 = res[0]
        optimize_result[index].t2 = res[1]
        optimize_result[index].G2_lendong = res[2]
        optimize_result[index].fluency_lendong = res[3]

        optimize_result[index].t3 = res[4]
        optimize_result[index].t4 = res[5]
        optimize_result[index].G3_lenque = res[6]
        optimize_result[index].fluency_lenque = res[7]

        optimize_result[index].delta_t = res[8]
        optimize_result[index].p2 = res[9]
        optimize_result[index].p3 = res[10]
        optimize_result[index].p4 = res[11]
        optimize_result[index].p = res[12]
        optimize_result[index].cop = res[13]
        optimize_result[index].n2 = res[14]
        optimize_result[index].n3 = res[15]
        optimize_result[index].z = res[16]
    return optimize_result


def optimizeACHPR(init_params, fit_result, optimize_result):
    tempQ = optimize_result[0].q * 2
    tempG2 = None

    for index, i in enumerate(optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        case = ACHPRcase(Q, TS, init_params, fit_result)
        optimizer = ACHPRoptimizer(case)
        res = optimizer.run(tempQ, tempG2)
        tempQ = Q
        tempG2 = res[4]

        """
        返回结果
        loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
        T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
        P1（主机功率）, P2（冷冻水泵功率）, total_P（总功率）,total_cop（系统COP）, 
        open_num（设备开启台数）
        """
        optimize_result[index].load_percentage = res[0]
        optimize_result[index].system_load_percentage = res[1]
        optimize_result[index].t1 = res[2]
        optimize_result[index].t2 = res[3]
        optimize_result[index].G2_lendong = res[4]
        optimize_result[index].fluency_lendong = res[5]

        optimize_result[index].p1 = res[6]
        optimize_result[index].p2 = res[7]
        optimize_result[index].p = res[8]
        optimize_result[index].cop = res[9]
        optimize_result[index].n = res[10]

    return optimize_result


def optimizeACHPH(init_params, fit_result, optimize_result):
    tempQ = optimize_result[0].q * 2
    tempG2 = None

    for index, i in enumerate(optimize_result):
        Q = abs(i.q)
        TS = i.ts
        if i.q == 0:
            break
        case = ACHPHcase(Q, TS, init_params, fit_result)
        optimizer = ACHPHoptimizer(case)
        res = optimizer.run(tempQ, tempG2)
        tempQ = Q
        tempG2 = res[4]

        """
        返回结果
        loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
        T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
        P1（主机功率）, P2（冷冻水泵功率）, total_P（总功率）,total_cop（系统COP）, 
        open_num（设备开启台数）
        """
        optimize_result[index].load_percentage = res[0]
        optimize_result[index].system_load_percentage = res[1]
        optimize_result[index].t1 = res[2]
        optimize_result[index].t2 = res[3]
        optimize_result[index].G2_lendong = res[4]
        optimize_result[index].fluency_lendong = res[5]

        optimize_result[index].p1 = res[6]
        optimize_result[index].p2 = res[7]
        optimize_result[index].p = res[8]
        optimize_result[index].cop = res[9]
        optimize_result[index].n = res[10]

    return optimize_result


def optimizeIECR(init_params, fit_result, optimize_result):
    tempQ = optimize_result[0].q * 2
    tempG2 = None

    for index, i in enumerate(optimize_result):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        case = IECRcase(Q, TS, init_params, fit_result)
        optimizer = IECRoptimizer(case)
        res = optimizer.run(tempQ, tempG2)
        tempQ = Q
        tempG2 = res[4]

        """
        返回结果
        loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
        T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
        P1（主机功率）, P2（冷冻水泵功率）, total_P（总功率）,total_cop（系统COP）, 
        open_num（设备开启台数）
        """
        optimize_result[index].load_percentage = res[0]
        optimize_result[index].system_load_percentage = res[1]
        optimize_result[index].t1 = res[2]
        optimize_result[index].t2 = res[3]
        optimize_result[index].G2_lendong = res[4]
        optimize_result[index].fluency_lendong = res[5]

        optimize_result[index].p1 = res[6]
        optimize_result[index].p2 = res[7]
        optimize_result[index].p = res[8]
        optimize_result[index].cop = res[9]
        optimize_result[index].n = res[10]

    return optimize_result


def optimizeIECH(init_params, fit_result, optimize_result):
    tempQ = optimize_result[0].q * 2
    tempG2 = None

    for index, i in enumerate(optimize_result):
        Q = abs(i.q)
        TS = i.ts
        if i.q == 0:
            break
        case = IECHcase(Q, TS, init_params, fit_result)
        optimizer = IECHoptimizer(case)
        res = optimizer.run(tempQ, tempG2)
        tempQ = Q
        tempG2 = res[4]

        """
        返回结果
        loading_ration（单机负荷百分比）, system_loading_ration（系统负荷百分比）, 
        T1（冷冻水出水温度）, T2（冷冻水回水温度）, G2（冷冻水泵流量）, 50 * G2 / G20（冷冻水泵频率） , 
        P1（主机功率）, P2（冷冻水泵功率）, total_P（总功率）,total_cop（系统COP）, 
        open_num（设备开启台数）
        """
        optimize_result[index].load_percentage = res[0]
        optimize_result[index].system_load_percentage = res[1]
        optimize_result[index].t1 = res[2]
        optimize_result[index].t2 = res[3]
        optimize_result[index].G2_lendong = res[4]
        optimize_result[index].fluency_lendong = res[5]

        optimize_result[index].p1 = res[6]
        optimize_result[index].p2 = res[7]
        optimize_result[index].p = res[8]
        optimize_result[index].cop = res[9]
        optimize_result[index].n = res[10]

    return optimize_result
