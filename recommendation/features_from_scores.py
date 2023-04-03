import json
import numpy as np
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))  # run from top dir with  python3 recommendation/score_retrival.py

print("sys.path", sys.path)

from recommendation.feature_extraction.load_features import convert_features
convert_features("recommendation/results/results")