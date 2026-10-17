"""platform 的定时任务。在 JOBS 中登记；任务函数必须幂等（见 campus_common/scheduler.py）。

待实现（任务 D-T05，NTF-01）：重试投递失败的邮件（最多 3 次，指数退避）。
"""

from campus_common.scheduler import Job

JOBS: list[Job] = []
