# =============================================================================
# This file contains configuration of the oTree software used in the experiment
# =============================================================================
from oTree_config.color_adj import adj_colors, orig_colors, color_scale, color_sc_dict

show_instructions = False
show_quiz = True
results = True
orderA = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6'
}
orderB = {
    1: '4',
    2: '5',
    3: '6',
    4: '1',
    5: '2',
    6: '3'
}
order = [orderA, orderB]
no_info = {
    '1': True,
    '2': False,
    '3': False,
    '4': True,
    '5': False,
    '6': False,
}
exog_info = {
    '1': False,
    '2': True,
    '3': False,
    '4': False,
    '5': True,
    '6': False
}
amb_state = {
    '1': False,
    '2': False,
    '3': False,
    '4': True,
    '5': True,
    '6': True
}
state_obj = 'ball'
state_obj_cont = 'jar'
message_obj = 'chip'
message_obj_cont = 'bag'

state_num = ['50', '?']
colors = {col: adj_colors(orig_colors[col], color_sc_dict[color_scale[col]]) for col in orig_colors.keys()}
colors_dark = {col: adj_colors(orig_colors[col], color_sc_dict[color_scale[col]] / 2) for col in orig_colors.keys()}
color_tolerance = 200

# Payoff settings
prize = 20
showup_fee = 10
completion_fee = 15

# Grid settings for CE elicitation
def create_grid(starts, steps):
    grid = []
    for i in range(len(steps)):
        r = starts[i + 1] - starts[i]
        size = int(r / steps[i])
        grid.extend([round(starts[i] + j * r / size, 2) for j in range(size)])
    return grid + [starts[-1]]

starts = [0, 3, 5, 6, 7, 13, 14, 15, 17, 20] # final version
steps = [3, 2, 1, 0.5, 0.25, 0.5, 1, 2, 3] # final version
cert_vals = create_grid(starts, steps)

# Grid settings for value of information
starts = [-5.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 5.0] # final version
steps = [2, 0.5, 0.2, 0.1, 0.2, 0.5, 2] # final version
info_cert_vals = create_grid(starts, steps)

# Randomization thresholds
state_threshold = [50, 73]  # first is risky, second is ambiguous
card_threshold = 23

# Switching consistency
enforce_consistency = False
enforce_strong_consistency = True

# Define Quiz Constants
quiz_cert_vals = [2*i for i in range(0, 6)]
quiz_num_choices = len(quiz_cert_vals)
quiz_indices = [j for j in range(0, quiz_num_choices)]
quiz_form_fields = ['quiz_choice_' + str(k) for k in quiz_indices]
quiz_mpl_choices = list(zip(quiz_indices, quiz_form_fields, quiz_cert_vals))

# Define Constants
num_choices = len(cert_vals)
indices = [j for j in range(0, num_choices)]
form_fields = ['choice_' + str(k) for k in indices]
mpl_choices = list(zip(indices, form_fields, cert_vals))

# Define Info Constants
info_num_choices = len(info_cert_vals)
info_indices = [j for j in range(0, info_num_choices)]
info_form_fields = ['info_choice_' + str(k) for k in info_indices]
info_mpl_choices = list(zip(info_indices, info_form_fields, info_cert_vals))

# oTree settings
name_in_url = 'a_info'
players_per_group = None
num_rounds = len(order[0])
