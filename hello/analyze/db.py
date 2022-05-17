import base64
import timeit

from analyze.schema import *
from analyze.template import template_file_base64
from typing import List
import openpyxl
import os

init_params = InitialParameters()
main_fittings: List[MainFitting] = list()
pump2_fittings: List[Pump2Fitting] = list()
pump3_fittings: List[Pump3Fitting] = list()
wet_bulb_fittings_1to1: List[WetBulbFitting_1to1] = list()
wet_bulb_fittings_2to1: List[WetBulbFitting_2to1] = list()
wet_bulb_fittings_3to1: List[WetBulbFitting_3to1] = list()
wet_bulb_fittings_4to1: List[WetBulbFitting_4to1] = list()
wet_bulb_fittings_3to2: List[WetBulbFitting_3to2] = list()
wet_bulb_fittings_4to3: List[WetBulbFitting_4to3] = list()
p4_fittings: List[P4Fitting] = list()

fitting_coefficients = FittingCoefficients()  # 拟合结果
optimize_result: List[OptimizeResult] = list()  # 优化结果
q_delta: List[QDeltaEntry] = list()  # Q值变化


def load(path: str):
    global init_params, main_fittings, pump2_fittings, pump3_fittings, wet_bulb_fittings_1to1, wet_bulb_fittings_2to1, wet_bulb_fittings_3to1, wet_bulb_fittings_4to1, wet_bulb_fittings_3to2, wet_bulb_fittings_4to3, p4_fittings, \
        fitting_coefficients, optimize_result, q_delta
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=True)
    for sheet in wb:
        if sheet.title == "q值变化值":
            q_delta = list()
            optimize_result = list()
            for idx, row in enumerate(sheet.rows):
                if idx <= 0:
                    continue
                entry = QDeltaEntry()
                entry.year = row[0].value
                entry.mon = row[1].value
                entry.day = row[2].value
                entry.hour = row[3].value
                entry.Q = row[4].value
                entry.Ts = row[5].value
                entry.T = row[6].value
                q_delta.append(entry)
                temp = OptimizeResult()
                temp.year = row[0].value
                temp.mon = row[1].value
                temp.day = row[2].value
                temp.hour = row[3].value
                temp.q = float(row[4].value)
                temp.ts = float(row[5].value)
                optimize_result.append(temp)
                # print(len(optimize_result))
        elif sheet.title == "参数初始值设定":

            init_params.q = float(sheet["B4"].value)
            init_params.n = int(sheet["B5"].value)
            init_params.efficiency_range = float(sheet["B6"].value)
            init_params.t3_min = float(sheet["B7"].value)
            init_params.G20 = float(sheet["B9"].value)
            init_params.G30 = float(sheet["B14"].value)
            init_params.h = float(sheet["B10"].value)
            init_params.p2 = float(sheet["B11"].value)
            init_params.delta_t1_range = (float(sheet["B24"].value), float(sheet["C24"].value))
            init_params.delta_t2_range = (float(sheet["B25"].value), float(sheet["C25"].value))
            init_params.q_min = float(sheet["B26"].value)
            # init_params.p20 = float(sheet["B27"].value)
            init_params.P0 = float(sheet["B21"].value)
            init_params.mu = float(sheet["B27"].value)
            init_params.lamb = float(sheet["B28"].value)
            init_params.lengque_maxn = float(sheet["B22"].value)
            init_params.yuzhi = float(sheet["B29"].value)

            for i in range(9):
                init_params.t1_range.append(float(sheet.cell(2, i + 2).value))

        elif sheet.title == "主机参数拟合":
            main_fittings = list()
            for rowidx, row in enumerate(sheet.rows):
                if rowidx <= 1:
                    continue
                if row[1].value is None:
                    break

                entry = MainFitting()
                entry.q = float(row[1].value)
                entry.p1 = float(row[2].value)
                entry.t1 = float(row[3].value)
                entry.t2 = float(row[4].value)
                entry.t3 = float(row[5].value)
                entry.t4 = float(row[6].value)
                entry.cop = float(row[7].value)
                main_fittings.append(entry)
        elif sheet.title == "水泵性能参数拟合":
            pump2_fittings = list()
            for i in range(5):
                entry = Pump2Fitting()
                entry.g2 = float(sheet.cell(4, 3 + i * 2).value)
                entry.p2 = float(sheet.cell(4, 4 + i * 2).value)
                pump2_fittings.append(entry)

            pump3_fittings = list()
            for i in range(5):
                entry = Pump3Fitting()
                entry.g3 = float(sheet.cell(11, 3 + i * 2).value)
                entry.p3 = float(sheet.cell(11, 4 + i * 2).value)
                pump3_fittings.append(entry)
        elif sheet.title == "冷却塔拟合":
            # print("4")
            i = 0
            wet_bulb_fittings_1to1 = list()
            while sheet.cell(3 + i, 1).value is not None:
                entry = WetBulbFitting_1to1()
                entry.temp = float(sheet.cell(3 + i, 1).value)
                entry.amplitude = float(sheet.cell(3 + i, 2).value)
                wet_bulb_fittings_1to1.append(entry)
                i += 1

            i = 0
            wet_bulb_fittings_2to1 = list()
            while sheet.cell(3 + i, 3).value is not None:
                entry = WetBulbFitting_2to1()
                entry.temp = float(sheet.cell(3 + i, 3).value)
                entry.amplitude = float(sheet.cell(3 + i, 4).value)
                wet_bulb_fittings_2to1.append(entry)
                i += 1
            i = 0
            wet_bulb_fittings_3to1 = list()
            while sheet.cell(3 + i, 5).value is not None:
                entry = WetBulbFitting_3to1()
                entry.temp = float(sheet.cell(3 + i, 5).value)
                entry.amplitude = float(sheet.cell(3 + i, 6).value)
                wet_bulb_fittings_3to1.append(entry)
                i += 1

            i = 0
            wet_bulb_fittings_4to1 = list()
            while sheet.cell(3 + i, 7).value is not None:
                entry = WetBulbFitting_4to1()
                entry.temp = float(sheet.cell(3 + i, 7).value)
                entry.amplitude = float(sheet.cell(3 + i, 8).value)
                wet_bulb_fittings_4to1.append(entry)
                i += 1

            i = 0
            wet_bulb_fittings_3to2 = list()
            while sheet.cell(3 + i, 9).value is not None:
                entry = WetBulbFitting_3to2()
                entry.temp = float(sheet.cell(3 + i, 9).value)
                entry.amplitude = float(sheet.cell(3 + i, 10).value)
                wet_bulb_fittings_3to2.append(entry)
                i += 1

            i = 0
            wet_bulb_fittings_4to3 = list()
            while sheet.cell(3 + i, 11).value is not None:
                entry = WetBulbFitting_4to3()
                entry.temp = float(sheet.cell(3 + i, 11).value)
                entry.amplitude = float(sheet.cell(3 + i, 12).value)
                wet_bulb_fittings_4to3.append(entry)
                i += 1

            i = 0
            p4_fittings = list()
            while sheet.cell(3 + i, 13).value is not None:
                entry = P4Fitting()
                entry.g = float(sheet.cell(3 + i, 13).value)
                entry.p4 = float(sheet.cell(3 + i, 14).value)
                p4_fittings.append(entry)
                i += 1

        elif sheet.title == "拟合系数表":
            # print("5")
            fitting_coefficients = FittingCoefficients()
            for i in range(12):
                val = 0.0
                if sheet.cell(3, 2 + i).value is not None:
                    val = float(sheet.cell(3, 2 + i).value)
                fitting_coefficients.b.append(val)
            for i in range(12):
                val = 0.0
                if sheet.cell(5, 2 + i).value is not None:
                    val = float(sheet.cell(3, 2 + i).value)
                fitting_coefficients.b.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(8, 2 + i).value is not None:
                    val = float(sheet.cell(8, 2 + i).value)
                fitting_coefficients.a.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(11, 2 + i).value is not None:
                    val = float(sheet.cell(11, 2 + i).value)
                fitting_coefficients.c.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(15, 2 + i).value is not None:
                    val = float(sheet.cell(15, 2 + i).value)
                fitting_coefficients.d_1to1.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(17, 2 + i).value is not None:
                    val = float(sheet.cell(17, 2 + i).value)
                fitting_coefficients.d_2to1.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(19, 2 + i).value is not None:
                    val = float(sheet.cell(19, 2 + i).value)
                fitting_coefficients.d_3to1.append(val)
            for i in range(4):
                val = 0.0
                if sheet.cell(21, 2 + i).value is not None:
                    val = float(sheet.cell(21, 2 + i).value)
                fitting_coefficients.d_4to1.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(23, 2 + i).value is not None:
                    val = float(sheet.cell(23, 2 + i).value)
                fitting_coefficients.d_3to2.append(val)
            for i in range(3):
                val = 0.0
                if sheet.cell(25, 2 + i).value is not None:
                    val = float(sheet.cell(25, 2 + i).value)
                fitting_coefficients.d_4to3.append(val)
            for i in range(4):
                val = 0.0
                if sheet.cell(27, 2 + i).value is not None:
                    val = float(sheet.cell(27, 2 + i).value)
                fitting_coefficients.e.append(val)
        # optimize_result = list()
        # elif sheet.title == "优化计算结果":
        #     # print("6")
        #     optimize_result = list()
        #     i = 0
        #     while sheet.cell(2 + i, 1).value is not None:
        #         entry = OptimizeResult()
        #         entry.year = sheet.cell(2 + i, 1).value
        #         entry.mon = sheet.cell(2 + i, 2).value
        #         entry.day = sheet.cell(2 + i, 3).value
        #         entry.hour = sheet.cell(2 + i, 4).value
        #         if sheet.cell(2 + i, 5).value is None:
        #             optimize_result.append(entry)
        #             i += 1
        #             continue
        #         entry.q = float(sheet.cell(2 + i, 5).value)
        #         entry.ts = float(sheet.cell(2 + i, 6).value)
        #         optimize_result.append(entry)
        #         i += 1
    print("load completed")
    wb.close()


def save_default(path: str):
    with open(path, "wb") as f:
        data = base64.decodebytes(bytes(template_file_base64, "utf-8"))
        f.write(data)
        f.close()


def save(path: str):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:

        if sheet.title == "参数初始值设定":
            sheet["B4"].value = str(init_params.q)
            sheet["B5"].value = str(init_params.n)
            sheet["B6"].value = str(init_params.efficiency_range)
            # sheet["C6"].value = str(init_params.efficiency_range[1])
            sheet["B7"].value = str(init_params.t3_min)
            sheet["B9"].value = str(init_params.G20)
            sheet["B14"].value = str(init_params.G30)
            sheet["B10"].value = str(init_params.h)
            sheet["B11"].value = str(init_params.p2)
            sheet["B24"].value = str(init_params.delta_t1_range[0])
            sheet["C24"].value = str(init_params.delta_t1_range[1])
            sheet["B25"].value = str(init_params.delta_t2_range[0])
            sheet["C25"].value = str(init_params.delta_t2_range[1])
            sheet["B21"].value = str(init_params.P0)
            sheet["B26"].value = str(init_params.q_min)
            # sheet["B27"].value = str(init_params.p20)
            sheet["B27"].value = str(init_params.mu)
            sheet["B28"].value = str(init_params.lamb)
            sheet["B22"].value = str(init_params.lengque_maxn)
            sheet["B29"].value = str(init_params.yuzhi)
            for i in range(9):
                sheet.cell(2, 2 + i).value = str(init_params.t1_range[i])
            # print("ini ok")
        # elif sheet.title == "主机参数拟合":
        #     # print("主机参数")
        #     i = 3
        #     for entry in main_fittings:
        #         sheet.cell(i, 1).value = str(round(float(entry.q) / float(init_params.q) * 100, 2))
        #         sheet.cell(i, 2).value = str(entry.q)
        #         sheet.cell(i, 3).value = str(entry.p1)
        #         sheet.cell(i, 4).value = str(entry.t1)
        #         sheet.cell(i, 5).value = str(entry.t2)
        #         sheet.cell(i, 6).value = str(entry.t3)
        #         sheet.cell(i, 7).value = str(entry.t4)
        #         sheet.cell(i, 8).value = str(entry.cop)
        #         i += 1
        #     while sheet.cell(i, 1).value is not None:
        #         sheet.delete_rows(i)
        # elif sheet.title == "水泵性能参数拟合":
        #     # print("水泵性能参数拟合")
        #     for i in range(5):
        #         sheet.cell(4, 3 + i * 2).value = str(pump2_fittings[i].g2)
        #         sheet.cell(4, 4 + i * 2).value = str(pump2_fittings[i].p2)
        #     for i in range(5):
        #         sheet.cell(11, 3 + i * 2).value = str(pump3_fittings[i].g3)
        #         sheet.cell(11, 4 + i * 2).value = str(pump3_fittings[i].p3)
        # elif sheet.title == "冷却塔拟合":
        #     # print("冷却塔拟合")
        #     i = 0
        #     # wet_bulb_fittings = list()
        #     for entry in wet_bulb_fittings_1to1:
        #         sheet.cell(3 + i, 1).value = str(entry.temp)
        #         sheet.cell(3 + i, 2).value = str(entry.amplitude)
        #         i += 1
        #     i = 0
        #     for entry in wet_bulb_fittings_2to1:
        #         print(i)
        #         print(entry.temp, entry.amplitude)
        #         sheet.cell(3 + i, 3).value = str(1)
        #         sheet.cell(3 + i, 4).value = str(1)
        #         i += 1
        #     i = 0
        #     for entry in wet_bulb_fittings_3to1:
        #         sheet.cell(3 + i, 5).value = str(entry.temp)
        #         sheet.cell(3 + i, 6).value = str(entry.amplitude)
        #         i += 1
        #     i = 0
        #     for entry in wet_bulb_fittings_4to1:
        #         sheet.cell(3 + i, 7).value = str(entry.temp)
        #         sheet.cell(3 + i, 8).value = str(entry.amplitude)
        #         i += 1
        #     i = 0
        #     for entry in wet_bulb_fittings_3to2:
        #         sheet.cell(3 + i, 9).value = str(entry.temp)
        #         sheet.cell(3 + i, 10).value = str(entry.amplitude)
        #         i += 1
        #     i = 0
        #     for entry in wet_bulb_fittings_4to3:
        #         sheet.cell(3 + i, 11).value = str(entry.temp)
        #         sheet.cell(3 + i, 12).value = str(entry.amplitude)
        #         i += 1
        #
        #     while sheet.cell(3 + i, 1).value is not None:
        #         sheet.cell(3 + i, 1).value = None
        #         sheet.cell(3 + i, 2).value = None
        #         i += 1
        #
        #     i = 0
        #     for entry in p4_fittings:
        #         sheet.cell(3 + i, 13).value = str(entry.g)
        #         sheet.cell(3 + i, 14).value = str(entry.p4)
        #         i += 1
        #     while sheet.cell(3 + i, 4).value is not None:
        #         sheet.cell(3 + i, 4).value = None
        #         sheet.cell(3 + i, 5).value = None
        #         i += 1
        elif sheet.title == "拟合系数表":
            # print("此时c：", fitting_coefficients.c)
            for i in range(12):
                # print(fitting_coefficients.b[i])
                sheet.cell(3, 2 + i).value = str(fitting_coefficients.b[i])
            for i in range(12):
                sheet.cell(5, 2 + i).value = str(fitting_coefficients.b[i + 12])
            for i in range(3):
                sheet.cell(8, 2 + i).value = str(fitting_coefficients.a[i])
            for i in range(3):
                sheet.cell(11, 2 + i).value = str(fitting_coefficients.c[i])
            for i in range(3):
                sheet.cell(15, 2 + i).value = str(fitting_coefficients.d_1to1[i])
            for i in range(3):
                sheet.cell(17, 2 + i).value = str(fitting_coefficients.d_2to1[i])
            for i in range(3):
                sheet.cell(19, 2 + i).value = str(fitting_coefficients.d_3to1[i])
            for i in range(4):
                sheet.cell(21, 2 + i).value = str(fitting_coefficients.d_4to1[i])
            for i in range(3):
                sheet.cell(23, 2 + i).value = str(fitting_coefficients.d_3to2[i])
            for i in range(3):
                sheet.cell(25, 2 + i).value = str(fitting_coefficients.d_4to3[i])
            for i in range(4):
                sheet.cell(27, 2 + i).value = str(fitting_coefficients.e[i])
        elif sheet.title == "优化计算结果":
            # print("优化计算结果")
            i = 0
            for entry in optimize_result:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.t1)
                sheet.cell(2 + i, 10).value = str(entry.t2)
                sheet.cell(2 + i, 11).value = str(entry.t3)
                sheet.cell(2 + i, 12).value = str(entry.t4)
                sheet.cell(2 + i, 13).value = str(entry.delta_t)
                sheet.cell(2 + i, 14).value = str(entry.p1)
                sheet.cell(2 + i, 15).value = str(entry.p2)
                sheet.cell(2 + i, 16).value = str(entry.p3)
                sheet.cell(2 + i, 17).value = str(entry.p4)
                sheet.cell(2 + i, 18).value = str(entry.p)
                sheet.cell(2 + i, 19).value = str(entry.cop)
                sheet.cell(2 + i, 20).value = str(entry.n)
                i += 1
            while sheet.cell(2 + i, 1).value is not None:
                for j in range(1, 17):
                    sheet.cell(2 + i, j).value = None
                i += 1

    # print("----")
    wb.save(path)
    wb.close()


def db_save_showAll(path: str, records):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:
        if sheet.title == "全显示":
            # print("优化计算结果")
            i = 0
            for entry in records:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.system_load_percentage)

                sheet.cell(2 + i, 10).value = str(entry.t1)
                sheet.cell(2 + i, 11).value = str(entry.t2)
                sheet.cell(2 + i, 12).value = str(entry.G2_lendong)
                sheet.cell(2 + i, 13).value = str(entry.fluency_lendong)

                sheet.cell(2 + i, 14).value = str(entry.t3)
                sheet.cell(2 + i, 15).value = str(entry.t4)
                sheet.cell(2 + i, 16).value = str(entry.G3_lenque)
                sheet.cell(2 + i, 17).value = str(entry.fluency_lenque)

                sheet.cell(2 + i, 18).value = str(entry.delta_t)
                sheet.cell(2 + i, 19).value = str(entry.p1)
                sheet.cell(2 + i, 20).value = str(entry.p2)
                sheet.cell(2 + i, 21).value = str(entry.p3)
                sheet.cell(2 + i, 22).value = str(entry.p4)
                sheet.cell(2 + i, 23).value = str(entry.p)
                sheet.cell(2 + i, 24).value = str(entry.cop)
                sheet.cell(2 + i, 25).value = str(entry.n)
                i += 1

            while sheet.cell(2 + i, 1).value is not None:
                print("is", 2 + i)
                for j in range(1, 25):
                    sheet.cell(2 + i, j).value = None
                i += 1
            break

    # print("----")

    wb.save(path)
    wb.close()


def db_save_temperature(path: str, records):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:
        if sheet.title == "温度":
            # print("优化计算结果")
            i = 0
            for entry in records:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.system_load_percentage)
                sheet.cell(2 + i, 10).value = str(entry.t1)
                sheet.cell(2 + i, 11).value = str(entry.t2)
                sheet.cell(2 + i, 12).value = str(entry.t3)
                sheet.cell(2 + i, 13).value = str(entry.t4)
                sheet.cell(2 + i, 14).value = str(entry.t2 - entry.t1)
                sheet.cell(2 + i, 13).value = str(entry.t4 - entry.t3)

                i += 1
            while sheet.cell(2 + i, 1).value is not None:
                for j in range(1, 25):
                    sheet.cell(2 + i, j).value = None
                i += 1
            break

    # print("----")

    wb.save(path)
    wb.close()


def db_save_Pump(path: str, records):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:
        if sheet.title == "功率":
            # print("优化计算结果")
            i = 0
            for entry in records:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.system_load_percentage)

                sheet.cell(2 + i, 10).value = str(entry.p1)
                sheet.cell(2 + i, 11).value = str(entry.p2)
                sheet.cell(2 + i, 12).value = str(entry.p3)
                sheet.cell(2 + i, 13).value = str(entry.p4)
                sheet.cell(2 + i, 14).value = str(entry.p)

                i += 1
            while sheet.cell(2 + i, 1).value is not None:
                for j in range(1, 25):
                    sheet.cell(2 + i, j).value = None
                i += 1
            break

    # print("----")

    wb.save(path)
    wb.close()


def db_save_cop(path: str, records):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:
        if sheet.title == "cop":
            # print("优化计算结果")
            i = 0
            for entry in records:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.system_load_percentage)
                Q = entry.q
                p1 = entry.p1
                pump_cop = round(Q / p1, 3)
                sheet.cell(2 + i, 10).value = str(pump_cop)
                sheet.cell(2 + i, 11).value = str(entry.cop)

                i += 1
            while sheet.cell(2 + i, 1).value is not None:
                for j in range(1, 25):
                    sheet.cell(2 + i, j).value = None
                i += 1
            break

    # print("----")

    wb.save(path)
    wb.close()


def db_save_lengqueta(path: str, records):
    if not os.path.exists(path):
        save_default(path)
    wb = openpyxl.load_workbook(path, read_only=False)
    for sheet in wb:
        if sheet.title == "冷却塔":
            # print("优化计算结果")
            i = 0
            for entry in records:
                sheet.cell(2 + i, 1).value = entry.year
                sheet.cell(2 + i, 2).value = entry.mon
                sheet.cell(2 + i, 3).value = entry.day
                sheet.cell(2 + i, 4).value = entry.hour
                sheet.cell(2 + i, 5).value = str(entry.q)
                sheet.cell(2 + i, 6).value = str(entry.ts)
                sheet.cell(2 + i, 8).value = str(entry.load_percentage)
                sheet.cell(2 + i, 9).value = str(entry.system_load_percentage)

                sheet.cell(2 + i, 10).value = str(entry.t4)
                sheet.cell(2 + i, 11).value = str(entry.t3)
                sheet.cell(2 + i, 12).value = str(entry.delta_t)
                sheet.cell(2 + i, 13).value = str(entry.t4 - entry.t3)
                i += 1
            while sheet.cell(2 + i, 1).value is not None:
                for j in range(1, 25):
                    sheet.cell(2 + i, j).value = None
                i += 1
            break

    # print("----")

    wb.save(path)
    wb.close()


"""
Test
if __name__ == '__main__':
    fitting_coefficients.b = [float(x) for x in range(24)]
    fitting_coefficients.a = [0.0, 1.0, 2.0]
    fitting_coefficients.c = [0.0, 1.0, 2.0]
    fitting_coefficients.d = [0.0, 1.0, 2.0]
    fitting_coefficients.e = [0.0, 1.0, 2.0, 3.0]
    for i in range(10):
        main_fittings.append(MainFitting())
    for i in range(5):
        pump2_fittings.append(Pump2Fitting())
        pump3_fittings.append(Pump3Fitting())
    for i in range(2):
        wet_bulb_fittings.append(WetBulbFitting())
    p4_fittings.append(P4Fitting())
    entry = OptimizeResult()
    entry.Q = 1145.0
    entry.ts = 233.0
    optimize_result.append(entry)
    save("testtest.xlsx")
"""
