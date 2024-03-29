from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List
from analyze.schema import *
from analyze import PumpFit

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)


# 主机参数拟合
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class chiller_r_ret(BaseModel):
    B0: Union[float, None] = None
    B1: Union[float, None] = None
    B2: Union[float, None] = None
    B3: Union[float, None] = None
    B4: Union[float, None] = None
    B5: Union[float, None] = None
    B6: Union[float, None] = None
    B7: Union[float, None] = None
    B8: Union[float, None] = None
    B9: Union[float, None] = None
    B10: Union[float, None] = None
    B11: Union[float, None] = None
    B12: Union[float, None] = None
    B13: Union[float, None] = None
    B14: Union[float, None] = None
    B15: Union[float, None] = None
    B16: Union[float, None] = None
    B17: Union[float, None] = None
    B18: Union[float, None] = None
    B19: Union[float, None] = None
    B20: Union[float, None] = None
    B21: Union[float, None] = None
    B22: Union[float, None] = None
    B23: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class chilled_water_pump_ret(BaseModel):
    A0: Union[float, None] = None
    A1: Union[float, None] = None
    A2: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class cooling_water_pump_ret(BaseModel):
    C0: Union[float, None] = None
    C1: Union[float, None] = None
    C2: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class cooling_tower_power_ret(BaseModel):
    E0: Union[float, None] = None
    E1: Union[float, None] = None
    E2: Union[float, None] = None
    E3: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class cooling_tower_cooling_amplitude_req(BaseModel):
    type: str
    datas: List[WetBulbFitting]


class cooling_tower_cooling_amplitude_ret(BaseModel):
    type: Union[str, None] = None
    D0: Union[float, None] = None
    D1: Union[float, None] = None
    D2: Union[float, None] = None
    D3: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class air_cooled_heat_pump_r_ret(BaseModel):
    F0: Union[float, None] = None
    F1: Union[float, None] = None
    F2: Union[float, None] = None
    F3: Union[float, None] = None
    F4: Union[float, None] = None
    F5: Union[float, None] = None
    F6: Union[float, None] = None
    F7: Union[float, None] = None
    F8: Union[float, None] = None
    F9: Union[float, None] = None
    F10: Union[float, None] = None
    F11: Union[float, None] = None
    F12: Union[float, None] = None
    F13: Union[float, None] = None
    F14: Union[float, None] = None
    F15: Union[float, None] = None
    F16: Union[float, None] = None
    F17: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class air_cooled_heat_pump_h_ret(BaseModel):
    L0: Union[float, None] = None
    L1: Union[float, None] = None
    L2: Union[float, None] = None
    L3: Union[float, None] = None
    L4: Union[float, None] = None
    L5: Union[float, None] = None
    L6: Union[float, None] = None
    L7: Union[float, None] = None
    L8: Union[float, None] = None
    L9: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class integrated_evaporative_chiller_r_ret(BaseModel):
    K0: Union[float, None] = None
    K1: Union[float, None] = None
    K2: Union[float, None] = None
    K3: Union[float, None] = None
    K4: Union[float, None] = None
    K5: Union[float, None] = None
    K6: Union[float, None] = None
    K7: Union[float, None] = None
    K8: Union[float, None] = None
    K9: Union[float, None] = None
    K10: Union[float, None] = None
    K11: Union[float, None] = None
    K12: Union[float, None] = None
    K13: Union[float, None] = None
    K14: Union[float, None] = None
    K15: Union[float, None] = None
    K16: Union[float, None] = None
    K17: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class integrated_evaporative_chiller_h_ret(BaseModel):
    J0: Union[float, None] = None
    J1: Union[float, None] = None
    J2: Union[float, None] = None
    J3: Union[float, None] = None
    J4: Union[float, None] = None
    J5: Union[float, None] = None
    J6: Union[float, None] = None
    J7: Union[float, None] = None
    J8: Union[float, None] = None
    J9: Union[float, None] = None
    MAPE: Union[float, None] = None
    RMSE: Union[float, None] = None


class cooling_tower_union(BaseModel):
    power: Union[cooling_tower_power_ret, None] = None
    cooling_amplitude_s: Union[List[cooling_tower_cooling_amplitude_ret], None] = None


class param_air_cooled_heat_pump(BaseModel):
    heat: Union[air_cooled_heat_pump_h_ret, None] = None
    refrigeration: Union[air_cooled_heat_pump_r_ret, None] = None


class param_integrated_evaporative_chiller(BaseModel):
    heat: Union[integrated_evaporative_chiller_h_ret, None] = None
    refrigeration: Union[integrated_evaporative_chiller_r_ret, None] = None


class param_chiller(BaseModel):
    min: Union[chiller_r_ret, None] = None
    max: Union[chiller_r_ret, None] = None


class param_chilled_water_pump(BaseModel):
    min_first: Union[chilled_water_pump_ret, None] = None
    min_second: Union[chilled_water_pump_ret, None] = None
    max_first: Union[chilled_water_pump_ret, None] = None
    max_second: Union[chilled_water_pump_ret, None] = None


class param_heat_water_pump(BaseModel):
    min_first: Union[chilled_water_pump_ret, None] = None
    min_second: Union[chilled_water_pump_ret, None] = None
    max_first: Union[chilled_water_pump_ret, None] = None
    max_second: Union[chilled_water_pump_ret, None] = None


class param_cooling_water_pump(BaseModel):
    min: Union[cooling_water_pump_ret, None] = None
    max: Union[cooling_water_pump_ret, None] = None


class param_cooling_tower(BaseModel):
    min: Union[cooling_tower_union, None] = None
    max: Union[cooling_tower_union, None] = None


class Params(BaseModel):
    chiller: Union[param_chiller, None] = None
    chilled_water_pump: Union[param_chilled_water_pump, None] = None
    chilled_water_pump: Union[param_heat_water_pump, None] = None
    cooling_water_pump: Union[param_cooling_water_pump, None] = None
    cooling_tower: Union[param_cooling_tower, None] = None
    air_cooled_heat_pump: Union[param_air_cooled_heat_pump, None] = None
    integrated_evaporative_chiller: Union[param_integrated_evaporative_chiller, None] = None


class op_data(BaseModel):
    year: Union[int, None] = None
    month: Union[int, None] = None
    day: Union[int, None] = None
    hour: Union[int, None] = None
    q: Union[float, None] = None  # 负荷，kw
    ts: Union[float, None] = None  # 湿球温度
    t: Union[float, None] = None  # 干球温度
    load_percentage: Union[float, None] = None  # 单台主机负荷百分比
    system_load_percentage: Union[float, None] = None  # 系统负荷百分比
    first_cold_t1: Union[float, None] = None  # 一次泵冷冻水出水温度,℃
    first_cold_t2: Union[float, None] = None  # 一次泵冷冻水回水温度,℃
    min_first_cold_g2: Union[float, None] = None  # 一次泵小冷冻水泵流量,m3/h
    min_first_cold_f2: Union[float, None] = None  # 一次泵小冷冻水泵频率,Hz
    min_first_cold_n: Union[float, None] = None  # 一次泵小冷冻水泵运行台数
    max_first_cold_g2: Union[float, None] = None  # 一次泵大冷冻水泵流量,m3/h
    max_first_cold_f2: Union[float, None] = None  # 一次泵大冷冻水泵频率,Hz
    max_first_cold_n: Union[float, None] = None  # 一次泵大冷冻水泵运行台数
    second_cold_t1: Union[float, None] = None  # 二次泵冷冻水出水温度,℃
    second_cold_t2: Union[float, None] = None  # 二次泵冷冻水回水温度,℃
    min_second_cold_g2: Union[float, None] = None  # 二次泵小冷冻水泵流量,m3/h
    min_second_cold_f2: Union[float, None] = None  # 二次泵小冷冻水泵频率,Hz
    min_second_cold_n: Union[float, None] = None  # 二次泵小冷冻水泵运行台数
    max_second_cold_g2: Union[float, None] = None  # 二次泵大冷冻水泵流量,m3/h
    max_second_cold_f2: Union[float, None] = None  # 二次泵大冷冻水泵频率,Hz
    max_second_cold_n: Union[float, None] = None  # 二次泵大冷冻水泵运行台数
    first_heat_t1: Union[float, None] = None  # 一次泵热水出水温度,℃
    first_heat_t2: Union[float, None] = None  # 一次泵热水回水温度,℃
    min_first_heat_g2: Union[float, None] = None  # 一次泵小热水泵流量,m3/h
    min_first_heat_f2: Union[float, None] = None  # 一次泵小热水泵频率,Hz
    min_first_heat_n: Union[float, None] = None  # 一次泵小热水泵运行台数
    max_first_heat_g2: Union[float, None] = None  # 一次泵大热水泵流量,m3/h
    max_first_heat_f2: Union[float, None] = None  # 一次泵大热水泵频率,Hz
    max_first_heat_n: Union[float, None] = None  # 一次泵大热水泵运行台数
    second_heat_t1: Union[float, None] = None  # 二次泵热水出水温度,℃
    second_heat_t2: Union[float, None] = None  # 二次泵热水回水温度,℃
    min_second_heat_g2: Union[float, None] = None  # 二次泵小热水泵流量,m3/h
    min_second_heat_f2: Union[float, None] = None  # 二次泵小热水泵频率,Hz
    min_second_heat_n: Union[float, None] = None  # 二次泵小热水泵运行台数
    max_second_heat_g2: Union[float, None] = None  # 二次泵大热水泵流量,m3/h
    max_second_heat_f2: Union[float, None] = None  # 二次泵大热水泵频率,Hz
    max_second_heat_n: Union[float, None] = None  # 二次泵大热水泵运行台数
    cool_t3: Union[float, None] = None  # 冷却水出水温度,℃
    cool_t4: Union[float, None] = None  # 冷却水回水温度,℃
    min_g3: Union[float, None] = None  # 小冷却水泵流量,m3/h
    min_f3: Union[float, None] = None  # 小冷却水泵频率,Hz
    min_pump_n: Union[float, None] = None  # 小冷却水泵运行台数
    max_g3: Union[float, None] = None  # 大冷却水泵流量,m3/h
    max_f3: Union[float, None] = None  # 大冷却水泵频率,Hz
    max_pump_n: Union[float, None] = None  # 大冷却水泵运行台数
    min_td: Union[float, None] = None  # 小冷却塔冷幅
    max_td: Union[float, None] = None  # 大冷却塔冷幅
    min_tower_n: Union[float, None] = None  # 小冷却塔运行台数
    max_tower_n: Union[float, None] = None  # 大冷却塔运行台数
    min_chiller_n: Union[float, None] = None  # 小冷水机组开启台数
    max_chiller_n: Union[float, None] = None  # 大冷水机组开启台数
    air_cooled_heat_pump_n: Union[float, None] = None  # 风冷热泵机组开启台数
    integrated_evaporative_chiller_n: Union[float, None] = None  # 蒸发冷一体机组开启台数
    min_chilled_p1: Union[float, None] = None  # 小制冷主机功率,kw
    max_chilled_p1: Union[float, None] = None  # 大制冷主机功率,kw
    min_air_cooled_heat_pump_p1: Union[float, None] = None  # 小热泵主机功率,kw
    max_air_cooled_heat_pump_p1: Union[float, None] = None  # 大热泵主机功率,kw
    min_integrated_evaporative_chiller_p1: Union[float, None] = None  # 小蒸发冷主机功率,kw
    max_integrated_evaporative_chiller_p1: Union[float, None] = None  # 大蒸发冷主机功率,kw
    min_first_cold_pump_p2: Union[float, None] = None  # 一次泵小冷冻水泵功率,kw
    max_first_cold_pump_p2: Union[float, None] = None  # 一次泵大冷冻水泵功率,kw
    min_first_heat_pump_p2: Union[float, None] = None  # 一次泵小热水泵功率,kw
    max_first_heat_pump_p2: Union[float, None] = None  # 一次泵大热水泵功率,kw
    min_second_cold_pump_p2: Union[float, None] = None  # 二次泵小冷冻水泵功率,kw
    max_second_cold_pump_p2: Union[float, None] = None  # 二次泵大冷冻水泵功率,kw
    min_second_heat_pump_p2: Union[float, None] = None  # 二次泵小热水泵功率,kw
    max_second_heat_pump_p2: Union[float, None] = None  # 二次泵大热水泵功率,kw
    min_cool_pump_p3: Union[float, None] = None  # 小冷却水泵功率,kw
    max_cool_pump_p3: Union[float, None] = None  # 大冷却水泵功率,kw
    min_tower_p4: Union[float, None] = None  # 小冷却塔功率,kw
    max_tower_p4: Union[float, None] = None  # 大冷却塔功率,kw
    p: Union[float, None] = None  # 总功率,kw
    cop: Union[float, None] = None  # 系统COP, kw


class optimal_calculation_req(BaseModel):
    init: Union[Init, None] = None
    params: Union[Params, None] = None
    datas: Union[List[op_data], None] = None


class optimal_calculation_ret(BaseModel):
    datas: Union[List[op_data], None] = None
    count: Union[int, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/fitting/chiller_r")
def fit_chiller_r(datas: List[MainFitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P1(datas)
    mape, rmse = pf.calc_pre_p1()
    ret = chiller_r_ret()
    ret.B0, ret.B1, ret.B2, ret.B3, ret.B4, ret.B5, ret.B6, ret.B7, ret.B8, ret.B9, ret.B10, ret.B11, ret.B12, ret.B13, ret.B14, ret.B15, ret.B16, ret.B17, ret.B18, ret.B19, ret.B20, ret.B21, ret.B22, ret.B23 = pf.B
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/chilled_water_pump")
def fit_chilled_water_pump(datas: List[Pump2Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P2(datas)
    mape, rmse = pf.calc_pre_p2()
    ret = chilled_water_pump_ret()
    ret.A0, ret.A1, ret.A2 = pf.A
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/cooling_water_pump")
def fit_cooling_water_pump(datas: List[Pump3Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P3(datas)
    mape, rmse = pf.calc_pre_p3()
    ret = cooling_water_pump_ret()
    ret.C0, ret.C1, ret.C2 = pf.C
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/cooling_tower/power")
def fit_cooling_tower_power(datas: List[P4Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P4(datas)
    mape, rmse = pf.calc_pre_p4()
    ret = cooling_tower_power_ret()
    ret.E0, ret.E1, ret.E2, ret.E3 = pf.E
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/cooling_tower/cooling_amplitude")
def fit_cooling_tower_cooling_amplitude(datas: cooling_tower_cooling_amplitude_req):
    ret = cooling_tower_cooling_amplitude_ret()
    pf = PumpFit.PumpFitting()
    t = datas.type
    if t == "2to1":
        pf.fit_Tdelta_2to1(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_2to1()
        ret.D0, ret.D1, ret.D2 = pf.D_2to1
    elif t == "3to1":
        pf.fit_Tdelta_3to1(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_3to1()
        ret.D0, ret.D1, ret.D2 = pf.D_3to1
    elif t == "4to1":
        pf.fit_Tdelta_4to1(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_4to1()
        ret.D0, ret.D1, ret.D2, ret.D3 = pf.D_4to1
    elif t == "3to2":
        pf.fit_Tdelta_3to2(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_3to2()
        ret.D0, ret.D1, ret.D2 = pf.D_3to2
    elif t == "4to3":
        pf.fit_Tdelta_4to3(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_4to3()
        ret.D0, ret.D1, ret.D2 = pf.D_4to3
    else:
        pf.fit_Tdelta_1to1(datas.datas)
        ret.MAPE, ret.RMSE = pf.calc_pre_Tdelta_1to1()
        ret.D0, ret.D1, ret.D2 = pf.D_1to1
    return ret


@app.post("/fitting/air_cooled_heat_pump_r")
def fit_air_cooled_heat_pump_r(datas: List[P5Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P5(datas)
    mape, rmse = pf.calc_pre_p5()
    ret = air_cooled_heat_pump_r_ret()
    ret.F0, ret.F1, ret.F2, ret.F3, ret.F4, ret.F5, ret.F6, ret.F7, ret.F8, ret.F9, ret.F10, ret.F11, ret.F12, ret.F13, ret.F14, ret.F15, ret.F16, ret.F17 = pf.K
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/air_cooled_heat_pump_h")
def fit_air_cooled_heat_pump_h(datas: List[P6Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P6(datas)
    mape, rmse = pf.calc_pre_p6()
    ret = air_cooled_heat_pump_h_ret()
    ret.L0, ret.L1, ret.L2, ret.L3, ret.L4, ret.L5, ret.L6, ret.L7, ret.L8, ret.L9 = pf.J
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/integrated_evaporative_chiller_r")
def fit_integrated_evaporative_chiller_r(datas: List[P5Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P5(datas)
    mape, rmse = pf.calc_pre_p5()
    ret = integrated_evaporative_chiller_r_ret()
    ret.K0, ret.K1, ret.K2, ret.K3, ret.K4, ret.K5, ret.K6, ret.K7, ret.K8, ret.K9, ret.K10, ret.K11, ret.K12, ret.K13, ret.K14, ret.K15, ret.K16, ret.K17 = pf.K
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/fitting/integrated_evaporative_chiller_h")
def fit_integrated_evaporative_chiller_h(datas: List[P6Fitting]):
    pf = PumpFit.PumpFitting()
    pf.fit_P6(datas)
    mape, rmse = pf.calc_pre_p6()
    ret = integrated_evaporative_chiller_h_ret()
    ret.J0, ret.J1, ret.J2, ret.J3, ret.J4, ret.J5, ret.J6, ret.J7, ret.J8, ret.J9 = pf.J
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret


@app.post("/optimal_calculation")
def optimal_calculation(req: optimal_calculation_req):
    print("=========")
    print(req.json())
    print("=========")
    result = optimize(req)
    print(result.json())
    return result


@app.post("/optimal_calculation_test")
def optimal_calculation(req: cooling_tower_union):
    return 100


DEVICE_CCT = "CCT"
DEVICE_ACHP = "ACHP"
DEVICE_IEC = "IEC"
INVALID_DEVICE = "INVALID_DEVICE"


# 冷源 0(冷水机组+冷却塔)，1(冷水机组+冷却塔(免费)) ，2（一体式蒸发冷水机组（单冷，冷暖))，3(四管制风冷热泵)，4（热泵（单冷，冷暖））
def getColdSource(code):
    # 冷源chiller(冷水机组),integrated_evaporative_chiller（蒸发冷一体机),air_cooled_heat_pump（空气源热泵）
    if code == "chiller":
        return DEVICE_CCT
    elif code == "integrated_evaporative_chiller":
        return DEVICE_IEC
    elif code == "integrated_evaporative_chiller":
        return DEVICE_ACHP
    else:
        return INVALID_DEVICE


# 热源  0（锅炉），2（一体式蒸发冷水机组），3（四管制风冷热泵），4（热泵）
def getHeatSource(code):
    # boiler（锅炉）,integrated_evaporative_chiller（蒸发冷一体机),	air_cooled_heat_pump（空气源热泵）
    if code == "integrated_evaporative_chiller":
        return DEVICE_IEC
    elif code == "air_cooled_heat_pump":
        return DEVICE_ACHP
    else:
        return INVALID_DEVICE


def optimize(req: optimal_calculation_req):
    ret = optimal_calculation_ret()
    datas = optimizeT(getColdSource(req.init.basic.cold_source), getColdSource(req.init.basic.heat_source), req.init,
                      req.params, req.datas)
    ret.datas = datas
    ret.count = len(datas)
    return ret


def optimizeT(codeSource: str, heatSource: str, init: Init, params: Params, datas: List[op_data]):
    isFixG = False
    if init.basic.optimize_calculation_model == "optimize_calculation_model":
        isFixG = True

    tempQ = 0
    tempG2 = 0
    tempG3 = 0
    tempP1 = 0
    tempT1 = 0
    tempT2 = 0
    tempT3 = 0
    tempT4 = 0
    free = False
    cooling_tower_free_sum = 1
    if init.cooling_tower_free_calculation.cooling_tower_free_sum is not None:
        cooling_tower_free_sum = init.cooling_tower_free_calculation.cooling_tower_free_sum
    count = 0

    for index, i in enumerate(datas):
        Q = i.q
        TS = i.ts
        if i.q == 0:
            break
        if Q > 0:  # 制冷
            if codeSource == DEVICE_CCT:
                if init.cooling_tower_free_calculation.cooling_tower_free == "cooling_tower_free_y":
                    case = CCTFcase(Q, TS, init, params)
                    free = False
                    if case.shouldOp is False:  # 免费冷源
                        count = count + 1
                        if count >= cooling_tower_free_sum:
                            free = True
                        else:
                            preCount = count
                            for j in range(cooling_tower_free_sum - count):
                                preIndex = index + j + 1
                                if preIndex >= len(datas):
                                    break
                                preCase = CCTFcase(datas[preIndex].q, datas[preIndex].ts, init, params)
                                if preCase.shouldOp is False:
                                    preCount = preCount + 1
                                    if preCount >= cooling_tower_free_sum:
                                        free = True
                                        break
                                else:
                                    break
                    else:
                        count = 0
                    if free is True:  # 免费冷源
                        optimizer = CCTFoptimizer(case)
                        res = optimizer.run()
                    else:  # 优化计算
                        case = CCTcase(Q, TS, init, params)
                        optimizer = CCToptimizer(case)
                        res = optimizer.run(isFixG, tempQ, tempG2, tempG3, tempP1, tempT1, tempT2, tempT3, tempT4)
                else:
                    case = CCTcase(Q, TS, init, params)
                    optimizer = CCToptimizer(case)
                    res = optimizer.run(isFixG, tempQ, tempG2, tempG3, tempP1, tempT1, tempT2, tempT3, tempT4)
                    free = False
            elif codeSource == DEVICE_ACHP:
                case = ACHPRcase(Q, TS, init, params)
                optimizer = ACHPRoptimizer(case)
                res = optimizer.run(tempQ, tempG2, tempG3, tempP1)
            elif codeSource == DEVICE_IEC:
                case = IECRcase(Q, TS, init, params)
                optimizer = IECRoptimizer(case)
                res = optimizer.run(tempQ, tempG2, tempG3, tempP1)
            else:
                raise HTTPException(status_code=401, detail="Invalid cold source!")
        else:  # 制热
            if codeSource == DEVICE_ACHP:
                case = ACHPHcase(Q, TS, init, params)
                optimizer = ACHPHoptimizer(case)
                res = optimizer.run(tempQ, tempG2, tempG3, tempP1)
            elif codeSource == DEVICE_IEC:
                case = IECHcase(Q, TS, init, params)
                optimizer = IECHoptimizer(case)
                res = optimizer.run(tempQ, tempG2, tempG3, tempP1)
            else:
                raise HTTPException(status_code=401, detail="Invalid heat source!")

        # 增加判断，然后直接复制 & 重新计算
        if res[19] is True:
            print("HAS OP:", Q)
            tempQ = Q
            tempG2 = res[4]
            tempG3 = res[8]
            tempP1 = res[11] / res[17]  # 单台P1
            tempT1 = res[2]
            tempT2 = res[3]
            tempT3 = res[6]
            tempT4 = res[7]
        else:
            if free is True:
                tempG2 = 0  # 置为0，使得下一次优化计算必定重新优化计算
                print("FREE: ", Q)
            else:
                print("NO OP:", Q)

        datas[index].load_percentage = res[0]
        datas[index].system_load_percentage = res[1]
        datas[index].first_cold_t1 = res[2]
        datas[index].first_cold_t2 = res[3]
        datas[index].min_first_cold_g2 = res[4]
        datas[index].min_first_cold_f2 = res[5]

        datas[index].cool_t3 = res[6]
        datas[index].cool_t4 = res[7]
        datas[index].min_g3 = res[8]
        datas[index].min_f3 = res[9]

        datas[index].min_td = res[10]
        datas[index].min_chilled_p1 = res[11]
        datas[index].min_first_cold_pump_p2 = res[12]
        datas[index].min_cool_pump_p3 = res[13]
        datas[index].min_tower_p4 = res[14]
        datas[index].p = res[15]
        datas[index].cop = res[16]
        if free is True:
            datas[index].min_chiller_n = 0
        else:
            datas[index].min_chiller_n = res[17]
        datas[index].min_first_cold_n = res[17]
        datas[index].min_pump_n = res[17]
        datas[index].min_tower_n = res[18]
    return datas
