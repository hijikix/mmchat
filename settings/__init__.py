import os
from settings.base import *

bottle_env = os.environ.get("BOTTLE_ENV", "develop")
if bottle_env == "production":
    from settings.production import *
elif bottle_env == "test":
    from settings.test import *
elif bottle_env == "develop":
    from settings.develop import *
else:
    raise Exception("invalid BOTTLE_ENV!!!")
