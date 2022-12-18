from typing import Union, List
from analyze.schema import *
from analyze import PumpFit

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
    D0: Union[float, None] = None
    D1: Union[float, None] = None
    D2: Union[float, None] = None
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
    pf.fit_P2(datas)
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
    t = cooling_tower_cooling_amplitude_req.type
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
        ret.D0, ret.D1, ret.D2 = pf.D_4to1
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
    ret = air_cooled_heat_pump_h_ret()
    ret.J0, ret.J1, ret.J2, ret.J3, ret.J4, ret.J5, ret.J6, ret.J7, ret.J8, ret.J9 = pf.J
    ret.MAPE = mape
    ret.RMSE = rmse
    return ret
