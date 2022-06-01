from analyze import PumpFit


def fitCCT(p1_fittings, p2_fittings, p3_fittings, CT_fittings_1to1, CT_fittings_2to1, CT_fittings_3to1,
           CT_fittings_4to1, CT_fittings_4to3, CT_fittings_3to2, p4_fittings):
    pf = PumpFit.PumpFitting()
    pf.fit_P1(p1_fittings)  # 主机参数拟合
    pf.fit_P2(p2_fittings)  # 冷冻泵系数拟合
    pf.fit_P3(p3_fittings)  # 冷却泵系数拟合
    # 冷却塔拟合
    pf.fit_Tdelta_1to1(CT_fittings_1to1)
    pf.fit_Tdelta_2to1(CT_fittings_2to1)
    pf.fit_Tdelta_3to1(CT_fittings_3to1)
    pf.fit_Tdelta_4to1(CT_fittings_4to1)
    pf.fit_Tdelta_3to2(CT_fittings_4to3)
    pf.fit_Tdelta_4to3(CT_fittings_3to2)
    pf.fit_P4(p4_fittings)
    return pf
