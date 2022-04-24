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
    "Thunderball (1965)",
    "You Only Live Twice (1967)",
    "On Her Majesty's Secret Service (1969)",
    "Diamonds are Forever (1971)",
    "Live and Let Die (1973)",
    "The Man with the Golden Gun (1974)",
    "The Spy Who Loved Me (1977)",
    "Moonraker (1979)",
    "For Your Eyes Only (1981)",
    "Octopussy (1983)",
    "A View to a Kill (1985)",
    "The Living Daylights (1987)",
    "Licence to Kill (1989)",
    "Goldeneye (1995)",
    "Tomorrow Never Dies (1997)",
    "The World Is Not Enough (1999)",
    "Die Another Day (2002)",
    "Casino Royale (2006)",
    "Quantum of Solace (2008)",
    "Skyfall (2012)",
    "Spectre (2015)",
    "No Time to Die (2021)"
]

ACTORS = [4, 5, 6, 13, 15, 19, len(FILES)-1]
ACTOR_COLOURS = [0, 1, 0, 2, 3, 4, 5]
COLOUR_SET = [
    COLOURS['A+'],
    COLOURS['D+'],
    COLOURS['F+'],
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
    plt.xticks(indices, labels, fontsize=12, rotation=90)
    plt.title(attribute)
    plt.ylabel('Count')
    plt.legend()
    prior = -1
    for i, a in enumerate(ACTORS):
        plt.axvspan(prior+0.5, a+0.5, color=COLOUR_SET[ACTOR_COLOURS[i]%len(COLOUR_SET)], alpha=0.1, lw=0)
        prior = a


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
    plt.xticks(indices, labels, fontsize=14, rotation=90)
    plt.title(', '.join(attributes))
    plt.ylabel('Count')
    plt.legend()
    prior = -1
    for i, a in enumerate(ACTORS):
        plt.axvspan(prior+0.5, a+0.5, color=COLOUR_SET[ACTOR_COLOURS[i]%len(COLOUR_SET)], alpha=0.1, lw=0)
        prior = a