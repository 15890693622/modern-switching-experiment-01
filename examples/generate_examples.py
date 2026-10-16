"""学生完成TODO后，用自己的实现生成示例格式；教师标准示例已随仓库提供。"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.performance_test import run
if __name__=='__main__':run(Path(__file__).resolve().parent/'student_preview')
