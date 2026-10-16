# 实验一学生名单与成绩记录

在线最新看板：[37人作业提交与自动评分记录](https://github.com/jwentong/modern-switching-experiment-01/issues/2)。已设置仓库变量TRACKING_ISSUE_NUMBER=2，机器人在Issue评论中更新。测试PR以 `[流程测试]` 标题和 `e2e-demo/` 分支标识，单独记入DEMO_TRACKING.md及demo_tracking.csv，不影响真实37人表。

已按教师要求上传核对后的37人名单：students.csv。仅包含序号、学号、姓名、GitHub用户名和备注。

- **实验一成绩记录表_37人.xlsx**：教师日常登记用，宋体；黄色单元格录入成绩，教师分、最终分与成绩状态自动计算。自动评分填入PR反馈中的实际分数（满分70），不得使用模板仓库自测分代替学生成绩。缺项时总分留空，实际0分可以正常计算。GitHub用户名可陆续填写。
- **实验一成绩记录表_37人.csv / .md**：首次建表快照，CSV兼容Excel，但不含公式；填写后的Excel请由教师保存，不会被云端任务覆盖。
- **homework_tracking.csv / HOMEWORK_TRACKING.md**：提交跟踪快照，沿用无线技术实验字段。最新动态数据在“作业情况实时跟踪”Actions的Summary和tracking-table附件，每次PR变化和每6小时刷新。仓库内静态文件不由Actions自动提交覆盖。

评分结构：自动70分＋教师30分（自拟反例5、实验报告15、AI协作记录10）；选做最多加10分，总成绩封顶100。四个必评分项完整录入后才显示最终成绩。未评分不等于0分。

提交匹配优先级：GitHub用户名、分支学号、PR标题学号、PR标题姓名。仅采用github-actions[bot]且对应当前head SHA的评分反馈。教师可选配TRACKING_ISSUE_NUMBER，将跟踪表同步到已有Issue。

```bash
python grading/update_homework_tracking.py
python -m pytest grading/test_tracking.py -q
```

离线运行只生成待提交基线；查询远端需GITHUB_TOKEN和GITHUB_REPOSITORY。API失败时停止，不能将获取失败解释为全班未交。
