import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

from destijl.style import COLOURS

DATA_DIR = "data"

SCORE_COLUMNS = [
    'Opening Scene',
    'Theme Song',
    'James Bond',
    'Bond Girl',
    'Allies and Supporting Cast',
    'Villain & Henchmen',
    'Car and Gadgets',
    'Locations',
    'Presentation',
    'Plot / Sophisticated Movie Critique',
    'Problematic',
    'Memery',
    'Wild Card',
    'Overall',
]

FILES = [
    "Dr. No (1962)",
    "From Russia With Love (1963)",
    "Goldfinger (1964)",
    "Thunderball (1965)"
]

def prep_film(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, usecols=SCORE_COLUMNS)
    return pd.concat({"mean": df.mean(), "median": df.median(), "responses": df.count()}, axis=1)


def prep_all_films() -> Dict[str, pd.DataFrame]:
    dfs = {}
    for file in FILES:
        dfs[file] = prep_film(f'{DATA_DIR}/{file}.csv')
    return dfs


def plot_attribute_across_film(films: Dict[str, pd.DataFrame], attribute: str) -> None:
    """please ignore my lazy pandas"""
    means, medians, counts = [], [], []
    labels = []
    for f, df in films.items():
        labels.append(f)
        mean, median, count = df.loc[attribute]
        means.append(mean)
        medians.append(median)
        counts.append(count)
    plt.figure(figsize=(12, 8))
    indices = np.arange(len(films))
    plt.bar(indices - 0.075, means, label='mean', alpha=0.5, color=COLOURS['A'], width=0.15)
    plt.bar(indices + 0.075, medians, label='median', alpha=0.5, color=COLOURS['C'], width=0.15)
    plt.xticks(indices, labels, fontsize=14, rotation=45)
    plt.title(attribute)
    plt.ylabel('Count')
    plt.legend()


def plot_multiple_attributes(films: Dict[str, pd.DataFrame], attributes: List[str], value: str) -> None:
    values = {a: [] for a in attributes}
    labels = []
    for f, df in films.items():
        labels.append(f)
        for a in attributes:
            values[a].append(df.loc[a][value])
    plt.figure(figsize=(16, 12))
    indices = np.arange(len(films))
    for a in attributes:
        plt.plot(indices, values[a], '+-', label=f"{a}:{value}", markersize=12, markeredgecolor='k')
    plt.xticks(indices, labels, fontsize=14, rotation=45)
    plt.title(', '.join(attributes))
    plt.ylabel('Count')
    plt.legend()