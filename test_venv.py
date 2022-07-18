'''An example file that imports some of the installed modules'''
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import flake8
from platform import python_version

print("python_path: ", sys.executable)
print("python_version: ", python_version())
print("pandas_version: ", pd.__version__)
print("numpy_version: ", np.__version__)
if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")