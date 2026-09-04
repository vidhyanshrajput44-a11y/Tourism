with open("hotel_data.py", "r") as f:
    code = f.read()

import re

# Just find the def generate_hotel_training_data() and keep everything from there onwards
start_idx = code.find("def generate_hotel_training_data():")

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

if start_idx != -1:
    final_code = new_imports + code[start_idx:]
    with open("hotel_data.py", "w") as f:
        f.write(final_code)
    print("Fixed!")
else:
    print("Not found")

