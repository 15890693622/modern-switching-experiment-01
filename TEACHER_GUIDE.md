# 实验一教师指南

本实验以3个TODO函数为必做，沿用无线实验的模板补全、图表、PR和评分流程。主题是比较电路/分组在不同业务下的利用率和排队代价，不将“分组总是更好”作为预设结论。

## 课堂120分钟

原理与手算20分钟，模板和示例15分钟，实现55分钟，反例20分钟，提交10分钟。90分钟课堂压缩为15/10/45/15/5，报告和自拟用例课后完成。

## 教师课前

阅读README和docs/model_contract.md，运行环境测试与grading/test_framework.py；使用examples里的已验证教师图演示。学生模板含NotImplementedError，核心pytest失败属预期。不要把参考实现放进公开分支。

## 评分

自动70分：环境5、电路20、分组20、指标15、产物10。教师30分：自拟测试5、报告15、AI记录与解释10。自动分显示x/100并明确人工待评。最终分为自动分+人工分+选做最多10，封顶100，最低0。

手工复核要检查图是否来自学生实现、JSON与曲线一致、学生能否解释数据守恒。文件存在不证明正确。公开测试用于反馈，不代替教师抽测。

## 仓库与权限

仓库可作Template或让学生Fork提交PR。自动评分执行PR代码时仅有contents:read，checkout不持久化凭据，无secrets。教师测试和依赖来自PR base提交；只取学生src、报告与产物。PR反馈是独立workflow_run，不执行或导入学生程序；校验关联PR及head SHA，旧版本成绩不覆盖新提交。

PR反馈分数和日志只是教学辅助，学生可在其测试进程内影响输出，最终须复核。不执行未经检查的artifact中的代码或命令。若学生fork的Actions首次运行需GitHub审批，由教师在界面审批。

## 作业跟踪

已启用固定看板：https://github.com/jwentong/modern-switching-experiment-01/issues/2 。仓库变量 `TRACKING_ISSUE_NUMBER=2` 已配置。机器人更新该Issue下的37人提交与自动分表，Actions还提供CSV/Markdown附件。模拟学号LAB01-DEMO-2026单独输出到 `DEMO_TRACKING.md` 与 `demo_tracking.csv`，不会计入班级人数和真实成绩。

仓库设置：Settings → Actions → General。Actions已开启，允许当前工作流所需的官方Actions，默认Workflow permissions维持只读即可，工作流自身已声明反馈和Issue更新权限。不需要上传PAT、部署密钥或设置学生名单Secret。保留首次贡献者Fork运行审批；学生第一次PR若显示等待批准，教师检查改动后点击Approve workflows。无需启用“Allow GitHub Actions to create and approve pull requests”。学生使用个人Fork提交PR，不需要加入仓库Collaborators。

教师日常操作：查看Issue #2的最新机器人表格，必要时在Actions的“作业情况实时跟踪”手动Run workflow。下载tracking-table附件可用Excel打开CSV。自动分最高70，人工30分仍由教师复核后填入Excel；初始Excel成绩簿不会自动同步云端或被覆盖。仅Push到个人Fork而未向教师仓库发PR，不算完成本课程提交。

跨Fork评分反馈通过GitHub实时PR元数据和head SHA关联作业，处理workflow_run未携带pull_requests的情况；旧SHA的分数不覆盖学生新提交。

已按教师要求公开37人名单，见 [学生名单](course_management/students.csv)。[成绩记录说明](course_management/README.md)提供Excel成绩表、评分规则和提交跟踪入口。最新提交状态见“作业情况实时跟踪”Actions的Summary和tracking-table附件。

无token的本地更新将显示待提交，不能把它误认为对GitHub实时提交情况的检查。云端接口错误应报错，不得将API失败伪装为全班未提交。

## 与期末项目衔接

本实验的固定时隙服务与配置接口为后续T/S交换做准备；事件顺序、队列、资源计量可用于呼叫控制和维护观察。不在本次加入完整Web界面、数据库或真实SIP。
