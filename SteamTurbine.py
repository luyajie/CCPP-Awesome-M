#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iapws import IAPWS97
import configparser
import os


def hpt_output(p_in, t_in, p_exh, t_exh, flow):
    # 计算高压缸做功"
    ms = IAPWS97(P=p_in, T=t_in)
    hps_exh = IAPWS97(P=p_exh, T=t_exh)
    hpt_power = (ms.h - hps_exh.h) * flow / 1000 * 0.98  # MW
    return hpt_power


def ipt_output(p_in, t_in, p_exh, t_exh, flow):
    # 计算中压缸做功"
    rhs = IAPWS97(P=p_in, T=t_in)
    ips_exh = IAPWS97(P=p_exh, T=t_exh)
    ipt_power = (rhs.h - ips_exh.h) * flow / 1000 * 0.98  # MW
    return ipt_power


def turbine_output(p_in, t_in, p_exh, t_exh, flow):
    """

    :param p_in:
    :param t_in:
    :param p_exh:
    :param t_exh:
    :param flow:
    :return:
    """
    stm_in = IAPWS97(P=p_in, T=t_in+273.15)
    stm_exh = IAPWS97(P=p_exh, T=t_exh+273.15)
    turb_power = (stm_in.h - stm_exh.h) * flow / 1000
    print("焓值%.2f %.2f"%(stm_in.h,stm_exh.h))
    return turb_power


def gasflow_by_power(mw):
    # 根据给定燃机负荷，计算燃气消耗量Nm3/hrs
    gas = 0.1405 * mw ^ 2 * 149.07 * mw + 21496
    return gas


def cond_ttd(t,pc):
    """
    :summary: 凝汽器端差:汽轮机背压下饱和温度与凝汽器出口循环水温度的差值.
    :param t: 凝汽器出口循环水温度,DegC.
    :param pc: 汽轮机背压,MPa.a
    :return: 凝汽器端差
    """
    ttd = IAPWS97(P = pc, x=1).T - t
    return ttd

def cond_wtr_sc(pc, tc):
    """
    :summary: 凝结水过冷度:汽轮机背压下饱和温度与凝汽器热井水温度的差值.
    :param pc: 凝汽器背压.(kPa.a)
    :param tc: 凝汽器热井水温度.(DefC)
    :return:
    """
    deltaT = IAPWS97(P=pc, x=1).T - tc
    return deltaT


if __name__ == '__main__':
    CONFIGFILE = "RunTimeEnv"
    conf = configparser.ConfigParser()
    conf.read(CONFIGFILE)

    p_ms = float(conf.get("steamturbine", "p_ms"))  # 主蒸汽压力 MPa
    t_ms = float(conf.get("steamturbine", "t_ms")) + 273.15  # 主蒸汽温度 DegC
    q_ms = float(conf.get("steamturbine", "q_ms")) / 3.6  # 主蒸汽流量 kg/s

    p_hpt_exh = float(conf.get("steamturbine", "p_hpt_exh"))  # 高压缸排汽压力 MPa
    t_hpt_exh = float(conf.get("steamturbine", "t_hpt_exh")) + 273.15  # 高压缸排汽温度 DegC

    p_rhs = float(conf.get("steamturbine", "p_rhs"))  # 热再热蒸汽压力 MPa
    t_rhs = float(conf.get("steamturbine", "t_rhs")) + 273.15  # 热再热蒸汽温度 DegC
    q_rhs = float(conf.get("steamturbine", "q_rhs")) / 3.6  # 热再热蒸汽流量 kg/s

    p_ipt_exh = float(conf.get("steamturbine", "p_ipt_exh"))  # 中压缸排汽压力 MPa
    t_ipt_exh = float(conf.get("steamturbine", "t_ipt_exh")) + 273.15  # 中压缸排汽温度 DegC

    power_hpt = hpt_output(p_ms, t_ms, p_hpt_exh, t_hpt_exh, q_ms)
    power_ipt = ipt_output(p_rhs, t_rhs, p_ipt_exh, t_ipt_exh, q_rhs)
    print("高压缸发电量：%.3f MW" % (power_hpt))
    print("中压缸发电量：%.3f MW" % (power_ipt))
    print("高中压缸发电量：%.3f MW" % (power_ipt + power_hpt))
    # os.system("pause")
    input("按回车键继续...")
