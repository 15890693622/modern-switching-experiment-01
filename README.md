# 实验一 电路交换与分组交换的资源利用率比较

本实验用相同业务输入和链路容量，比较固定时隙电路交换与共享FIFO分组交换。你需要解释效率和时延如何随业务变化，并用测试检查AI生成的实现。实验成果将用于期末数字程控交换机的时隙、资源与性能观察模块。

参考课堂时长120分钟。先完成三个TODO，再生成图表和报告。首次环境配置尽量课前完成。90分钟课堂将自拟反例和报告安排到课后。

## 1 学习目标

理解固定资源预留、统计复用、包头开销、队列和尾丢弃。区分有效载荷利用率与线路忙碌率。比较连续、错峰突发、同步突发和轻载随机四类业务，不能预设某一种方式总是更优。

## 2 快速开始

使用Python 3.10或更高版本。教师验证使用Python 3.12，建议学生保持相同大版本。

```bash
python -m venv .venv
# Windows PowerShell若不允许激活，可直接使用.venv/Scripts/python.exe执行后续命令
python -m pip install -r requirements.txt
python src/test_environment.py
python -m pytest grading/test_framework.py -q
```

上面四个教师框架测试应通过。此时三个TODO仍未实现，核心功能测试失败和运行提示NotImplementedError是正常起点。

## 3 仿真规则

| 项目 | 约定 |
|---|---|
| 用户 | 4名，编号0～3 |
| 时钟 | 256个tick，每tick 1 ms |
| 链路 | 每tick最多128 bit，即128 kbit/s |
| 电路模型 | tick % users决定本时隙服务用户；其他用户不能借用空时隙 |
| 分组模型 | 共享FIFO；每记录增加32 bit包头；可以跨tick续传 |
| 缓存 | 两模型均为4096 bit有效载荷预留空间，含在传记录 |
| 准入 | 到达先于发送；按输入顺序；放不下时整条记录尾丢弃 |
| 完成 | 在tick结束时计完整记录送达，时延为完成边界减生成时刻 |
| 观察 | 仅[0,256)窗口，不追加排空时间；未完成记录计积压，不算丢包 |

缓存按未完成记录的原始payload大小预留，记录完整交付才释放。分组包头增加线路开销，不增加本实验定义的payload缓存配额。这样可让两模型采用同一种明确的缓存准入规则；它不是对真实设备存储器的精确建模。

本实验比较预先建立的单链路承载模型，忽略建链、传播、重传、路由与多跳时延。线路不存在额外误码。这里不仿真真实实时系统。

## 4 三个必做函数

| 文件 | 函数 | 任务 |
|---|---|---|
| src/part1_circuit.py | serve_circuit | 只服务本时隙用户，FIFO扣减发送预算 |
| src/part2_packet.py | serve_packet | 服务共享队首，计入包头，正确跨tick续传 |
| src/metrics.py | summarize | 利用率、时延、丢失、积压与守恒检查 |

框架已提供数据生成、缓存准入、循环时钟、PCM装帧和绘图，不必重新编写。不要修改教师测试去消除失败。各函数的输入、输出、提示见docstring和materials/teacher_lab_guide.md。

## 5 公平比较与指标

两种方式必须使用完全相同的Arrival序列、link容量、缓存容量和观察时长。分组方式额外计算包头；电路方式保留空时隙而不借用。

- 有效载荷利用率 = 完整交付payload bit / (ticks × slot_bits)。
- 线路忙碌率 = 实际发送wire bit / (ticks × slot_bits)，包含包头和未完成记录已发送部分。
- 平均/最大时延：只统计完成记录，包括最后一个tick的传送时间。
- 没有记录完成时，时延为None，表示无样本。
- payload丢失率 = 尾丢弃payload bit / 生成payload bit。没有生成时为0。
- 守恒：生成payload = 已完成payload + 尾丢弃payload + 未完成记录原始payload。

完成记录的时延必须和丢失、积压一起看，不能忽略未完成的大量数据而宣称低时延。基础实验的有限窗口指标不是无限长稳态理论结论。

## 6 四种业务

1. continuous：每4 tick各用户生成128 bit，连续满载；观察分组头对有效吞吐的影响。
2. staggered_burst：每tick一个用户生成96 bit，活跃用户每64 tick轮换；观察固定预留能否适应突发热点。
3. synchronized_burst：每80 tick所有用户各生成8条96 bit记录；观察集中突发的排队与完成时延。
4. light_random：每用户每tick以0.08概率生成96 bit，用固定随机种子2026复现。

至少手算一组2用户、2 tick的小例子；再改变包头长度或缓存大小，讨论结论适用条件。修改参数后的附加结果放在results/extra/。

## 7 运行和提交

```bash
python -m pytest grading/test_circuit.py grading/test_packet.py grading/test_metrics.py -q
python src/performance_test.py
python -m pytest grading/test_integration.py -q
python grading/calculate_grade.py
```

应生成results/comparison.json、comparison.csv、comparison_metrics.png、queue_occupancy.png、pcm_frame_view.png。PCM工具是附带教学示例，32时隙×8 bit×8000帧/s对应2.048 Mbit/s；不要把它与上表的128 kbit/s抽象比较链路混为同一速率。

复制REPORT_TEMPLATE.md为REPORT.md，复制AI_LOG_TEMPLATE.md为AI_LOG.md，写一项student_tests/test_my_case.py，并运行python -m pytest student_tests -q。

```bash
git add src/ REPORT.md AI_LOG.md student_tests/
git add -f results/*.png results/*.json results/*.csv
git commit -m "完成现代交换实验01"
git push
```

在教师仓库创建PR，标题为“现代交换实验01-姓名-学号”。账号信息仅用于课程提交；不要上传密码、API密钥或同学的名单。

## 8 评分100分

| 项目 | 分值 | 方式 |
|---|---:|---|
| 环境可运行 | 5 | 自动 |
| 电路发送 | 20 | 自动，4组测试局部给分 |
| 分组发送 | 20 | 自动，4组测试局部给分 |
| 指标统计 | 15 | 自动，3组测试局部给分 |
| 结果数据与3张图 | 10 | 自动检查产物，教师复核内容 |
| 自拟反例与断言 | 5 | 教师 |
| 实验报告 | 15 | 教师 |
| AI协作记录与核心逻辑解释 | 10 | 教师 |
| 合计 | 100 | 自动70，人工30 |

自动报告中“总分: x/100”只是已获自动分，教师30分尚未计入，不是最终成绩。模板未完成时自动分低属正常。可选包头/负载扫描最多加10分，最终封顶100，基础完整也可得100。

## 9 AI使用和期末衔接

可以让AI解释队列、补全单函数、设计反例和定位报错，但需要自己给出手算预期并核对运行结果。AI_LOG记录一条真实的需求、建议、验证、修正过程；首次正确时可记录边界验证，不编造错误。

期末将复用Config、Arrival、时隙映射、事件时间、利用率/队列观察方法。后续实验逐步加入交换网络和呼叫状态机。

## 10 自动反馈与作业跟踪

GitHub Actions“自动评分系统”提供Summary及grading-report Artifacts；独立反馈流程尽可能在PR评论，无评论时以Summary和Artifacts为准。自动分仅作辅助反馈，教师复核后确定成绩。评分使用教师分支上的测试，学生修改评分脚本不能改变教师的评分规则。

跟踪表见course_management/HOMEWORK_TRACKING.md；GitHub端最新表见“作业情况实时跟踪”Summary和tracking-table Artifact。若教师配置TRACKING_ISSUE_NUMBER，还会更新该Issue中的表。真实名单保留本地，云端按教师配置的私密名单或PR作者跟踪；不得把本地名单提交到公开仓库。

## 11 常见问题

- 大分组超过一个tick怎么办？保留remaining_wire_bits，下一个tick继续发送，不重新加头。
- 为什么时延低却未必更好？可能只送达少量数据，其他仍在积压或已丢失。
- 结果与示例不一致？先检查固定种子、服务顺序、包头和统计窗口，再用小例子定位。
- TODO失败能否提交？可以分阶段提交，查看反馈后改进，最终按提交截止版本评分。
