"""本服务的定时任务。在 JOBS 中登记；任务函数必须幂等（见 campus_common/scheduler.py）。

待实现（任务 M2-T06）：每分钟扫描
- 到达审批截止仍在审批中：超时撤销、释放 HOLD、通知（M2-TMO-01，BR-M2-11）；
- 截止前 R 小时提醒当前级别审批人，每级一次（M2-TMO-02）；
- 已通过的申请到达结束时间：置为已完成（M2-TMO-03）。
"""

from campus_common.scheduler import Job

JOBS: list[Job] = []
