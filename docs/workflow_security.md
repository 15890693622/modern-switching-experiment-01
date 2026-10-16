# 自动评分执行边界

参考GitHub官方文档：https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target 与 https://docs.github.com/en/actions/reference/security/secure-use 。

评分使用pull_request事件、只读token和不持久化凭据的checkout。可信测试/依赖来自base提交，只覆盖学生src、results和报告；不执行PR修改的workflow或依赖文件。独立workflow_run只下载JSON并验证大小、字段和当前PR的SHA，不执行artifact或学生代码。

本系统用于低风险教学自动反馈，公开测试不是抗对抗的安全判卷器；学生可在Python进程中干扰输出，最终成绩必须教师复核。不要向评分job传入secrets。跟踪job只执行默认分支的可信脚本，姓名和学号不输出到云端表。

使用仓库已有成熟checkout v4.2.2、upload-artifact v4.6.2、github-script v7.0.1，setup-python采用官方Node24版v6；发布时记录的实际Actions运行结果比版本号推测更可靠。
