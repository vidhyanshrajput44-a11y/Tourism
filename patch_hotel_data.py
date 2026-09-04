import re

with open("hotel_data.py", "r") as f:
    code = f.read()

new_imports = """import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import httpx
import os
import json

with open("hotels_db_dump.json", "r") as f:
    HOTELS_DB = json.load(f)
"""

code = re.sub(r'import pandas as pd.*?HOTELS_DB = \{.*?\}\n', new_imports, code, flags=re.DOTALL)

with open("hotel_data.py", "w") as f:
    f.write(code)
print("Patched hotel_data.py")
