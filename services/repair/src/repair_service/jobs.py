"""本服务的定时任务。在 JOBS 中登记；任务函数必须幂等（见 campus_common/scheduler.py）。"""

from campus_common.scheduler import Job

JOBS: list[Job] = []
