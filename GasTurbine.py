#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Awesome
# Date: 2015-12-22
from iapws import IAPWS97


def air_enthalpy(t, rh):
    """

    :param t: 空气温度 ℃
    :param rh: 相对湿度 %
    :return: 空气焓值 [kJ/kg干]
    """
    p_sat_stm = IAPWS97(T=t + 273.15, x=1).P * 1000000  # t温度下饱和压力 Pa
    p_stm = rh * p_sat_stm
    print(p_stm)
    x = (0.622 * p_stm) / (101325 - p_stm)
    h_air = 1.005 * t + x * (2500 + 1.84 * t)
    return h_air


def eff_comp(p_in, t_in, p_out, t_out):
    """
    计算燃机压气机效率
    :param p_in: 入口压力
    :param t_in: 入口温度 K
    :param p_out:出口压力
    :param t_out: 出口温度 K
    :return:
    """
    t_out_s = pow(p_out / p_in, 0.2871) * t_in + 273.15
    print(t_out_s)
    eff_comp = (t_out_s - t_in + 273.15) / (t_out - t_in + 273.15)
    return eff_comp


def eff_gt_rating(mw):
    """ 燃气轮机ISO各工况效率拟合公式

    Arguments:
        mw {[float]} -- 燃机负荷 单位：MW
    """
    eff_gt = -3.456e-6 * mw * mw + 0.002 * mw + 0.1102
    return eff_gt


def ms_hrsg_rating(mw):
    """主汽流量与燃机负荷
    
    已知燃机负荷，求主蒸汽流量。
    
    Arguments:
        mw {[float]} -- 燃机负荷，单位：MW
    """
    pass


def eff_gt(t, p, rh):
    """[计算燃机效率]

    [description]

    Arguments:
        t {[type]} -- [description]
        p {[type]} -- [description]
        rh {[type]} -- [description]
    """
    pass

if __name__ == '__main__':
    test = eff_gt_rating(150)
    print(test)
    ah = air_enthalpy(20, 0.5)
