'''
import psutil
# Liệt kê tất cả tiến trình Python
for proc in psutil.process_iter(['pid', 'name']):
    if "python" in proc.info['name'].lower():
        print(proc.info)


import sys

# Liệt kê tất cả các module đã import
print("Modules currently loaded:")
for module_name in sys.modules.keys():
    if "tensorflow" in module_name or "tflite" in module_name:
        print(module_name)

'''

import os
import tensorflow as tf

# Xem các cấu hình log hiện tại
log_level = os.environ.get("TF_CPP_MIN_LOG_LEVEL", "Not Set")
print(f"Current TF_CPP_MIN_LOG_LEVEL: {log_level}")
