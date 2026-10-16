from campus_common.migrations import import_models, run_migrations
from room_service.db import Base

import_models("room_service")
run_migrations([Base.metadata], schemas=["m2"])
