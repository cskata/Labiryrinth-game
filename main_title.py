import common

title_l1 = r"""  _    _                      _                   _    _____          _       _ """
title_l2 = r""" | |  | |                    | |                 | |  / ____|        | |     | |"""
title_l3 = r""" | |__| | __ _ _ __  ___  ___| |   __ _ _ __   __| | | |  __ _ __ ___| |_ ___| |"""
title_l4 = r""" |  __  |/ _` | '_ \/ __|/ _ \ |  / _` | '_ \ / _` | | | |_ | '__/ _ \ __/ _ \ |"""
title_l5 = r""" | |  | | (_| | | | \__ \  __/ | | (_| | | | | (_| | | |__| | | |  __/ ||  __/ |"""
title_l6 = r""" |_|  |_|\__,_|_| |_|___/\___|_|  \__,_|_| |_|\__,_|  \_____|_|  \___|\__\___|_|"""

titles = [title_l1, title_l2, title_l3, title_l4, title_l5, title_l6]


def print_centered_main_title():
    for title in titles:
        print("{: ^100s}".format(title))
    press_start = "Press any button to start the game."
    print("\n" * 3)
    print("{: ^100s}".format(press_start))
    start_game = False
    if common.getch():
        start_game = True
