# =============================================================================
# This script produces pgf and pdf files for figures 1 and 2 in the paper
# =============================================================================

import pandas as pd
import numpy as np
from cleaning import d, atzero, abovezero, belowzero
import colorlover as cl
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')
from cleaning import d, q_ce, q_iv, n, atzero, aroundzero, abovezero, belowzero, my_mean, number_of_obs, my_std, filter_main, filter_appendix, cens

fig_dir = 'figs/'
os.makedirs(fig_dir, exist_ok=True)

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
    'Pshort': '$P$',
    'V': 'Value of Information $V$',
    'Vshort': '$V$',
    'R': 'Risky State',
    'A': 'Ambiguous State',
    'Rfig': '1',
    'Afig': '2',
    'Pfig': 'A',
    'Vfig': 'B'
}

orders = {
    'main_text': ['A', 'A', 'B', 'B'],
    'appendix': ['All', 'All', 'All', 'All']
}
cen = 0
order_type = 'main_text'
# order_type = 'appendix'
order = orders[order_type]


# Plotting parameters
barwidth = 0.8
cred = (238, 0, 0)
cblue = (55, 126, 184)
cgreen = (57, 225, 54)
mycolors = [cred, cblue, cgreen]
mycolors_palette = [tuple(i/255 for i in c) for c in mycolors]
sns.set_palette(mycolors_palette)
coltest = cl.scales['3']['qual']['Set1']


def below_cmap(x):
    return (int(x)/255)*0.2 + 0.8
def at_cmap(x):
    return (int(x)/255)*0.5 + 0.5
def above_cmap(x):
    return (int(x)/255)*0.8 + 0.2


cmaps = [below_cmap, at_cmap, above_cmap]
legend_symbols = ['$<0$', '$=0$', '$>0$']

mpl.use('pgf')
plt.style.use('seaborn-white')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
# plt.rcParams['axes.labelweight'] = 'bold'
# plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 10
plt.rcParams['axes.linewidth'] = 1


def size_counter(data, var, state_type, cen, x, y):
    df = data[cens[cen][var+state_type]]
    return df.groupby([var+state_type, 'amb_premium'])['ones'].sum().loc[(x, y)]


def plot_size_scatter(yvar, ax, dt, maxsize=20, sizevar=None, order='All'):
    if order == 'All':
        data = dt.sort_values(by=['amb_attitude'])
    else:
        data = dt[dt.order == order].sort_values(by=['amb_attitude'])
    if sizevar==None:
        sns.scatterplot(x="amb_premium", y=yvar, hue="amb_attitude", hue_order=[
            "averse", "neutral", "seeking"], data=data, alpha=0.3, s=20, ax=ax)
    else:
        data = data.drop_duplicates(
            subset=[var+state_type, 'amb_premium'], keep='first')
        sns.scatterplot(x="amb_premium", y=yvar, hue="amb_attitude", hue_order=[
                        "averse", "neutral", "seeking"], data=data, alpha=0.5, size=sizevar, sizes=(15, 15*maxsize), ax=ax)
    ax.axhline(y=0, color='gray', zorder=2, linewidth=0.5)
    ax.axvline(x=0, color='gray', zorder=2, linewidth=0.5)



for cen in [1]:
    for state_type in ['R', 'A']:
        # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=False, figsize=(10, 10))
        for i, var in zip(range(2), ['P', 'V']):
            fig, axs = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=(
                7, 4.5), gridspec_kw={'width_ratios': [5, 1]})
            ax = axs[0]
            dt = d[cens[cen][var+state_type]]
            sizevar = 'size'+var+state_type+str(cen)
            dt[sizevar] = dt.apply(lambda row: size_counter(dt, var, state_type,
                                                            cen, row[var+state_type], row.amb_premium), axis=1)
            maxsize = max(dt.groupby([var+state_type, 'amb_premium'])['ones'].sum())
            # sizevar = None
            plot_size_scatter(var+state_type, ax, dt, maxsize, sizevar)
            ax.get_legend().remove()
            ax.set(xlabel='Ambiguity Premium', ylabel=labels_dict[var])
            dd = d[filter_main].groupby(['amb_attitude'])[
                var+state_type].agg([atzero, abovezero, belowzero])
            bottoms = [None, dd.belowzero, dd.belowzero+dd.atzero]
            pos_annot = [dd.belowzero/2, dd.belowzero +
                        dd.atzero/2, dd.belowzero+dd.atzero+dd.abovezero/2]
            bars = [dd.belowzero, dd.atzero, dd.abovezero]
            axs[1].xaxis.set_ticks_position('bottom')
            axs[1].set(ylabel=labels_dict[var+'short']+' (%, by attitude)')
            plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=45)
            for k in range(3):
                bar = axs[1].bar([2, 1, 0], bars[k],
                                    width=barwidth, bottom=bottoms[k])
                leg = []
                for j in range(3):
                    col = tuple(cmaps[k](itup) for itup in mycolors[j])
                    bar[j].set_color(col)
                    leg.append(plt.Line2D((0, 1), (0, 0), color=col,
                                        linestyle='-', linewidth=6))
                    axs[1].annotate(legend_symbols[k],
                                    xy=(j, pos_annot[k][2-j]), xycoords='data',
                                    size=7, ha='center', va='center')
            axs[1].set_xticks([0, 1, 2], minor=False)
            axs[1].set_xticklabels(['seeking', 'neutral', 'averse'], minor=False)
            axs[1].set_xticks([0, 1, 2], minor=False)
            axs[1].set_xticklabels(['seeking', 'neutral', 'averse'], minor=False)
            if sizevar == None:
                sizelabel = ''
            else:
                sizelabel = '_size'
            plt.tight_layout()
            plt.subplots_adjust(left=0, bottom=0.1, right=0.9,
                                top=0.9, wspace=0.3, hspace=0.3)
            plt.savefig(fig_dir + 'fig_' + labels_dict[state_type + 'fig'] +
                        labels_dict[var + 'fig'] + '_' +
                        state_type + '_' + var + '_' + '.pdf', bbox_inches='tight')
            plt.savefig(fig_dir + 'fig_' + labels_dict[state_type + 'fig'] +
                        labels_dict[var + 'fig'] + '_' +
                        state_type + '_' + var + '_' + '.pgf', bbox_inches='tight')
