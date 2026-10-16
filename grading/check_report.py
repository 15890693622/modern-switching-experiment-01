"""仅提示材料完整性，不将标题存在当作人工分析得分。"""
from pathlib import Path

def inspect(root):
    return {name:(root/name).exists() for name in ('REPORT.md','AI_LOG.md','student_tests/test_my_case.py')}
