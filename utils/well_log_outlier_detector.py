"""
测井曲线异常值检测模块

提供基于先验规则、3σ法则和IQR方法的异常值检测功能
"""

from typing import Optional

import lasio
import numpy as np

# 定义异常值规则
ANOMALY_RULES = {
    "GR": {"min": 0, "max": None, "description": "GR不能为负值(物理意义)"},
    "DEN": {"min": 1.0, "max": 3.0, "description": "密度小于1.0表示井眼扩径或钻井液,大于3.0不合理"},
    "RHOB": {"min": 1.0, "max": 3.0, "description": "密度小于1.0表示井眼扩径或钻井液,大于3.0不合理"},
    "DT": {"min": 40, "max": 200, "description": "小于40为跳周现象,大于200表示极疏松地层或异常"},
    "AC": {"min": 40, "max": 200, "description": "小于40为跳周现象,大于200表示极疏松地层或异常"},
    "CAL": {"min": 8.5, "max": 16.0, "description": "井径不应小于钻头尺寸,远大于钻头尺寸表示严重扩径"},
    "CALI": {"min": 8.5, "max": 16.0, "description": "井径不应小于钻头尺寸,远大于钻头尺寸表示严重扩径"},
    "LLD": {"min": 0.1, "max": 2000, "description": "极低值表示仪器短路,极高值需要截断"},
    "LLD1": {"min": 0.1, "max": 2000, "description": "极低值表示仪器短路,极高值需要截断"},
    "POR": {"min": 0.1, "max": 1.0, "description": "0.1的孔隙度是一个默认值，可以去除小于等于该值的数据"},
}


def detect_anomalies(data: np.ndarray, min_val: Optional[float] = None, max_val: Optional[float] = None) -> np.ndarray:
    """
    检测异常值(基于先验规则)

    Parameters:
    -----------
    data : np.ndarray
        测井数据
    min_val : float, optional
        最小合理值
    max_val : float, optional
        最大合理值

    Returns:
    --------
    mask : np.ndarray
        异常值掩码(True表示异常)
    """
    mask = np.zeros(len(data), dtype=bool)

    # 检测NaN
    mask |= np.isnan(data)

    # 检测无穷大
    mask |= np.isinf(data)

    # 检测超出范围的值
    if min_val is not None:
        mask |= data <= min_val

    if max_val is not None:
        mask |= data >= max_val

    return mask


def apply_statistical_filter_3sigma(data: np.ndarray, sigma: float = 3.0, verbose: bool = True) -> np.ndarray:
    """
    应用3σ法则检测离群点

    Parameters:
    -----------
    data : np.ndarray
        测井数据
    sigma : float, default=3.0
        标准差倍数
    verbose : bool, default=True
        是否打印统计信息

    Returns:
    --------
    mask : np.ndarray
        离群点掩码(True表示离群)
    """
    # 排除NaN和Inf
    valid_data = data[~np.isnan(data) & ~np.isinf(data)]

    if len(valid_data) == 0:
        return np.zeros(len(data), dtype=bool)

    mean = np.mean(valid_data)
    std = np.std(valid_data)

    if verbose:
        print(f"  [3σ法则] 均值: {mean:.2f}, 标准差: {std:.2f}")

    mask = np.abs(data - mean) > (sigma * std)

    return mask


def apply_statistical_filter_iqr(data: np.ndarray, multiplier: float = 1.5, verbose: bool = True) -> np.ndarray:
    """
    应用IQR(四分位距)方法检测离群点

    适用于偏态分布数据,比3σ法则更稳健

    Parameters:
    -----------
    data : np.ndarray
        测井数据
    multiplier : float, default=1.5
        IQR倍数,常用值为1.5(温和离群点)或3.0(极端离群点)
    verbose : bool, default=True
        是否打印统计信息

    Returns:
    --------
    mask : np.ndarray
        离群点掩码(True表示离群)
    """
    # 排除NaN和Inf
    valid_data = data[~np.isnan(data) & ~np.isinf(data)]

    if len(valid_data) == 0:
        return np.zeros(len(data), dtype=bool)

    # 计算四分位数
    q1 = np.percentile(valid_data, 25)
    q3 = np.percentile(valid_data, 75)
    iqr = q3 - q1

    # 计算离群点边界
    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    if verbose:
        print(f"  [IQR方法] Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}")
        print(f"  [IQR方法] 边界: [{lower_bound:.2f}, {upper_bound:.2f}]")

    # 标记离群点
    mask = (data < lower_bound) | (data > upper_bound)

    return mask


# def get_curve_mnemonic(las: lasio.LASFile, possible_names: list) -> Optional[str]:
#     """
#     根据可能的名称列表查找曲线

#     Parameters:
#     -----------
#     las : lasio.LASFile
#         LAS文件对象
#     possible_names : list
#         可能的曲线名称列表

#     Returns:
#     --------
#     mnemonic : str or None
#         找到的曲线名称
#     """
#     curve_mnemonics = [c.mnemonic for c in las.curves]

#     for name in possible_names:
#         if name in curve_mnemonics:
#             return name

#     return None
