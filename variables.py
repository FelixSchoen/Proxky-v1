class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ids:
    SPREAD = "id_spread"
    GROUP_NORMAL_O = "id_group_normal_o"
    GROUP_SPLIT_O = "id_group_split_o"
    ARTWORK_O = "id_artwork_o"
    TYPE_O = "id_type_o"
    NAME_T = "id_name_t"
    TYPE_LINE_T = "id_type_line_t"
    MANA_COST_T = "id_mana_cost_t"
    MODAL_T = "id_modal_t"
    GROUP_MODAL_O = "id_group_modal_o"
    COLOR_BARS_O = "id_color_bars_o"
    GRADIENTS_O = "id_gradients_o"
    ORACLE_TEXT_T = "id_oracle_text_t"
    ORACLE_TEXT_O = "id_oracle_text_o"
    ADVENTURE_ORACLE_TEXT_L_T = "id_adventure_oracle_text_l_t"
    ADVENTURE_ORACLE_TEXT_L_O = "id_adventure_oracle_text_l_o"
    ADVENTURE_ORACLE_TEXT_R_T = "id_adventure_oracle_text_r_t"
    ADVENTURE_ORACLE_TEXT_R_O = "id_adventure_oracle_text_r_o"
    GROUP_ORACLE_PLANESWALKER_O = "id_group_oracle_planeswalker_o"
    PLANESWALKER_VALUE_T = "id_planeswalker_value_t"
    PLANESWALKER_VALUE_O = "id_planeswalker_value_o"
    PLANESWALKER_TEXT_T = "id_planeswalker_text_t"
    PLANESWALKER_TEXT_O = "id_planeswalker_text_o"
    GROUP_ORACLE_ADVENTURE_O = "id_group_oracle_adventure_o"
    MASK_O = "id_mask_o"
    VALUE_T = "id_value_t"
    VALUE_O = "id_value_o"
    VALUE_SHORT_FRAME_O = "id_value_short_frame_o"
    VALUE_LONG_FRAME_O = "id_value_long_frame_o"
    MASK_SHORT_O = "id_mask_short_o"
    MASK_LONG_O = "id_mask_long_o"
    GROUP_BOTTOM_O = "id_bottom_o"
    ARTIST_T = "id_artist_t"
    SIDE_INDICATOR_T = "id_side_indicator_t"
    SIDE_INDICATOR_O = "id_side_indicator_o"
    COLLECTOR_INFORMATION_T = "id_collector_information_t"
    SET_O = "id_set_o"


# IDs
id_general_front = {
    "id_spread": "uff",
    "id_artwork_o": "u2e6",
    "id_type_o": "u2e5",
    "id_name_t": "u2d0",
    "id_type_line_t": "u2ba",
    "id_mana_cost_t": "u2a4",
    "id_color_bars_o": ['u2a0', 'u29f', 'u122', 'u121'],
    "id_gradients_o": ['ue1', 'ue3', 'ue2', 'ue4'],
    "id_oracle_text_t": "u25e",
    "id_oracle_text_o": "u270",
    "id_mask_o": "u106",
    "id_value_t": "u196",
    "id_value_o": "u1a8",
    "id_value_short_frame_o": "u130",
    "id_value_long_frame_o": "u123",
    "id_mask_short_o": "u12f",
    "id_mask_long_o": "u108",
    "id_bottom_o": "u109",
    "id_artist_t": "u176",
    "id_collector_information_t": "u13e",
    "id_set_o": "u13c",
    "id_group_normal_o": "uc21",
    "id_group_split_o": "u1cdf",
    "id_modal_t": "u281",
    "id_group_modal_o": "u274",
    "id_group_oracle_planeswalker_o": "u1ac",
    "id_planeswalker_value_t": ['u248', 'u21c', 'u1f0', 'u1c4'],
    "id_planeswalker_value_o": ['u25a', 'u22e', 'u202', 'u1d6'],
    "id_planeswalker_text_t": ['u232', 'u206', 'u1da', 'u1ae'],
    "id_planeswalker_text_o": ['u244', 'u218', 'u1ec', 'u1c0'],
    "id_group_oracle_adventure_o": "ub82",
    "id_side_indicator_t": "u160",
    "id_side_indicator_o": "u153",
}
id_general_front_st = {
    "id_spread": "uff",
    "id_artwork_o": "u18f4",
    "id_type_o": "u18f3",
    "id_name_t": "u18df",
    "id_type_line_t": "u18c8",
    "id_mana_cost_t": "u18b1",
    "id_color_bars_o": ['u18a9', 'u18a8', 'u16c8', 'u16c7'],
    "id_gradients_o": ['u2634', 'u2626', 'u2628', 'u2633'],
    "id_oracle_text_t": "u1872",
    "id_oracle_text_o": "u186f",
    "id_mask_o": "u16ab",
    "id_value_t": "u1727",
    "id_value_o": "u1724",
    "id_value_short_frame_o": "u16d0",
    "id_value_long_frame_o": "u16c9",
    "id_mask_short_o": "u16cf",
    "id_mask_long_o": "u16ad",
    "id_bottom_o": "u16ae",
    "id_artist_t": "u170c",
    "id_collector_information_t": "u16d9",
    "id_set_o": "u16d5",
}
id_general_front_sb = {
    "id_spread": "uff",
    "id_artwork_o": "u1ccf",
    "id_type_o": "u1cce",
    "id_name_t": "u1cba",
    "id_type_line_t": "u1ca3",
    "id_mana_cost_t": "u1c8c",
    "id_color_bars_o": ['u1c84', 'u1c83', 'u1c14', 'u1c13'],
    "id_gradients_o": ['u262a', 'u262a', 'u2631', 'u2631'],
    "id_oracle_text_t": "u1c6d",
    "id_oracle_text_o": "u1c6a",
    "id_mask_o": "u1bf7",
    "id_value_t": "u1c56",
    "id_value_o": "u1c53",
    "id_value_short_frame_o": "u1c1b",
    "id_value_long_frame_o": "u1c15",
    "id_mask_short_o": "u1c1a",
    "id_mask_long_o": "u1bf9",
    "id_bottom_o": "u1bfa",
    "id_artist_t": "u1c3b",
    "id_collector_information_t": "u1c24",
    "id_set_o": "u1c20",
}
id_general_front_adventure = {
    "id_spread": "uff",
    "id_type_o": "ubca",
    "id_name_t": "ubb6",
    "id_type_line_t": "ub9f",
    "id_mana_cost_t": "ub88",
    "id_color_bars_o": ['uc15', 'uc16'],
    "id_gradients_o": ['udf', 'udf'],
    "id_adventure_oracle_text_l_t": "uc00",
    "id_adventure_oracle_text_l_o": "ubfd",
    "id_adventure_oracle_text_r_t": "ube9",
    "id_adventure_oracle_text_r_o": "ube6",
}
id_general_back = {
    "id_spread": "u2635",
    "id_artwork_o": "u2a41",
    "id_type_o": "u2a40",
    "id_name_t": "u2a2c",
    "id_type_line_t": "u2a15",
    "id_mana_cost_t": "u29fe",
    "id_color_bars_o": ['u29f8', 'u29f6', 'u2812', 'u2811'],
    "id_gradients_o": ['udf', 'udf', 'udf', 'udf'],
    "id_oracle_text_t": "u29c0",
    "id_oracle_text_o": "u29bd",
    "id_mask_o": "u27f4",
    "id_value_t": "u2873",
    "id_value_o": "u2870",
    "id_value_short_frame_o": "u281a",
    "id_value_long_frame_o": "u2813",
    "id_mask_short_o": "u2819",
    "id_mask_long_o": "u27f6",
    "id_bottom_o": "u27f7",
    "id_artist_t": "u2857",
    "id_collector_information_t": "u2824",
    "id_set_o": "u2820",
    "id_group_normal_o": "u27f2",
    "id_group_split_o": "u263b",
    "id_modal_t": "u29de",
    "id_group_modal_o": "u29d5",
    "id_group_oracle_planeswalker_o": "u2903",
    "id_planeswalker_value_t": ['u29a9', 'u297b', 'u294d', 'u291e'],
    "id_planeswalker_value_o": ['u29a6', 'u2978', 'u294a', 'u291b'],
    "id_planeswalker_text_t": ['u2992', 'u2964', 'u2936', 'u2907'],
    "id_planeswalker_text_o": ['u298f', 'u2961', 'u2932', 'u2904'],
    "id_group_oracle_adventure_o": "u2888",
    "id_side_indicator_t": "u2840",
    "id_side_indicator_o": "u2838",
}

# Values
VALUE_MODAL_HEIGHT = 23.822047244094502 - 13.546456692913399
VALUE_DISTANCE_VALUE = 4.960627698522806
VALUE_TOP_PLANESWALKER = -46.204724409448914
VALUE_BOT_PLANESWALKER = 38.83464566929126

# API
api_url = "https://api.scryfall.com"

# Folders
f_preset = "D:/Drive/Creative/Magic/Proxky/Types/General.idml"
f_output = "D:/Games/Magic/Proxky/v1/Documents"
f_artwork = "D:/Games/Magic/Proxky/v1/Artwork"
f_artwork_downloaded = "D:/Games/Magic/Proxky/v1/ArtworkDownload"
f_icon_types = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Card Types"
f_icon_mana = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Mana"
f_icon_set = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Set"

# Enumerations
supported_layouts = ["normal", "modal_dfc", "transform", "split", "adventure", "class", "saga"]

# Types
mana_types = ["W", "U", "B", "R", "G", "C"]
image_types = ["png", "jpg", "jpeg"]

# Mappings
mana_mapping = {
    "{T}": "T",
    "{W}": "W",
    "{U}": "U",
    "{B}": "B",
    "{R}": "R",
    "{G}": "G",
    "{C}": "C",
    "{0}": "0",
    "{1}": "1",
    "{2}": "2",
    "{3}": "3",
    "{4}": "5",
    "{5}": "5",
    "{6}": "6",
    "{7}": "7",
    "{8}": "8",
    "{9}": "9",
    "{10}": "",
    "{X}": "X",
    "{E}": "E",
}
color_mapping = {
    "C": "Magic Grey",
    "W": "Magic White",
    "U": "Magic Blue",
    "B": "Magic Black",
    "R": "Magic Red",
    "G": "Magic Green"
}

# Regex
regex = [
    ([r"({[A-Z0-9]+})+"], "font", ("KyMana", "")),
    ([r"Adamant", "Addendum", "Battalion", "Bloodrush", "Channel", "Chroma", "Cohort", "Constellation", "Converge",
      "Council's dilemma", "Coven", "Delirium", "Domain", "Eminence", "Enrage", "Fateful hour", "Ferocious",
      "Formidable", "Grandeur", "Hellbent", "Heroic", "Imprint", "Join forces", "Kinship", "Landfall", "Lieutenant",
      "Magecraft", "Metalcraft", "Morbid", "Pack tactics", "Parley", "Radiance", "Raid", "Rally", "Revolt",
      "Spell mastery", "Strive", "Sweep", "Tempting offer", "Threshold", "Underdog", "Undergrowth",
      "Will of the council"], "font", ("Plantin MT Pro", "Italic")),
    ([r" ?\(.+\)"], "type", "reminder")
]
regex_planeswalker = [([r"[\+|−]?\d+: "], "type", "loyalty")]
regex_leveler = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"
regex_decklist_id = r"ID: (?P<id>.+)"
regex_decklist = r"^(?P<amount>\d+) (?P<name>.+?)(?: \[(?P<set>.+)\])?$"
