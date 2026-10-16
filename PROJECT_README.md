# 实验平台说明

学生必做代码位于src/part1_circuit.py、src/part2_packet.py、src/metrics.py。其余src模块为教师框架。grading包含可信测试与自动70分汇总；人工复核30分不由脚本伪造。results保存学生产物，examples保存教师标准结果，二者用途不同。

materials保存学生指导书、课堂导入幻灯片及再生成源文件；course_management保存匹配、跟踪和隐私说明。.github/workflows包含只读评分、PR反馈和跟踪三个流程。

创建依据：本地无线通信实验01～03工作流；已根据GitHub官方安全文档调整PR执行权限。详细公平条件见docs/model_contract.md。依赖只声明功能需要的numpy、matplotlib、pytest，不需要付费AI接口或网络仿真软件。
