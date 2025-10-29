## 笔记

- well_import.ipynb：尝试用lasio库导入Petrel导出的测井曲线
    - 输入：*.las

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

- well_log_truncate.ipynb：尝试对目的层曲线进行截断（这个方法只对直井有效）
    - 输入：vertical_well_common_las/*.las，sand_group_thickness_complete.xlsx
    - 输出：vertical_well_truncated_las/*.las

- well_log_preprocess.ipynb：（TODO）尝试剔除测井曲线的一些异常值
    - 输入：vertical_well_truncated_las/*.las
    - 输出：
- well_visualize.ipynb：尝试可视化测井曲线以及解释层位
    -
- well_correlation_analysis.ipynb：（TODO）尝试分析各个测井属性的相关性，热力图&散点图
- cali_check.ipynb：尝试通过众数或者直方图检查钻头的基础尺寸

## 工具函数
