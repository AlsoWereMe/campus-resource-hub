from campus_common.migrations import import_models, run_migrations
from repair_service.db import Base

import_models("repair_service")
run_migrations([Base.metadata], schemas=["m3"])
