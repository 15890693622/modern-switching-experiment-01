# 学生提交与自动评分流程验收（2026-10-16）

## 实测范围

使用独立测试Fork `plan-lab-szu/modern-switching-experiment-01-e2e-demo`，向教师仓库发起真实跨Fork PR。测试作者使用教师已登录账号，因此不等同于陌生学生账号的首次审批测试。当前仓库审批策略为首次贡献者需批准，教师应在学生PR等待批准时检查改动并点击Approve workflows。

测试PR：https://github.com/jwentong/modern-switching-experiment-01/pull/1 。模拟学号LAB01-DEMO-2026，与37名真实学生完全分表。演示实现故意不完整，没有上传完整参考答案，也没有合并到教学模板。

## 两次真实提交

| 操作 | 预期 | 实际与证据 |
|---|---|---|
| 首次跨Fork PR，保留三个TODO | 环境5分，其他自动项0 | 自动5分，报告status=ok，机器人评论、独立模拟CSV均有记录；[评分运行](https://github.com/jwentong/modern-switching-experiment-01/actions/runs/38912632565) |
| 同一PR再次Push，只返回空闲发送结果 | 电路测试1/4通过，多得5分 | 自动10分，反馈对应新head SHA；[评分运行](https://github.com/jwentong/modern-switching-experiment-01/actions/runs/38913399574) |
| 新提交正在评分，旧提交已有5分 | 新提交不能继承旧分数 | 跟踪附件显示已提交、未评分、分数空白；[跟踪运行](https://github.com/jwentong/modern-switching-experiment-01/actions/runs/38913393971) |
| 完成新评分 | 模拟成绩更新为10分 | demo_tracking.csv中提交次数2、最新评分10/100，教师30分待评 |
| 班级记录隔离 | 保持37人，模拟记录不计入 | 真班级CSV保持37人，不增加模拟学生，不修改真实分数 |

## 测试中发现并修复的问题

GitHub的跨Fork评分workflow_run事件中pull_requests数组实际为空。旧反馈流程虽然显示成功，但跳过了PR评论，从而导致跟踪表无法取得自动分。现通过GitHub实时PR元数据、分支名、head SHA与base仓库共同定位，要求唯一匹配，拒绝过时SHA。

修复后已经在真实GitHub运行中验证机器人评论成功、跟踪附件写入成功及固定Issue表格更新成功。教师分与最终分仍需要教师复核，不把自动分当最终成绩。

## 仓库设置与教师日常操作

- Actions已启用，当前官方Action可运行。
- Workflow permissions默认read，保留即可；各工作流已分别声明所需权限。
- 不需要添加PAT、学生令牌、部署密钥或学生名单Secret。
- 不需要开启Actions创建和批准PR的开关，不需要把37名学生添加为Collaborators。
- 已创建[固定37人看板](https://github.com/jwentong/modern-switching-experiment-01/issues/2)，仓库变量TRACKING_ISSUE_NUMBER=2已设置。
- 学生第一次PR可能等待教师批准；个人Fork上的Push后还须向教师仓库创建PR。后续同一分支Push会更新原PR并重新评分。
- Issue中机器人表格与最新Actions附件为在线记录。仓库main分支内CSV/MD为已保存快照，Excel是教师人工登记簿，不会自动覆盖或实时同步。
- 下载最新tracking-table可获得班级CSV、Markdown及独立模拟记录。人工30分和选做分由教师核定后填写Excel，总分封顶100。

官方设置依据：[仓库Actions设置](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)、[批准Fork工作流](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/approve-runs-from-forks)。
