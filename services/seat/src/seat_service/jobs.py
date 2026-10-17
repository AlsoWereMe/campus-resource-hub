"""本服务的定时任务。在 JOBS 中登记；任务函数必须幂等（见 campus_common/scheduler.py）。

待实现（任务 M1-T10）：每分钟扫描
- 开始前提醒（M1-REM-01）、未签到提醒（M1-REM-02）；
- 超时未签到：违约取消、释放、记违约、通知（M1-VIO-01）；
- 已签到到达结束时间：自动完成（M1-RSV-05）。
非生产环境可经 POST /internal/test/jobs/<name> 立即触发，并用 PUT /internal/test/clock 推进时间。
"""

from campus_common.scheduler import Job

JOBS: list[Job] = []
