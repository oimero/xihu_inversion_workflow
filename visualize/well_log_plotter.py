"""
测井曲线可视化工具模块

提供测井曲线绘图和层位标注的通用函数。
"""

import os
from typing import Optional

import lasio
import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体支持
plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


# 内置曲线样式字典
DEFAULT_CURVE_STYLES = {
    "GR": {"color": "green", "range": (0, 150), "label": "GR (gAPI)"},
    "GAMMA": {"color": "green", "range": (0, 150), "label": "GAMMA (gAPI)"},
    "DT": {"color": "blue", "range": (40, 240), "label": "DT (us/ft)"},
    "AC": {"color": "blue", "range": (40, 240), "label": "AC (us/ft)"},
    "DEN": {"color": "red", "range": (1.95, 2.95), "label": "DEN (g/cm3)"},
    "RHOB": {"color": "red", "range": (1.95, 2.95), "label": "RHOB (g/cm3)"},
    "NPHI": {"color": "cyan", "range": (-0.05, 0.45), "label": "NPHI (v/v)"},
    "SP": {"color": "orange", "range": (-150, 50), "label": "SP (mV)"},
    "CN": {"color": "cyan", "range": (0, 0.45), "label": "CN (v/v)"},
    "LLD": {"color": "purple", "range": (0.2, 2000), "label": "LLD (ohm.m)", "log": True},
    "LLD1": {"color": "purple", "range": (0.2, 2000), "label": "LLD1 (ohm.m)", "log": True},
    "RT": {"color": "magenta", "range": (0.2, 2000), "label": "RT (ohm.m)", "log": True},
    "CAL": {"color": "brown", "range": (6, 20), "label": "CAL (in)"},
    "CALI": {"color": "brown", "range": (6, 20), "label": "CALI (in)"},
    "INPEFA": {"color": "black", "range": (-2, 2), "label": "INPEFA"},
    "POR": {"color": "teal", "range": (0, 0.4), "label": "POR (v/v)"},
    "SW": {"color": "blue", "range": (0, 1), "label": "SW (v/v)"},
    "VSH": {"color": "olive", "range": (0, 1), "label": "VSH (v/v)"},
}


def plot_well_log(
    well_name: str,
    las_file_path: str,
    curves_to_plot: list[str],
    horizon_df: Optional[pd.DataFrame] = None,
    output_dir: str = "output",
    depth_padding: int = 20,
    save_plot: bool = True,
    show_plot: bool = False,
    fig_height: int = 30,
    track_width: int = 3,
) -> Optional[tuple]:
    """
    绘制单井的测井曲线综合图，并可选地标注地质层位。

    参数:
    - well_name (str): 要绘制的井名,用于命名输出文件。
    - las_file_path (str): 对应井的 LAS 文件路径。
    - curves_to_plot (list[str]): 希望绘制的曲线名称列表 (例如 ['GR', 'DT', 'DEN'])。
    - horizon_df (pd.DataFrame | None): 包含所有井层位信息的 DataFrame。
                                        应包含 'Well', 'MD', 'Surface' 等列。
                                        如果为 None,则不绘制层位。默认为 None。
    - output_dir (str): 保存图像的目录。默认为 "output"。
    - depth_padding (int): 在最浅和最深层位上下额外显示的深度范围(单位:米)。默认为 10。
    - save_plot (bool): 是否保存图像文件。默认为 True。
    - show_plot (bool): 是否在运行时显示图像。默认为 False。
    - fig_height (int): 图像高度(英寸)。默认为 30。
    - track_width (int): 每个道的宽度(英寸)。默认为 3。

    返回:
    - tuple | None: 如果成功绘图,返回 (fig, axes),否则返回 None。
    """

    # ============ 1. 读取 LAS 文件 ============
    try:
        las = lasio.read(las_file_path)
        print(f"✓ 成功读取 LAS 文件: {las_file_path}")
        print(f"  深度范围: {las.index[0]:.2f} - {las.index[-1]:.2f} m")
    except Exception as e:
        print(f"✗ 读取 LAS 文件失败: {e}")
        return None

    # ============ 2. 处理层位数据(可选) ============
    well_horizons = None
    if horizon_df is not None:
        well_horizons = horizon_df[horizon_df["Well"] == well_name].copy()
        if len(well_horizons) > 0:
            well_horizons = well_horizons.sort_values("MD").reset_index(drop=True)
            print(f"✓ 找到 {len(well_horizons)} 个层位")
        else:
            print(f"⚠ 未在层位数据中找到井 '{well_name}' 的数据")
            well_horizons = None

    # ============ 3. 筛选可用曲线 ============
    available_curves = {}
    for curve_name in curves_to_plot:
        if curve_name in las.keys():
            if curve_name in DEFAULT_CURVE_STYLES:
                available_curves[curve_name] = DEFAULT_CURVE_STYLES[curve_name]
            else:
                # 如果曲线存在但没有预设样式,使用默认样式
                available_curves[curve_name] = {
                    "color": "black",
                    "range": (None, None),
                    "label": curve_name,
                }
                print(f"⚠ 曲线 '{curve_name}' 使用默认样式")
        else:
            print(f"⚠ 曲线 '{curve_name}' 不存在于 LAS 文件中")

    if not available_curves:
        print("✗ 没有可绘制的曲线")
        return None

    print(f"✓ 将绘制的曲线: {list(available_curves.keys())}")

    # ============ 4. 确定绘图深度范围 ============
    if well_horizons is not None and len(well_horizons) > 0:
        min_depth = well_horizons["MD"].min() - depth_padding
        max_depth = well_horizons["MD"].max() + depth_padding
        print(f"✓ 使用层位深度范围: {min_depth:.2f} - {max_depth:.2f} m")
    else:
        min_depth = las.index[0]
        max_depth = las.index[-1]
        print(f"✓ 使用完整深度范围: {min_depth:.2f} - {max_depth:.2f} m")

    # ============ 5. 创建图形 ============
    n_tracks = len(available_curves)
    fig, axes = plt.subplots(1, n_tracks, figsize=(track_width * n_tracks, fig_height), sharey=True)

    # 确保 axes 是列表
    if n_tracks == 1:
        axes = [axes]

    # ============ 6. 绘制曲线 ============
    depth = las.index
    mask = (depth >= min_depth) & (depth <= max_depth)
    plot_depth = depth[mask]

    for idx, (curve_name, props) in enumerate(available_curves.items()):
        ax = axes[idx]

        # 获取曲线数据
        curve_data = las[curve_name][mask]

        # 绘制曲线
        if props.get("log", False):
            ax.semilogx(curve_data, plot_depth, color=props["color"], linewidth=0.8)
        else:
            ax.plot(curve_data, plot_depth, color=props["color"], linewidth=0.8)

        # 设置坐标轴
        ax.set_ylim(max_depth, min_depth)  # 深度从上到下
        if props["range"][0] is not None:
            ax.set_xlim(props["range"])
        ax.set_xlabel(props["label"], fontsize=10)
        ax.grid(True, alpha=0.3, linestyle="--")

        # 只在第一个道显示深度标签
        if idx == 0:
            ax.set_ylabel("深度 (m)", fontsize=12, fontweight="bold")

        # ============ 7. 标注层位(可选) ============
        if well_horizons is not None:
            for _, horizon in well_horizons.iterrows():
                horizon_depth = horizon["MD"]
                surface_name = horizon["Surface"]

                # 如果在绘图范围内
                if min_depth <= horizon_depth <= max_depth:
                    # 绘制层位线
                    ax.axhline(
                        y=horizon_depth,
                        color="black",
                        linewidth=1.5,
                        linestyle="--",
                        alpha=0.7,
                        zorder=10,
                    )

                    # 在第一个道添加层位名称标注
                    if idx == 0:
                        # 获取 x 位置(考虑可能没有设置范围的情况)
                        xlim = ax.get_xlim()
                        x_pos = xlim[0] + (xlim[1] - xlim[0]) * 0.02
                        ax.text(
                            x_pos,
                            horizon_depth + 2,
                            f"{surface_name}",
                            verticalalignment="center",
                            fontsize=8,
                        )

    plt.tight_layout()

    # ============ 8. 保存图像 ============
    if save_plot:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{well_name}_well_log.png")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"✓ 图像已保存到: {output_file}")

    # ============ 9. 显示图像 ============
    if show_plot:
        plt.show()
    else:
        plt.close()

    return fig, axes
