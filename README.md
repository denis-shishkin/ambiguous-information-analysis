---
contributors:
  - Pietro Ortoleva
  - Denis Shishkin
---

[![DOI](https://zenodo.org/badge/596248264.svg)](https://zenodo.org/badge/latestdoi/596248264) [![DOI](https://doi.org/10.1016/j.jet.2023.105610)](https://doi.org/10.1016/j.jet.2023.105610)

## Overview

This is a replication package for [Shishkin ® Ortoleva "Ambiguous Information and Dilation: An Experiment"](https://doi.org/10.1016/j.jet.2023.105610), forthcoming in the Journal of Economic Theory.
It contains:

- raw experimental data,
- a Python script which cleans the data and generates variables for analysis,
- a Python script which produces tables 2, 3, 4, 5, 6 and 7,
- a Python script which produces figures 1 and 2,
- a Stata script with some additional analysis.

A replicator should expect to run the code for less than a minute.

## Data Availability and Provenance Statements

### Statement about Rights

- [x] I certify that the author(s) of the manuscript have legitimate access to and permission to use the data used in this manuscript.
- [x] I certify that the author(s) of the manuscript have documented permission to redistribute/publish the data contained within this replication package.

###  License for Data

The data are licensed under a [Creative Commons/CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

### Summary of Availability

- [x] All data **are** publicly available.

### Details on each Data Source

There were four experimental sessions. Two file were extracted from oTree after each session: `amb_info_YYYY_MM_DD.xlsx` containing choice data and `TimeSpent (accessed YYY-MM-DD).csv` containing time stamps for each question in the experiment.

All of these files are located in the `raw_data` folder containing folders for each session.

## Computational requirements

### Software Requirements

- Any OS supporting Python and STATA (the code was tested on macOS 13.1)
- Python 3 (the code was tested with Python 3.8.2)
- STATA version 13.0 or later (the code was tested with STATA 13.0)

### Memory and Runtime Requirements

There are minimal system requirements: the code runs in less than a minute on a standard 2023 desktop machine (the code was tested on a 10-core Apple Silicon-based laptop with 64GB of RAM).

## Description of programs/code

- The script in `cleaning.py` combines the data from all sessions, cleans it, generates new variables for analysis, and saves the output the root directory in `clean_data.csv`.
- The script in `generate_tables.py` produces tex files for tables 2, 5, and 7 and prints the data for tables 3, 4, and 6 in the console. It also performs some auxiliary analyses reported in the paper.
- The script in `generate_figures.py` produces pgf (and pdf) files for figures 1 and 2.
- The script in `order_effects(Tab5).do` performs a test of order effects reported in table 5 using statistical significance stars
