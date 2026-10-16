# Git与提交速查

在教师仓库Fork后Clone自己的副本。若本仓库启用Template也可创建副本，但向教师仓库提交PR时须确认分支关联方式。

```bash
git status
git add src/ REPORT.md AI_LOG.md student_tests/
git add -f results/*.png results/*.json results/*.csv
git commit -m "完成现代交换实验01"
git push
```

PR标题：现代交换实验01-姓名-学号。每次修改后push现有PR自动更新。不要把本地真实名单或整个课程目录加入Git。
