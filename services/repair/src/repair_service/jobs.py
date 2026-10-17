"""本服务的定时任务。在 JOBS 中登记；任务函数必须幂等（见 campus_common/scheduler.py）。

待实现：每分钟扫描
- 任务 M3-T05：当前阶段超时升级 L1（通知调度员）、超过 2 倍时限升级 L2（通知物业主管）（M3-ESC-02）；
- 任务 M3-T04：待验收超过 m3.auto_accept_hours 自动验收并释放下架（M3-ACC-03）。
"""

from campus_common.scheduler import Job

JOBS: list[Job] = []
