# =============================================================================
# This script produces tex files for tables 2, 5, and 7 and prints the data for
# tables 3, 4, and 6 in the console. It also does some auxiliary analysis
# reported in the paper.
#
# Needs to be run from a directory which contains folders with raw session data
# from oTree each named as YYYY-MM-DD
# =============================================================================

import pandas as pd
import numpy as np
import scipy.stats
from math import log10, floor
from oTree_config.config import form_fields, info_form_fields, cert_vals, info_cert_vals
from datetime import datetime
from dateutil import tz
import seaborn as sns
from cleaning import d, q_ce, q_iv, n, atzero, aroundzero, abovezero, belowzero, my_mean, number_of_obs, my_std, filter_main, filter_appendix, cens
import colorlover as cl
import matplotlib.pyplot as plt
import econtools.metrics as mt
import os


tables_dir = 'tables/'
os.makedirs(tables_dir, exist_ok=True)
labels_dict = {
    'number_of_obs': '\# of obs.',
    'median': 'median',
    'mean': 'mean',
    'my_mean': 'mean',
    'w_mean': 'wins. mean',
    'std': 'st. dev.',
    'my_std': 'st. dev.',
    'atzero': '$=0$',
    'abovezero': '$>0$',
    'belowzero': '$<0$',
    'aroundzero': '$\\approx 0$',
    'amb_attitude': 'Ambiguity attitude',
    'iv3': 'Value of information (risky)',
    'P': 'Information Premium $P$',
    'V': 'Value of Information $V$',
    }
format_dict = {
    'number_of_obs': '{:.0f}',
    'median': '{:.2g}',
    'mean': '{:.2g}',
    'my_mean': '{:.2g}',
    'w_mean': '{:.2g}',
    'std': '{:.2g}',
    'atzero': '{:.0f}\%',
    'abovezero': '{:.0f}\%',
    'belowzero': '{:.0f}\%',
    'aroundzero': '{:.0f}\%',
    'my_std': '{:.2g}'}

lvls = ['amb_attitude', 'order']
vars = ['iv3', 'iv6']
states = ['Risky state', 'Ambiguous state']



report_rows = [np.median, my_mean]
zero_rows = [aroundzero, atzero, abovezero, belowzero, number_of_obs]


orders = {
    'main_text': {
        'R': ['All'],
        'A': ['All']
    },
    'appendix': {
        'R': ['A', 'B'],
        'A': ['A', 'B']
    }
}

def concat(objs):
    return pd.concat(objs, axis=1, sort=False)


def forder(data, o):
    if o == 'All':
        return data
    else:
        return data[data.order == o]


def sum_var(var, cen, order_type):
    data = d[cens[cen][var]]
    ords = orders[order_type][var[-1]]
    if var[0] == 'V':
        rr = [np.median, my_mean, atzero, abovezero, belowzero, number_of_obs]
        tab = concat([concat([
            forder(data, o).groupby(['constant'])[var].agg(rr).T,
            forder(data, o).groupby(['amb_attitude'])[var].agg(rr).T
        ]) for o in ords])
    if var[0] == 'P':
        rr = report_rows
        zr = zero_rows
        tab = concat([concat([concat([
            forder(data, o).groupby(['constant'])[var].agg(rr),
            forder(data, o).groupby(['constant'])['diff'+var].agg(zr)
        ]).T, concat([
            forder(data, o).groupby(['amb_attitude'])[var].agg(rr),
            forder(data, o).groupby(['amb_attitude'])['diff'+var].agg(zr)
        ]).T]) for o in ords])
    return tab[['All', 'averse', 'neutral', 'seeking']]


def sum_vars(var, cen, order_type):
    # Summary of a variable
    return concat([
        sum_var(var+'R', cen, order_type),
        pd.DataFrame(index=sum_var(var+'R', cen, order_type).index, columns=[' ']),
        sum_var(var+'A', cen, order_type)],
    )


def new_write_to_tex(vars, cen, order_type):
    direc = tables_dir+"new_sum_"+order_type+'_'+str(cen)+".tex"
    subcols = ['All', 'averse', 'neutral', 'seeking']
    nsubcols = len(subcols)

    with open(direc, "w") as f:
        nordersR = len(orders[order_type]['R'])
        nordersA = len(orders[order_type]['A'])
        norders = nordersR + nordersA
        print('Printing to', direc)
        f.write("% !TeX root = ../main.tex\n")
        f.write("\\begin{tabular}{ r " +
                " ".join(["c"] * (2 + nsubcols*norders)) + " }\n\\toprule \n")
        f.write(
            "& \\multicolumn{"+str(nsubcols*nordersR)+"}{c}{\\it Risky payoff state} & & \\multicolumn{"+str(nsubcols*nordersR)+"}{c}{\\it Ambiguous payoff state}\\\\\n")
        f.write(' '.join([
            '\\cmidrule[\\mrw](lr){'+str(2+i*(nordersR*nsubcols+1)) +
            '-'+str(2+nordersR*nsubcols-1+i*(nordersR*nsubcols+1))+'}'
            for i in [0, 1]]) + '\n')
        f.write('ambiguity attitude & '+' & & '.join(2*[' & '.join(
            ['\\multicolumn{'+str(nordersR)+'}{c}{' + c + '}' for c in subcols])]) + '\\\\\n')
        if (order_type == 'appendix'):
            f.write(' '.join(['\\cmidrule[\\mrw](lr){'+str(2+i*nordersR)+'-'+str(3+i*nordersR)+'}' for i in range(nsubcols)]))
            f.write(' '.join(['\\cmidrule[\\mrw](lr){'+str(11+i*nordersR)+'-'+str(
                12+i*nordersA)+'}' for i in range(nsubcols)]) + '\n')
            f.write("order" + " & " + 
                " & ".join(nsubcols * orders[order_type]['R']) + " & & " +
                " & ".join(nsubcols * orders[order_type]['A']) + '\\\\\n')
        for var in vars:
            f.write("\\midrule[\\mrw] \n")
            f.write(
                "& \\multicolumn{"+str(norders * nsubcols + 1)+"}{c}{"+labels_dict[var]+"}\\\\ \n")
            f.write("\\midrule[\\mrw] \n")
            k = 0
            for i, row in sum_vars(var, cen, order_type).iterrows():
                k = k+1
                if var == 'V' or (k < len(sum_vars(var, cen, order_type))):
                    f.write(
                        " & ".join([labels_dict[row.name]] +
                        ['' if np.isnan(x) else format_dict[row.name].format(x) for x in row.values]) + " \\\\\n")
                if var == 'V' and (k == len(sum_vars(var, cen, order_type))-1):
                        f.write("\\midrule[\\mrw] \n")
        f.write("\\bottomrule \n \\end{tabular}")
    return concat([sum_vars(vars[0], cen, order_type), sum_vars(vars[1], cen, order_type)])

# =============================================================================
# Table 2
# =============================================================================

new_write_to_tex(['P', 'V'], 1, 'main_text')

# =============================================================================
# Table 3: Ambiguity attitude in the sample
# =============================================================================

print('Table 3: Ambiguity attitude in the sample')
data = d[filter_appendix]
print(data.groupby(['amb_attitude', 'order'])
      [['delta14']].agg([number_of_obs]).T)

# =============================================================================
# Table 4: Ambiguity premia in the sample
# =============================================================================

print('Data for Table 4: Ambiguity premia in the sample')
print('By order')
data = d[filter_appendix]
print(data.groupby(['amb_attitude', 'order'])
      [['delta14']].agg([np.median, my_mean, number_of_obs]).T)
print('For both A and B orders')
print(data.groupby(['amb_attitude'])
      [['delta14']].agg([np.median, my_mean, number_of_obs]).T)

# =============================================================================
# Table 5
# =============================================================================

new_write_to_tex(['P', 'V'], 1, 'appendix')

# =============================================================================
# Table 6: Ambiguity attitude in the sample (all observations)
# =============================================================================

print('Table 6: Ambiguity attitude in the sample')
data = d[filter_main]
print(data.groupby(['amb_attitude', 'order'])
      [['delta14']].agg([number_of_obs]).T)

# =============================================================================
# Table 7
# =============================================================================

new_write_to_tex(['P', 'V'], 0, 'main_text')

# =============================================================================
# Discussion: Ignoring information
# =============================================================================

print('Percentage of subjects who chose the same color as in the message')
dt = d[d.index.isin(filter_appendix) & d.index.isin(d.amb_attitude == 'averse')]
arr1 = dt[dt.chose_given_color2 == 1].PR
arr2 = dt[dt.chose_given_color2 == 0].PR

print('In Q2')
print(d.groupby(['amb_attitude']).chose_given_color2.agg(
    [my_mean]).T)

print('In Q5')
print(d.groupby(['amb_attitude']).chose_given_color5.agg(
    [my_mean]).T)
