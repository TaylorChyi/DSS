import os
import shutil
from log.logger import log_function
from common.config import *


@log_function
def remove_pycache(path):
    for root, dirs, files in os.walk(path):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            # print(f'Removed __pycache__ from {root}')
    print('CLosed.')