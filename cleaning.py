import pandas as pd
import numpy as np
import scipy.stats
from math import log10, floor
from oTree_config.config import form_fields, info_form_fields, cert_vals, info_cert_vals
from datetime import datetime
from dateutil import tz
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# Load the data
# =============================================================================

raw_data_dir = 'raw_data/'

# Enter session dates
sessions = ['2019-02-12', '2019-02-14', '2019-02-16', '2019-02-19']

def pexl_time(timestamp):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    utc = datetime.utcfromtimestamp(timestamp)
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    # central.strftime("%Y-%m-%d %H:%M:%S")
    return central.strftime("%Y-%m-%d %H:%M:%S")


print('Analyzing duration of the sessions...')

for s in sessions:
    df_time1 = pd.read_csv(raw_data_dir+s+'/TimeSpent (accessed '+s+').csv')
    d_time1 = pd.pivot_table(
        df_time1,
        values=['time_stamp', 'seconds_on_page'],
        columns=['page_index'],
        index=['participant__code']
        )
    d_time1['total_time'] = d_time1['time_stamp'][48] - d_time1['time_stamp'][1]
    print('Session', s, 'lasted', np.round(max(
        d_time1['total_time'])/60, 1), 'min, average time spent:', np.round(np.mean(d_time1['total_time'])/60, 1), 'min.')

# Load all data into a single pandas frame
frames = []
for s in sessions:
    frames = frames + [pd.read_excel(raw_data_dir+s+'/amb_info_'+s+'.xlsx')]

df = pd.concat(frames, sort=False)

# Rename columns for easier access
colnames = df.columns.tolist()
renaming = {
    'player': '',
    'group': '',
    'subsession': '',
    'session': '',
    'participant': 'prt_'}

for coltype in list(renaming.keys()):
    colnames = [n.replace(coltype + '.', renaming[coltype]) for n in colnames]
df.columns = colnames

# Drop empty obs
df = df[np.logical_not(df.state_rd.isnull())]

# Calculate number of observations
N = len(df)
print('Total number of subjects:', N/6)

# =============================================================================
# Payments
# =============================================================================

print('Analyzing payments...')
df.payoff
print('Average payment: $', np.round(df.payoff.sum()/(N/6),1), 'per capita (excluding $10 show-up fee and $15 completion fee)')

# =============================================================================
# Determine the type of a question
# =============================================================================

df['info_question'] = np.logical_or(df.question == 3, df.question == 6)

# =============================================================================
# Find switching rows
# =============================================================================

df['ce_index'] = (df[form_fields] == 'A').sum(axis=1)  # Certainty equivalent
df['iv_index'] = (df[info_form_fields] == 'A').sum(axis=1)  # Information value

cert_vals = [cert_vals[0]] + cert_vals + [cert_vals[-1]]
df['ce'] = [(cert_vals[i+1]+cert_vals[i])/2 for i in df.ce_index]

info_cert_vals = [info_cert_vals[0]] + info_cert_vals + [info_cert_vals[-1]]
df['iv'] = [(info_cert_vals[i+1]+info_cert_vals[i])/2 for i in df.iv_index]


df['ce_w'] = [
    int(i in [0, len(form_fields)])
    for i in df.ce_index]
df['iv_w'] = [0] * N
df.loc[df.info_question, ['iv_w']] = [
    int(i in [0, len(info_form_fields)])
    for i in df[df.info_question].iv_index]

ce_cols = ['prt_code','question','order_treatment','ce_index', 'ce']
iv_cols = ['prt_code','question','order_treatment','iv_index', 'iv']
# df[(df.ce_index > 34) & df.info_question].loc[:,ce_cols]
df[(df.ce_w == 1)].loc[:,ce_cols]
df[(df.iv_w == 1)].loc[:,iv_cols]

# =============================================================================
# Checking whether chosen color == given color
# =============================================================================

df['chose_given_color'] = df.info_validate == df.chosen_color

# =============================================================================
# Reshape data
# =============================================================================

def wide_table(var, qs):
    return pd.pivot_table( 
        df,
        values=var,
        columns=['question'],
        index=['prt_code']
        ).loc[:, qs].rename(
            index=str,
            columns={q: var+str(q) if len(qs) > 1 else var for q in qs}
            )


def add_variable(var, qs, d=None):
    if d is None:
        return wide_table(var, qs)
    else:
        return pd.concat([d, wide_table(var, qs)], axis=1, sort=False)


# Constants
def add_cvariable(var, d, q=1):
    return pd.concat([
        d,
        df[df.round_number == q].loc[:, ['prt_code', var]].set_index('prt_code')
    ], axis=1, sort=False)

# =============================================================================
# Define main variables from choice data
# =============================================================================

# Main vars
d = add_variable('ce', [1, 2, 3, 4, 5, 6])
d = add_variable('iv', [3, 6], d)
d = add_variable('ce_index', [1, 2, 3, 4, 5, 6], d)
d = add_variable('iv_index', [3, 6], d)
n = len(d)
d = add_variable('ce_w', [1, 2, 3, 4, 5, 6], d)
d = add_variable('iv_w', [3, 6], d)

# Order treatment
d = add_variable('order_treatment', [1], d)
d['order'] = d['order_treatment']
d = d.replace({'order': {1: 'B', 0: 'A'}})

# Robustness checks
d = add_variable('chose_given_color', [2, 5], d)

# Miscellaneous
d = add_variable('chose_info', [3, 6], d)
d = add_cvariable('prt_time_started', d).rename(columns = {'prt_time_started': 'date'})
d.date = [i[5:10] for i in list(d.date)]
d = add_cvariable('feedback', d, 6)

# PC Label
d = add_cvariable('prt_label', d)
d['PC_label'] = [int(i[3:]) for i in list(d.prt_label)]
d = d.drop(columns=['prt_label'])


# =============================================================================
# Filter observations
# =============================================================================

q_ce = ['ce1', 'ce2', 'ce3', 'ce4', 'ce5', 'ce6']
q_iv = ['iv3', 'iv6']

# =============================================================================
# Calculate additional variables
# =============================================================================

d['risk_premium'] = d.ce1 - 10
d['amb_premium'] = d.ce1 - d.ce4
d['delta24'] = d.ce2 - d.ce4
d['delta12'] = d.ce1 - d.ce2
d['delta14'] = d.ce1 - d.ce4
d['delta45'] = d.ce4 - d.ce5
d['delta15'] = d.ce1 - d.ce5
d['pdelta24'] = (d.ce2 - d.ce4)/d.ce2
d['pdelta12'] = (d.ce1 - d.ce2)/d.ce1
d['pdelta14'] = (d.ce1 - d.ce4)/d.ce1
d['PR'] = d.ce2 - d.ce1
d['PA'] = d.ce5 - d.ce4
d['VR'] = d.iv3
d['VA'] = d.iv6

d['diffellsberg'] = d.ce_index4 - d.ce_index1
d['diffPR'] = d.ce_index2 - d.ce_index1
d['diffPA'] = d.ce_index5 - d.ce_index4
d['diffVR'] = d.iv_index3 - int((len(info_cert_vals)-1)/2)
d['diffVA'] = d.iv_index6 - int((len(info_cert_vals)-1)/2)

d['amb_attitude'] = 'neutral'
d.loc[d.diffellsberg < -1.1, ['amb_attitude']] = 'averse'
d.loc[d.diffellsberg > 1.1, ['amb_attitude']] = 'seeking'

d['ones'] = 1
d['constant'] = 'All'

# =============================================================================
# Save to csv
# =============================================================================

d.to_csv('cleaned_data.csv', index=False)

# =============================================================================
# Define functions and filters to be used for figures and tables
# =============================================================================

filter_main = [True]*len(d)  # all data
filter_appendix = (d.ce_w4 == 0)  # only those who chose undominated in Q4

# Define censoring dictionary
cens = {
    0: {  # censoring of type 0 = all data, to include in appendix
        'PR': filter_main,
        'PA': filter_main,
        'VR': filter_main,
        'VA': filter_main},
    1: {  # censoring of type 1 = undominated options, to include in main text
        'PR': filter_appendix,
        'PA': filter_appendix,
        'VR': filter_appendix,
        'VA': filter_appendix},
}


def round_to_n(x, n):
    return round(x, -int(floor(log10(x))) + (n - 1))


def number_of_obs(arr):
    return np.round(np.size(arr), 2)


def my_mean(arr):
    return np.round(np.mean(arr), 2)


def w_mean(arr):
    return np.round(np.mean(scipy.stats.mstats.winsorize(arr, limits=0.05)), 2)


def my_std(arr):
    return np.round(np.std(arr), 2)


def atzero(arr):
    return np.round(np.mean([int(abs(i) < 0.1)*100 for i in arr]), 1)


def aroundzero(arr):
    return np.round(np.mean([int(abs(i) < 1.1)*100 for i in arr]), 1)


def abovezero(arr):
    return np.round(np.mean([int(i > 0.1)*100 for i in arr]), 1)


def belowzero(arr):
    return np.round(np.mean([int(i < -0.1)*100 for i in arr]), 1)
