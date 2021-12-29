from initialize import keywords


class ids:
    SPREAD = "id_spread"

    # Groups
    GROUP_NORMAL_O = "id_group_normal_o"
    GROUP_SPLIT_O = "id_group_split_o"
    GROUP_HEADER_O = "id_group_header_o"
    GROUP_BODY_O = "id_group_body_o"
    GROUP_PLANESWALKER_O = "id_group_planeswalker_o"
    GROUP_ADVENTURE_O = "id_group_adventure_o"
    GROUP_FOOTER_O = "id_group_footer_o"

    # Misc
    GRADIENTS_O = "id_gradients_o"

    # Header
    TYPE_ICON_O = "id_type_icon_o"
    TITLE_T = "id_title_t"
    TYPE_LINE_T = "id_type_line_t"
    MANA_COST_T = "id_mana_cost_t"
    COLOR_INDICATOR_TOP_O = "id_color_indicator_top_o"

    # Body
    MODAL_T = "id_modal_t"
    ORACLE_T = "id_oracle_t"
    ORACLE_O = "id_oracle_o"

    # Planeswalker
    PLANESWALKER_VALUE_T = "id_planeswalker_value_t"
    PLANESWALKER_VALUE_O = "id_planeswalker_value_o"
    PLANESWALKER_ORACLE_NUMBERED_T = "id_planeswalker_oracle_numbered_t"
    PLANESWALKER_ORACLE_NUMBERED_O = "id_planeswalker_oracle_numbered_o"
    PLANESWALKER_ORACLE_FINAL_T = "id_planeswalker_oracle_final_t"
    PLANESWALKER_ORACLE_FINAL_O = "id_planeswalker_oracle_final_o"

    # Adventure
    ADVENTURE_ORACLE_LEFT_T = "id_adventure_oracle_left_t"
    ADVENTURE_ORACLE_LEFT_O = "id_adventure_oracle_left_o"
    ADVENTURE_ORACLE_RIGHT_T = "id_adventure_oracle_right_t"
    ADVENTURE_ORACLE_RIGHT_O = "id_adventure_oracle_right_o"

    # Footer
    VALUE_T = "id_value_t"
    VALUE_O = "id_value_o"
    COLOR_INDICATOR_BOT_O = "id_color_indicator_bot_o"
    ARTIST_T = "id_artist_t"
    COLLECTOR_INFORMATION_T = "id_collector_information_t"

    # Artwork
    BACKDROP_O = "id_backdrop_o"
    ARTWORK_O = "id_artwork_o"

    PRINTING_FRAME_O = "pid_frame_o"


class id_names:
    # Groups
    GROUP_NORMAL = "Normal"
    GROUP_SPLIT = "Split"
    GROUP_SPLIT_TOP = "Split Top"
    GROUP_SPLIT_BOT = "Split Bot"
    GROUP_HEADER = "Header"
    GROUP_PLANESWALKER = "Layout Planeswalker"
    GROUP_ADVENTURE = "Layout Adventure"

    # Header
    TYPE_ICON = "Type Icon"
    TITLE = "Title"
    TYPE_LINE = "Type Line"
    MANA_COST = "Mana Cost"
    COLOR_INDICATOR_TOP = "Color Indicator Top"

    # Body
    MODAL = "Modal"
    ORACLE = "Oracle"

    # Planeswalker
    PLANESWALKER_VALUE_1 = "Planeswalker Value 1"
    PLANESWALKER_VALUE_2 = "Planeswalker Value 2"
    PLANESWALKER_VALUE_3 = "Planeswalker Value 3"
    PLANESWALKER_VALUE_4 = "Planeswalker Value 4"
    PLANESWALKER_ORACLE_1 = "Planeswalker Oracle 1"
    PLANESWALKER_ORACLE_2 = "Planeswalker Oracle 2"
    PLANESWALKER_ORACLE_3 = "Planeswalker Oracle 3"
    PLANESWALKER_ORACLE_4 = "Planeswalker Oracle 4"
    PLANESWALKER_ORACLE_FINAL = "Planeswalker Oracle"

    # Adventure
    ADVENTURE_TYPE_ICON = "Adventure Type Icon"
    ADVENTURE_TITLE = "Adventure Title"
    ADVENTURE_TYPE_LINE = "Adventure Type Line"
    ADVENTURE_MANA_COST = "Adventure Mana Cost"
    ADVENTURE_COLOR_INDICATOR = "Adventure Color Indicator"
    ADVENTURE_ORACLE_LEFT = "Adventure Oracle Left"
    ADVENTURE_ORACLE_RIGHT = "Adventure Oracle Right"

    # Footer
    VALUE = "Value"
    COLOR_INDICATOR_BOT = "Color Indicator Bot"
    ARTIST_INFORMATION = "Artist Information"
    COLLECTOR_INFORMATION = "Collector Information"

    # Split
    ST_ORACLE = "ST Oracle"
    ST_ARTIST_INFORMATION = "ST Artist Information"
    ST_COLLECTOR_INFORMATION = "ST Collector Information"

    SB_ORACLE = "SB Oracle"
    SB_ARTIST_INFORMATION = "SB Artist Information"
    SB_COLLECTOR_INFORMATION = "SB Collector Information"

    BACKDROP = "Backdrop"
    ARTWORK = "Artwork"

    # Printing
    P_FRAME = "Frame"


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


# IDs
id_general_front = {
    "id_spread": "uce",
    "id_group_header_o": "u3f9",
    "id_type_icon_o": "u17b",
    "id_title_t": "u158",
    "id_type_line_t": "u1c1",
    "id_mana_cost_t": "u1a7",
    "id_color_indicator_top_o": "u2ed",
    "id_gradients_o": ['u105f', 'u1061'],
    "id_oracle_t": "u1da",
    "id_oracle_o": "u1ec",
    "id_color_indicator_bot_o": "u204",
    "id_value_t": "u23f",
    "id_value_o": "u251",
    "id_artist_t": "u20c",
    "id_collector_information_t": "u229",
    "id_artwork_o": "u14d",
    "id_backdrop_o": "u12f5",
    "id_group_planeswalker_o": "u4ea",
    "id_group_adventure_o": "u3db",
    "id_modal_t": "u3fe",
    "id_planeswalker_value_t": ['u41b', 'u469', 'u497', 'u4ca'],
    "id_planeswalker_value_o": ['u42d', 'u466', 'u494', 'u4c7'],
    "id_planeswalker_oracle_numbered_t": ['u436', 'u452', 'u480', 'u4b3'],
    "id_planeswalker_oracle_numbered_o": ['u432', 'u44f', 'u47d', 'u4b0'],
    "id_planeswalker_oracle_final_t": "u4ef",
    "id_planeswalker_oracle_final_o": "u4ec",
}
id_general_split_top_front = {
    "id_spread": "uce",
    "id_group_header_o": "u16ef",
    "id_type_icon_o": "u1736",
    "id_title_t": "u1722",
    "id_type_line_t": "u170b",
    "id_mana_cost_t": "u16f4",
    "id_color_indicator_top_o": "u16f0",
    "id_gradients_o": ['u1055', 'u1057'],
    "id_oracle_t": "u16c4",
    "id_oracle_o": "u16c1",
    "id_color_indicator_bot_o": "u1560",
    "id_value_t": "u1564",
    "id_value_o": "u1561",
    "id_artist_t": "u154c",
    "id_collector_information_t": "u1535",
    "id_artwork_o": "u152f",
    "id_backdrop_o": "u1530",
}
id_general_split_bot_front = {
    "id_spread": "uce",
    "id_group_header_o": "u17e2",
    "id_type_icon_o": "u182a",
    "id_title_t": "u1816",
    "id_type_line_t": "u17fe",
    "id_mana_cost_t": "u17e7",
    "id_color_indicator_top_o": "u17e3",
    "id_gradients_o": ['u1055', 'u1057'],
    "id_oracle_t": "u17b7",
    "id_oracle_o": "u17b4",
    "id_color_indicator_bot_o": "u179b",
    "id_value_t": "u179f",
    "id_value_o": "u179c",
    "id_artist_t": "u1787",
    "id_collector_information_t": "u1770",
    "id_artwork_o": "u176a",
    "id_backdrop_o": "u176b",
}
id_general_front_adventure = {
    "id_spread": "uce",
    "id_type_icon_o": "u3d8",
    "id_title_t": "u3c4",
    "id_type_line_t": "u3ad",
    "id_mana_cost_t": "u396",
    "id_color_indicator_top_o": "u3df",
    "id_gradients_o": "Black",
    "id_adventure_oracle_left_t": "u1065",
    "id_adventure_oracle_left_o": "u1062",
    "id_adventure_oracle_right_t": "u107e",
    "id_adventure_oracle_right_o": "u107b",
}
id_general_back = {
    "id_spread": "u1837",
    "id_group_header_o": "u1b88",
    "id_type_icon_o": "u1bd0",
    "id_title_t": "u1bbc",
    "id_type_line_t": "u1ba4",
    "id_mana_cost_t": "u1b8d",
    "id_color_indicator_top_o": "u1b89",
    "id_gradients_o": ['u1055', 'u1057'],
    "id_oracle_t": "u1b5d",
    "id_oracle_o": "u1b5a",
    "id_color_indicator_bot_o": "u19fa",
    "id_value_t": "u19fe",
    "id_value_o": "u19fb",
    "id_artist_t": "u19e6",
    "id_collector_information_t": "u19cf",
    "id_artwork_o": "u19c9",
    "id_backdrop_o": "u19ca",
    "id_group_planeswalker_o": "u1a8a",
    "id_group_adventure_o": "u1a13",
    "id_modal_t": "u1b74",
    "id_planeswalker_value_t": ['u1b46', 'u1b18', 'u1aea', 'u1abc'],
    "id_planeswalker_value_o": ['u1b43', 'u1b15', 'u1ae7', 'u1ab9'],
    "id_planeswalker_oracle_numbered_t": ['u1b2f', 'u1b01', 'u1ad3', 'u1aa5'],
    "id_planeswalker_oracle_numbered_o": ['u1b2c', 'u1afe', 'u1ad0', 'u1aa2'],
    "id_planeswalker_oracle_final_t": "u1a8e",
    "id_planeswalker_oracle_final_o": "u1a8b",
}
id_general_print_front = {
    "id_spread": "ue7",
    "pid_frame_o": ['uf5', 'u114', 'u115', 'u119', 'u118', 'u117', 'u11c', 'u11b', 'u11a'],
}
id_general_print_back = {
    "id_spread": "u11d",
    "pid_frame_o": ['u12c', 'u12b', 'u12a', 'u129', 'u127', 'u126', 'u125', 'u124', 'u123'],
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
VALUE_SHIFT_ARTWORK_FULL_BODY = abs(10.204724409448769 - 139.03937007874012)

# Font
FONT_STANDARD = "Plantin MT Pro"
FONT_STANDARD_STYLE_ITALIC = "Italic"
FONT_SANS = "Helvetica Now Var"
FONT_SANS_STYLE = "Display"

# Folders
f_main = "D:/Games/Magic/Proxky/v2"

file_template = f_main + "/Resources/Templates/Proxky.idml"
file_print = f_main + "/Resources/Templates/Print.idml"

f_icon_card_types = f_main + "/Resources/Icons/Card Types"
f_documents = f_main + "/Documents"
f_pdf = f_main + "/PDF"
f_print = f_main + "/Print"
f_artwork = f_main + "/Artwork"
f_artwork_downloaded = f_main + "/Artwork Downloaded"

# Enumerations
supported_layouts = ["normal"]  # , "modal_dfc", "transform", "split", "adventure", "class", "saga", "meld",
# "token", "double_faced_token", "emblem"]
double_faced_layouts = ["modal_dfc", "transform", "meld", "double_faced_token"]

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
regex_template_flavor = [([r"\*(?:.)+\*"], "type", "normal")]

regex_leveler = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"
regex_newline = r"\n"

regex_card_entry = r"^(?P<amount>\d+) (?P<name>.+?)(?P<flags> \[.+\])?$"
regex_card_options = r"(?P<type>(?:.)+): (?P<id>(?:.)+)"
regex_card_name = r"^(?P<set>.+) - (?P<name>.+?)$"

# Text Frame Resizing Array, AT LEAST ONE OF EACH ARRAYS MUST CONTAIN MORE THAN ONE ELEMENT
resize_array = [
    # Text Frames to Resize
    [
        [id_names.ORACLE],
        [id_names.PLANESWALKER_ORACLE_1, id_names.PLANESWALKER_ORACLE_2,
         id_names.PLANESWALKER_ORACLE_3, id_names.PLANESWALKER_ORACLE_4],
        [id_names.PLANESWALKER_ORACLE_FINAL],
        [id_names.ST_ORACLE],
        [id_names.SB_ORACLE],
        ["Placeholder", "Placeholder"]
    ],
    # Text Frames to Condense
    [
        [id_names.ARTIST_INFORMATION, id_names.ARTIST_INFORMATION],
        [id_names.COLLECTOR_INFORMATION],
        [id_names.ST_ARTIST_INFORMATION],
        [id_names.ST_COLLECTOR_INFORMATION],
        [id_names.SB_ARTIST_INFORMATION],
        [id_names.SB_COLLECTOR_INFORMATION],
        ["Placeholder", "Placeholder"]
    ]
]
