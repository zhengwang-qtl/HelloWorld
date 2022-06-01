from analyze.chiller_coolingTower_optimizer import CCToptimizer
from analyze.chiller_coolingTower_case import CCTcase


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
        tempG2 = optimizer.G2
        tempG3 = optimizer.G3
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
