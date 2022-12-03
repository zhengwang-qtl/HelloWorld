from typing import Union
from analyze.db import *
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
    B0: float
    B1: float
    B2: float
    B3: float
    B4: float
    B5: float
    B6: float
    B7: float
    B8: float
    B9: float
    B10: float
    B11: float
    B12: float
    B13: float
    B14: float
    B15: float
    B16: float
    B17: float
    B18: float
    B19: float
    B20: float
    B21: float
    B22: float
    B23: float
    MAPE: float
    RMSE: float

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
def fit_chiller_r(datas: main_fittings):
    pf = PumpFit.PumpFitting()
    pf.fit_P1(datas)
    mape, rmse = pf.calc_pre_p1()
    ret = chiller_r_ret()
    ret.B0, ret.B1, ret.B2, ret.B3, ret.B4, ret.B5, ret.B6, ret.B7, ret.B8, ret.B9, ret.B10, ret.B11, ret.B12, ret.B13, ret.B14, ret.B15, ret.B16, ret.B17, ret.B18, ret.B19, ret.B20, ret.B21, ret.B22, ret.B23 = pf.B
    ret.MAPE=mape
    ret.RMSE=rmse
    return ret

