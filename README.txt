2026网页改编版
原作: Jeffrey S. Rosenthal and Gareth O. Roberts, March 2022
https://probability.ca/fdraw/drawnew.html
https://probability.ca/fdraw/drawnew.js

original/ 保留原始HTML与JavaScript快照。
draw2026.js 改编原随机候选分配与合法性筛选结构，支持12组、3东道主及完整2026约束。
engine.js 为新增Skip引擎，使用完整可行性搜索，不是Gurobi实现。
gurobi_simulator.py 为另外编写的整数规划实现，需Gurobi及许可证，未在本环境运行验证。

运行网页: 解压后在目录执行 python -m http.server 8000，然后访问 http://localhost:8000。
不能仅双击HTML运行Worker。
网页新增公开Skip、真实顺序重放、均匀拒绝采样及均匀初始化后交换。原多球法未移植。
数据来源: 用户提供的2026研究数据包，保留抽签时占位符。

批量入口lab.html现使用与首页相同Canvas与2026引擎，支持公开Skip或均匀拒绝采样、样本切换和带mechanism的CSV。

首页为唯一模拟器页面；旧lab.html自动跳转首页。次数设1即可单次模拟。

批量上限10001；超过100次时，仅首个样本保留逐组检查明细，其余保留抽出对象与落位序列，完整分组CSV不受影响。

视觉升级：莫兰迪配色与按钮样式；过程观察器显示当前球队、候选组局部冲突／未来死局／接受状态。未保存的检查不推断其可行性。算法与采样规则未改变。
