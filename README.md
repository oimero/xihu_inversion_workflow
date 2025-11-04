## 笔记

![](data\diagrams\Used Well.bmp)

---

### Week1

- well_import.ipynb：尝试用 lasio 库导入 Petrel 导出的测井曲线
    - 输入：*.las

- well_visualize.ipynb：尝试可视化测井曲线以及解释层位

- well_horizon_preprocess.ipynb：尝试删除一些明显异常的（或者不想要的）井或层位
    - 输入：well_horizon.xlsx
    - 输出：well_horizon_processed.xlsx

- well_find_common_logs.ipynb：尝试查看井有哪些共同曲线
    - 输入：vertical_well_las/*.las

- well_extract_common_logs.ipynb：尝试提取井的共同曲线
    - 输入：vertical_well_las/*.las
    - 输出：vertical_well_common_las/*.las

- sand_group_thickness：尝试获得砂组级层位砂厚的统计信息
    - 输入：well_horizon_processed.xlsx
    - 输出：sand_group_thickness_complete.xlsx（砂组级层位砂厚的统计信息）

- well_log_truncate.ipynb：尝试截断到目的层曲线
    - 输入：vertical_well_common_las/*.las，sand_group_thickness_complete.xlsx
    - 输出：vertical_well_truncated_las/*.las

- cali_check.ipynb：尝试通过众数或者直方图检查钻头的基础尺寸 → 12.25 in

- well_log_delete_outliers.ipynb：尝试剔除测井曲线的一些异常值
    - 输入：vertical_well_truncated_las/*.las
    - 输出：vertical_well_las_delete_outliers/*.las

---

### Week2

- well_log_delete_outliers_by_layers.ipynb：尝试分层剔除测井曲线的一些异常值
    - 输入：vertical_well_truncated_las/*.las
    - 输出：vertical_well_las_delete_outliers_by_layers/*.las

- well_visualize_test.ipynb：测试可视化测井曲线以及解释层位的函数，并集中可视化

- well_log_baseline_correction：（SUSPEND）尝试对测井曲线做基线校正
    - 问题1：需要做吗？→ 一般对 SP 曲线做基线校正，暂时用不着 SP

![](data\diagrams\baseline_shift.png)

- well_correlation_analysis.ipynb：（TODO）分层位分析测井曲线之间的相关性，热力图&交会图
    - 问题1：部分井缺层位？→ 将解释层位更换到了5月23日提供的版本，现在不缺了

- seismic_import.ipynb：试着用 pyzgy 库导入地震数据
    - 输入：obn-yuan.zgy

- forward_correlation_analysis.ipynb：（TODO）卷积正演，然后分析正演波形与井旁道地震波形的相关性
    - 问题1：要把井转换到时间域。但是，构建速度模型时，怎么知道井的**第一个**解释层位要对到地震上的哪个时间采样点？
    - 前提1：别忘了对波阻抗做地震频带的带通
    - 问题2：怎么获得用于卷积的小波？

- borehole_correction：（TODO）根据测井曲线之间的相关性，对扩径段DT和DEN进行拟合


## 工具函数

### Week1

- well_log_plotter.py：可视化测井曲线以及解释层位

### Week2

- well_log_outlier_detector.py: 剔除测井曲线的先验异常值和统计异常值
