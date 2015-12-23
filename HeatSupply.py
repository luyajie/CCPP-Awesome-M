# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#########################
计算热网系统供热量计算模块
#########################
"""
print(__doc__)
from iapws import IAPWS97
import CONST
from SteamTurbine import turbine_output

def heat_trans(p_in, t_in, p_out, t_out, med_flux):
    """

    :param p_rtn_wtr: 回水压力 MPa
    :param t_rtn_wtr: 回水温度 DegC
    :param p_sup_wtr: 供水压力 MPa
    :param t_sup_wtr: 供水温度 DegC
    :param wtr_flux: 供水流量 t/h
    :return:heat_load: 供热负荷 GJ
    """

    med_in = IAPWS97(P=p_in, T=t_in + 273.15)
    med_out = IAPWS97(P=p_out, T=t_out + 273.15)
    heat_load = (med_in.h - med_out.h) * med_flux / 1000
    return heat_load


def min_power_by_heat(heat_load):
    """
    给定机组供热量（GJ），求机组最低运行负荷。
    根据供热量，得出热网抽汽流量，热网抽汽流量减去低压补汽量即为再热蒸汽流量。根据再热蒸汽量计算高中压缸功率
    :param heat_load: GJ
    :return:
    """
    p_ext = 0.3
    t_ext = 250 + 273.15
    p_drn = 0.2
    t_drn = 55 + 273.15
    flux_lp = 30

    stm_ext = IAPWS97(P=p_ext, T=t_ext)
    wtr_drn = IAPWS97(P=p_drn, T=t_drn)
    stm_ext_flux = heat_load * 1000 / (stm_ext.h - wtr_drn.h)  # 热网抽汽流量 t/h
    print("热网抽汽流量:%.2f t/h"%(stm_ext_flux))
    min_flux_lpt = 100

    stm_lpt_in = IAPWS97(P=0.6, T=300+273.15)
    stm_lpt_exh = IAPWS97(P=0.005, x=0.921)
    rhs_flux = (stm_ext_flux + min_flux_lpt-flux_lp) / 3.6 # kg/s
    print(rhs_flux)
    """
    计算高压缸、中压缸、低压缸负荷
    """
    lpt_load = min_flux_lpt * (stm_lpt_in.h-stm_lpt_exh.h) / 1000
    ipt_load = turbine_output(3,540,0.5,300,rhs_flux)
    hpt_load = turbine_output(12,545,3.4,359,rhs_flux-12)

    if rhs_flux > 315:  # 判断是否需要二拖一
        gt_load = 0.0076 * rhs_flux/2 * rhs_flux/2 -2.2675 * rhs_flux/2 + 272.03
    else:
        gt_load = 0.0076 * rhs_flux * rhs_flux -2.2675 * rhs_flux + 272.03

    print("高中低压缸功率为%.2f %.2f %.2f"%(hpt_load,ipt_load,lpt_load))
    plant_power = gt_load*2+hpt_load+ipt_load+lpt_load
    return (plant_power,gt_load)


def max_power_by_heat(heat_load):
    """

    :param heat_load:
    :return:plant_power(机组总负荷,低压缸负荷)
    """
    p_ext = 0.3
    t_ext = 250 + 273.15
    p_drn = 0.2
    t_drn = 55 + 273.15
    flux_lp = 40

    stm_ext = IAPWS97(P=p_ext, T=t_ext)
    wtr_drn = IAPWS97(P=p_drn, T=t_drn)
    stm_ext_flux = heat_load * 1000 / (stm_ext.h - wtr_drn.h)  # 热网抽汽流量 t/h
    lpt_flux = CONST.RHS_FLUX_RATING+CONST.LS_FLUX_RATING-stm_ext_flux
    stm_lpt_in = IAPWS97(P=0.6, T=300+273.15)
    stm_lpt_exh = IAPWS97(P=0.005, x=0.921)
    lpt_power = lpt_flux * (stm_lpt_in.h-stm_lpt_exh.h) / 1000 / 3.6
    global_power = CONST.COUPLING_POWER_RATING+CONST.HPT_POWER_RATING + CONST.IPT_POWER_RATING+lpt_power
    plant_power = (global_power,lpt_power)
    return plant_power



if __name__ == '__main__':
    print(min_power_by_heat(1500))
    print("%.3f" % max_power_by_heat(1500)[0])


