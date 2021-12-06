from initialize import keywords


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
    GROUP_HEADER_O = "id_group_header_o"
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
    PLANESWALKER_ORACLE_T = "id_planeswalker_oracle_t"
    PLANESWALKER_ORACLE_O = "id_planeswalker_oracle_o"
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
    PRINTING_FRAME_O = "pid_frame_o"


class tf_names:
    ORACLE_TEXT = "Oracle Text"
    PLANESWALKER_TEXT_1 = "Planeswalker Text 1"
    PLANESWALKER_TEXT_2 = "Planeswalker Text 2"
    PLANESWALKER_TEXT_3 = "Planeswalker Text 3"
    PLANESWALKER_TEXT_4 = "Planeswalker Text 4"
    PLANESWALKER_ORACLE_TEXT = "Planeswalker Oracle Text"
    ADVENTURE_ORACLE_TEXT_LEFT = "Adventure Oracle Text Left"
    ADVENTURE_ORACLE_TEXT_RIGHT = "Adventure Oracle Text Right"
    ARTIST = "Artist"
    COLLECTOR_INFORMATION = "Collector Information"

    ST_ORACLE_TEXT = "ST Oracle Text"
    ST_ARTIST = "ST Artist"
    ST_COLLECTOR_INFORMATION = "ST Collector Information"

    SB_ORACLE_TEXT = "SB Oracle Text"
    SB_ARTIST = "SB Artist"
    SB_COLLECTOR_INFORMATION = "SB Collector Information"


# IDs
id_general_front = {
    "id_spread": "uff",
    "id_artwork_o": "u2e6",
    "id_group_header_o": "u273",
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
    "id_planeswalker_oracle_t": "u342c",
    "id_planeswalker_oracle_o": "u3429",
    "id_group_oracle_adventure_o": "ub82",
    "id_side_indicator_t": "u160",
    "id_side_indicator_o": "u153",
}
id_general_front_st = {
    "id_spread": "uff",
    "id_artwork_o": "u18f4",
    "id_group_header_o": "u1886",
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
    "id_group_header_o": "u1c81",
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
    "id_spread": "u4ba2",
    "id_artwork_o": "u4fc3",
    "id_group_header_o": "u4f56",
    "id_type_o": "u4fc2",
    "id_name_t": "u4fae",
    "id_type_line_t": "u4f97",
    "id_mana_cost_t": "u4f7f",
    "id_color_bars_o": ['u4f79', 'u4f78', 'u4d7e', 'u4d7d'],
    "id_gradients_o": ['udf', 'udf', 'udf', 'udf'],
    "id_oracle_text_t": "u4f42",
    "id_oracle_text_o": "u4f3f",
    "id_mask_o": "u4d61",
    "id_value_t": "u4ddf",
    "id_value_o": "u4ddc",
    "id_value_short_frame_o": "u4d85",
    "id_value_long_frame_o": "u4d7f",
    "id_mask_short_o": "u4d84",
    "id_mask_long_o": "u4d63",
    "id_bottom_o": "u4d64",
    "id_artist_t": "u4dc3",
    "id_collector_information_t": "u4d90",
    "id_set_o": "u4d8b",
    "id_group_normal_o": "u4d5f",
    "id_group_split_o": "u4ba8",
    "id_modal_t": "u4f60",
    "id_group_modal_o": "u4f57",
    "id_group_oracle_planeswalker_o": "u4e6e",
    "id_planeswalker_value_t": ['u4f2b', 'u4efd', 'u4ecf', 'u4ea1'],
    "id_planeswalker_value_o": ['u4f28', 'u4efa', 'u4ecc', 'u4e9e'],
    "id_planeswalker_text_t": ['u4f14', 'u4ee6', 'u4eb8', 'u4e8a'],
    "id_planeswalker_text_o": ['u4f11', 'u4ee3', 'u4eb5', 'u4e86'],
    "id_planeswalker_oracle_t": "u4e72",
    "id_planeswalker_oracle_o": "u4e6f",
    "id_group_oracle_adventure_o": "u4df4",
    "id_side_indicator_t": "u4dac",
    "id_side_indicator_o": "u4da4",
}
id_general_print_front = {
    "id_spread": "uce",
    "pid_frame_o": ['u3ca', 'u3d6', 'u3d8', 'u3d9', 'u3da', 'u3db', 'u3dc', 'u3dd', 'u3de'],
}
id_general_print_back = {
    "id_spread": "u20b",
    "pid_frame_o": ['u497', 'u496', 'u495', 'u494', 'u493', 'u492', 'u491', 'u490', 'u48e'],
}

# Flags
FLAG_OK = 0
FLAG_FILE_NOT_FOUND = 11000
FLAG_FILE_EXISTS = 11001
FLAG_PREFLIGHT_FAIL = 12000

# Values
VALUE_MODAL_HEIGHT = 23.822047244094502 - 13.546456692913399
VALUE_DISTANCE_VALUE = 4.960627698522806  # Distance how much the value panel extends over the bottom color line
COORDINATE_TOP_ORACLE_TEXT = -47.905511811023686 \
                             + 0  # Top coordinate of the oracle box, note not necessarily same for all boxes shifting
COORDINATE_BOT_ORACLE_TEXT = 37.13385826771649
VALUE_SHIFT_HEADER_TOKEN_WITH_VALUE = 80.50393700787403 + abs(
    -1.559055118110237)  # How much to shift the header for a token that has a power toughness value
VALUE_SHIFT_ARTWORK_TOKEN_WITH_VALUE = abs(-200.6929133858268) - abs(-118.62992125984258)
VALUE_SHIFT_TOKEN_NO_VALUE = abs(-210.6141732283465) - abs(
    -200.6929133858268)  # How much to shift for a token without a value

# Font
FONT_STANDARD = "Plantin MT Pro"
FONT_STANDARD_STYLE_ITALIC = "Italic"
FONT_SANS = "Helvetica Now Var"
FONT_SANS_STYLE = "Display"

# Folders
f_preset_folder = "D:/Drive/Creative/Magic/Proxky"
f_output_folder = "D:/Games/Magic/Proxky/v1/"

f_preset = f_preset_folder + "/Types/General.idml"
f_preset_print = f_preset_folder + "/Types/Printing.idml"
f_icon_types = f_preset_folder + "/Resource/Icons/Card Types"
f_icon_mana = f_preset_folder + "/Resource/Icons/Mana"
f_icon_set = f_preset_folder + "/Resource/Icons/Set"

f_documents = f_output_folder + "/Documents"
f_pdf = f_output_folder + "/PDF"
f_print = f_output_folder + "/Other/Print"
f_artwork = f_output_folder + "/Artwork"
f_artwork_downloaded = f_output_folder + "/ArtworkDownload"

# Enumerations
supported_layouts = ["normal", "modal_dfc", "transform", "split", "adventure", "class", "saga", "token",
                     "double_faced_token"]

# Types
mana_types = ["W", "U", "B", "R", "G", "C"]
image_types = ["png", "jpg", "jpeg"]

# Mappings
mana_mapping = {
    "{T}": "T",
    "{W}": "W",
    "{W/U}": "",
    "{W/B}": "",
    "{W/P}": "",
    "{2/W}": "",
    "{U}": "U",
    "{U/B}": "",
    "{U/R}": "",
    "{U/P}": "",
    "{2/U}": "",
    "{B}": "B",
    "{B/R}": "",
    "{B/G}": "",
    "{B/P}": "",
    "{2/B}": "",
    "{R}": "R",
    "{R/G}": "",
    "{R/W}": "",
    "{R/P}": "",
    "{2/R}": "",
    "{G}": "G",
    "{G/W}": "",
    "{G/U}": "",
    "{G/P}": "",
    "{2/G}": "",
    "{C}": "C",
    "{P}": "P",
    "{0}": "0",
    "{1}": "1",
    "{2}": "2",
    "{3}": "3",
    "{4}": "4",
    "{5}": "5",
    "{6}": "6",
    "{7}": "7",
    "{8}": "8",
    "{9}": "9",
    "{10}": "",
    "{11}": "",
    "{12}": "",
    "{13}": "",
    "{14}": "",
    "{15}": "",
    "{16}": "",
    "{17}": "",
    "{18}": "",
    "{19}": "",
    "{20}": "",
    "{S}": "S",
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
regex_mana = r"(?P<match>{(?P<mana>[A-Z0-9\/]+)})"
regex_add_mana = r"(?P<match>(?P<req>(?:{[A-Z0-9\/]+})+)+: Add (?P<prod>(?:{(?:[A-Z0-9\/]+)})+))"

regex_template_mana = [([regex_mana], "font", ("KyMana", ""))]
regex_template_regular = regex_template_mana.copy()
regex_template_regular.append(
    ([r" ?\(.+\)"], "type", "reminder"))
regex_template_oracle = regex_template_regular.copy()
regex_template_oracle.append(
    (keywords, "font", ("Plantin MT Pro", "Italic")))
regex_template_planeswalker = [([r"[\+|−]?(?:\d+|X): "], "type", "loyalty")]

regex_leveler = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"
regex_newline = r"\n"
regex_decklist_id = r"^(?P<amount>\d+) (?P<name>.+?)(?: \[(ID: (?P<id>.+))\])$"
regex_decklist = r"^(?P<amount>\d+) (?P<name>.+?)(?: \[(?P<set>.+)\])?$"

# Text Frame Resizing Array, AT LEAST ONE OF EACH ARRAYS MUST CONTAIN MORE THAN ONE ELEMENT
resize_array = [
    # Text Frames to Resize
    [
        [tf_names.ORACLE_TEXT],
        [tf_names.PLANESWALKER_TEXT_1, tf_names.PLANESWALKER_TEXT_2,
         tf_names.PLANESWALKER_TEXT_3, tf_names.PLANESWALKER_TEXT_4],
        [tf_names.PLANESWALKER_ORACLE_TEXT],
        [tf_names.ST_ORACLE_TEXT],
        [tf_names.SB_ORACLE_TEXT],
        ["Placeholder", "Placeholder"]
    ],
    # Text Frames to Condense
    [
        [tf_names.ARTIST, tf_names.ARTIST],
        [tf_names.COLLECTOR_INFORMATION],
        [tf_names.ST_ARTIST],
        [tf_names.ST_COLLECTOR_INFORMATION],
        [tf_names.SB_ARTIST],
        [tf_names.SB_COLLECTOR_INFORMATION],
        ["Placeholder", "Placeholder"]
    ]
]
