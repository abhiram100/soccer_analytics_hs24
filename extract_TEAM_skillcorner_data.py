from mplsoccer import VerticalPitch
from matplotlib import animation
import matplotlib.pyplot as plt
from pathlib import Path
import imageio.v2 as iio
from tqdm import tqdm
import pandas as pd
import matplotlib
import zipfile
import shutil
import os

from skillcorner_utils import SkillCorner


INPUT_DIR = Path("input/skillcorner")


def extract_data_by_match_id(match_id):
    # skillcorner zip file path
    zip_file = INPUT_DIR / f"{match_id}.zip"

    # Extract the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(INPUT_DIR)

    # match metadata and tracking data file paths
    metadata_file = INPUT_DIR / f"{match_id}.jsonl"
    tracking_file = INPUT_DIR / f"{match_id}_tracking_extrapolated.jsonl"

    # game intelligence data file paths
    physical_file = INPUT_DIR / f"{match_id}_physical.json"
    passes_file = INPUT_DIR / f"{match_id}_passes.json"
    on_ball_pressures_file = INPUT_DIR / f"{match_id}_on_ball_pressures.json"
    off_ball_runs_file = INPUT_DIR / f"{match_id}_off_ball_runs.json"
    
    # TODO(Abhiram): Extract set piece data
    
    skillcorner = SkillCorner()
    skillcorner.load(match_id, metadata_file, tracking_file, physical_file, passes_file, on_ball_pressures_file, off_ball_runs_file)

if __name__ == "__main__":
    
    # Hungary games
    hun_match_ids = [
        1370340,
        1381467,
        1381472,
        1370343,
    ]
    
    # Germany games
    ger_match_ids = [
        1251601,
        1193707,
        1381517,
        1381516,
    ]
    
    match_ids = hun_match_ids + ger_match_ids
    
    for match_id in tqdm(match_ids, desc="Extracting data"):
        extract_data_by_match_id(match_id)