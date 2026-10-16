from campus_common.migrations import import_models, run_migrations
from seat_service.db import Base

import_models("seat_service")
run_migrations([Base.metadata], schemas=["m1"])
