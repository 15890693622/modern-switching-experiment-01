# 作业跟踪和名单

students.example.csv是示例。真实students.csv仅保留本地，被.gitignore排除。跟踪列沿用无线课：序号、学号、姓名、GitHub用户名、是否提交代码、PR数量、提交次数、最新PR、最新PR状态、最新评分、评分状态、最近提交时间、备注。

匹配优先级：GitHub用户名、分支学号、PR标题学号、姓名。提交状态和评分状态分开。只信任github-actions[bot]自动反馈且head SHA一致的成绩，不读取学生自行写的总分评论。

默认云端按PR作者建匿名列表；教师可自行配置Secret STUDENT_ROSTER_CSV以使用真实名单，但输出表仍隐藏姓名和学号。配置变量TRACKING_ISSUE_NUMBER可将匿名表更新到已有Issue；不配置仍生成Summary和Artifact。

```bash
python grading/update_homework_tracking.py
python -m pytest grading/test_tracking.py -q
```

本地离线模式只生成待提交基线；真实远端状态需GITHUB_TOKEN与GITHUB_REPOSITORY。不要把“未成功获取API”写成“全班未交”。
