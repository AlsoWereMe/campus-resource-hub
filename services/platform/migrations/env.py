from campus_common.migrations import import_models, run_migrations
from platform_service.db import METADATAS, SCHEMAS

import_models("platform_service")
run_migrations(METADATAS, schemas=SCHEMAS)
