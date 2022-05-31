# 初始化参数
class InitialParameters:
    def __init__(self):
        self.calcType = 0  # 冷却塔计算类型
        self.lengque_maxn = 4  # 冷水机组最大台数
        # 冷水机组设定
        self.q = 2814.0  # 单台额定冷水机组额定负荷Qs，KW
        self.n = 3  # 冷水机组台数，台
        self.efficiency_range = 80.0  # 单台高效率冷负荷范围η，%
        self.t3_min = 21.0  # 冷却塔出水（机组允许）最低温度T3
        # 冷冻水泵设定
        self.h = 41.0  # 单台冷冻水泵扬程H，m
        self.p20 = 90.0  # 单台冷冻水泵功率P2，Kw
        self.G20 = 533.0  # 单台冷冻水泵的额定流量G，m3/h
        self.q_min = 422.0  # 单台冷冻水泵最低负荷Qq,Kw
        # 冷冻水泵台数，台  3 ？？？
        # 冷却水泵设定
        self.G30 = 650.0  # 单台冷却水泵的额定流量G，m3/h
        # 冷却塔设定 数据缺失???
        self.P0 = 22.0  # 单台冷却塔功率P0，Kw
        # 进出口温差设定
        self.delta_t1_range = (4.0, 10.0)  # 冷冻水进出口温差 T2 - T1
        self.delta_t2_range = (4.0, 10.0)  # 冷却水进出口温差 T4 - T3
        self.mu = 0.6  # 冷冻水泵变频频率下限值μ
        self.lamb = 0.65  # 冷冻水泵频率下限值λ
        self.yuzhi = 5  # 优化计算设定值%

        self.load_rat = [100, 95, 90, 85, 80, 75, 70, 65, 60]  # 负荷率
        self.t1_range = []  # 冷冻水出水温度T1


# 主机参数拟合
class MainFitting:
    def __init__(self):
        self.load_percentage = 100.0  # 负荷百分比，%
        self.q = 0.0
        self.p1 = 0.0
        self.t1 = 0.0
        self.t2 = 0.0
        self.t3 = 0.0
        self.t4 = 0.0
        self.cop = 0.0


# 冷冻水泵参数拟合
class Pump2Fitting:
    def __init__(self):
        self.g2 = 0.0  # 流量（m3/h)
        self.p2 = 0.0  # 轴功率(kw)


# 冷却水泵参数拟合
class Pump3Fitting:
    def __init__(self):
        self.g3 = 0.0  # 流量（m3/h)
        self.p3 = 0.0  # 轴功率(kw)


# 冷却塔 一对一
class WetBulbFitting_1to1:
    def __init__(self):
        self.temp = 0.0  # 湿球温度
        self.amplitude = 0.0  # 冷幅


# 冷却塔 二对一
class WetBulbFitting_2to1:
    def __init__(self):
        self.temp = 0.0
        self.amplitude = 0.0


# 冷却塔 三对一
class WetBulbFitting_3to1:
    def __init__(self):
        self.temp = 0.0
        self.amplitude = 0.0


# 冷却塔 四对一
class WetBulbFitting_4to1:
    def __init__(self):
        self.temp = 0.0
        self.amplitude = 0.0


# 冷却塔 三对二
class WetBulbFitting_3to2:
    def __init__(self):
        self.temp = 0.0
        self.amplitude = 0.0


# 冷却塔 四对三
class WetBulbFitting_4to3:
    def __init__(self):
        self.temp = 0.0
        self.amplitude = 0.0


# 冷却塔 P4功率与流量的拟合
class P4Fitting:
    def __init__(self):
        self.g = 0.0  # 水流量G（m3/h）
        self.p4 = 0.0  # 功率P4（Kw）


# 拟合结果
class FittingCoefficients:
    def __init__(self):
        self.a = []  # 0-2 冷冻泵系数
        self.b = []  # 0-23 主机系数
        self.c = []  # 0-2 冷却泵系数
        # 冷却塔系数
        self.d_1to1 = []  # 0-2
        self.d_2to1 = []  # 0-2
        self.d_3to1 = []  # 0-2
        self.d_4to1 = []  # 0-2
        self.d_3to2 = []  # 0-2
        self.d_4to3 = []  # 0-2
        self.e = []  # 0-3 # 系数(功率)


# 优化计算结果
class OptimizeResult:
    def __init__(self):
        self.year = ""
        self.mon = ""
        self.day = ""
        self.hour = ""
        self.q = 0.0  # 负荷Q，Kw
        self.ts = 0.0  # 湿球温度Ts，℃
        self.load_percentage = None  # 负荷百分比
        self.system_load_percentage = None  #
        self.t1 = None  # 冷冻水出水温度，℃
        self.t2 = None  # 冷冻水回水温度，℃
        self.G2_lendong = None  # 冷冻水泵流量，m3/h
        self.fluency_lendong = None  # 冷冻水泵频率，Hz

        self.t3 = None  # 冷却水出水温度，℃
        self.t4 = None  # 冷却水回水温度，℃
        self.G3_lenque = None  # 冷却水泵流量，m3/h
        self.fluency_lenque = None  # 冷却水泵频率，Hz
        self.delta_t = None  # 冷却塔冷幅
        self.p1 = None  # 主机功率，kw
        self.p2 = None  # 冷冻水泵功率，kw
        self.p3 = None  # 冷却水泵功率，kw
        self.p4 = None  # 冷却塔功率，kw
        self.p = None  # 总功率，kw
        self.cop = None  # 系统COP, kw
        self.n = 0  # 设备开启台数


# Q值变化值
class QDeltaEntry:
    def __init__(self):
        self.year = "2021"
        self.mon = "1"
        self.day = "1"
        self.hour = "1"
        self.Q = "1"  # 负荷Q，Kw
        self.Ts = "1"  # 湿球温度Ts，℃
        self.T = "1"  # 干球温度T，℃

# 蒸发冷一体机组系数（制冷工况）
class P5Fitting:
    def __init__(self):
        self.T0 = 0.0
        self.T1 = 0.0
        self.T2 = 0.0
        self.Q = 0.0
        self.P = 0.0

# 风冷热泵机组系数（制热工况）
class P6Fitting:
    def __init__(self):
        self.T0 = 0.0
        self.T1 = 0.0
        self.Q = 0.0
        self.P = 0.0
