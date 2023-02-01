import numpy as np

orig_colors = {
    '': '#000000',
    'Red': '#CC3311',
    'Purple': '#AA3377',
    'Rose': '#CC6677',
    'Pink': '#FFC0CB',
    'Magenta': '#EE3377',
    'Violet': '#EE82EE',
    'Indigo': '#4B0082',
    'Blue': '#0077BB',
    'Lavender': '#E6E6FA',
    'Cyan': '#66CCEE',
    'Aquamarine': '#7FFFD4',
    'Teal': '#009988',
    'Green': '#228833',
    'Lime': '#00FF00',
    'Yellow': '#CCBB44',
    'Orange': '#EE7733',
    'Ochre': '#CC7722',
    'Brown': '#662506',
    'Gray': '#BEBEBE',
    'Olive': '#808000',
}
color_scale_1 = 1
color_scale_2 = 0.932
color_scale_3 = 0.804
color_scale_4 = 0.548
color_scale_5 = 0.5
color_sc_dict = [1, 0.932, 0.804, 0.548, 0.3, 0.096, 0]
color_scale = {
    '': 0,
    'Red': 0,
    'Purple': 0,
    'Rose': 0,
    'Pink': 2,
    'Magenta': 1,
    'Violet': 1,
    'Indigo': 0,
    'Blue': 0,
    'Lavender': 2,
    'Cyan': 1,
    'Aquamarine': 2,
    'Teal': 0,
    'Green': 0,
    'Lime': 2,
    'Yellow': 2,
    'Orange': 0,
    'Ochre': 0,
    'Brown': 0,
    'Gray': 2,
    'Olive': 1,
}


def adj_colors(h, scale):
    t = tuple(int(round(int(h.lstrip('#')[i:i + 2], 16) * scale)) for i in (0, 2, 4))
    rgb_color = 'rgb(' + str(t[0]) + ', ' + str(t[1]) + ', ' + str(t[2]) + ')'
    return rgb_color


def color_dist(color1, color2):
    t1 = np.array([int(round(int(orig_colors[color1].lstrip('#')[i:i + 2], 16) * color_sc_dict[color_scale[color1]])) for i in (0, 2, 4)])
    t2 = np.array([int(round(int(orig_colors[color2].lstrip('#')[i:i + 2], 16) * color_sc_dict[color_scale[color2]])) for i in (0, 2, 4)])
    rm = 0.5 * (t1[0] + t2[0])
    # print('t1:', t1, '; t2:', t2)
    return np.sqrt(np.inner([2 + rm / 256, 4, 3 + (255 - rm) / 256], (t2 - t1) ** 2))


def colors_are_similar(colors, tol):
    for k in range(6):
        cols = [2 * k, 2 * k + 1]
        if k != 0 or k != 3:
            if k == 1 or k == 2:
                cols.extend([10 + 2 * k, 11 + 2 * k])
            elif k == 4 or k == 5:
                cols.extend([8 + 2 * k, 9 + 2 * k])
        for i in range(len(cols)):
            for j in range(i):
                if color_dist(colors[cols[i]], colors[cols[j]]) < tol:
                    # print('Colors:', colors[cols[i]], 'and', colors[cols[j]], ';', color_dist(colors[cols[i]], colors[cols[j]]))
                    return True
    return False
