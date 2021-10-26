import copy
import json
import math
import os
import re
import shutil
import time
import urllib.parse
import xml.etree.ElementTree
import zipfile
from time import sleep
from PIL import Image  # Pillow

import requests

from card import Card


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
    GROUP_ORACLE_PLANESWALKER_O = "id_group_oracle_planeswalker_o"
    PLANESWALKER_VALUE_T = "id_planeswalker_value_t"
    PLANESWALKER_VALUE_O = "id_planeswalker_value_o"
    PLANESWALKER_TEXT_T = "id_planeswalker_text_t"
    PLANESWALKER_TEXT_O = "id_planeswalker_text_o"
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


MODAL_HEIGHT = 23.822047244094502 - 13.546456692913399

# API
api_url = "https://api.scryfall.com"

# Folders
f_preset = "D:/Drive/Creative/Magic/Proxky/Types/General.idml"
f_output = "D:/Games/Magic/Proxky/v1/Documents/Test"
f_artwork = "D:/Games/Magic/Proxky/v1/Artwork"
f_artwork_downloaded = "D:/Games/Magic/Proxky/v1/ArtworkDownload"
f_icon_types = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Card Types"
f_icon_mana = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Mana"
f_icon_set = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Set"

# Enumerations
supported_layouts = ["normal", "modal_dfc", "transform", "class", "saga"]
id_general_front = {
"id_spread": "uff",
"id_artwork_o": "u2e6",
"id_type_o": "u2e5",
"id_name_t": "u2d0",
"id_type_line_t": "u2ba",
"id_mana_cost_t": "u2a4",
"id_modal_t": "u281",
"id_group_modal_o": "u274",
"id_color_bars_o": ['u2a0', 'u29f', 'u122', 'u121'],
"id_gradients_o": ['ue1', 'ue3', 'ue2', 'ue4'],
"id_oracle_text_t": "u25e",
"id_oracle_text_o": "u270",
"id_group_oracle_planeswalker_o": "u1ac",
"id_planeswalker_value_t": ['u248', 'u21c', 'u1f0', 'u1c4'],
"id_planeswalker_value_o": ['u25a', 'u22e', 'u202', 'u1d6'],
"id_planeswalker_text_t": ['u232', 'u206', 'u1da', 'u1ae'],
"id_planeswalker_text_o": ['u244', 'u218', 'u1ec', 'u1c0'],
"id_mask_o": "u106",
"id_value_t": "u196",
"id_value_o": "u1a8",
"id_value_short_frame_o": "u130",
"id_value_long_frame_o": "u123",
"id_mask_short_o": "u12f",
"id_mask_long_o": "u108",
"id_bottom_o": "u109",
"id_artist_t": "u176",
"id_side_indicator_t": "u160",
"id_side_indicator_o": "u153",
"id_collector_information_t": "u13e",
"id_set_o": "u13c",
}
id_general_back = {
"id_spread": "u96e",
"id_artwork_o": "ub43",
"id_type_o": "ub42",
"id_name_t": "ub2e",
"id_type_line_t": "ub17",
"id_mana_cost_t": "uaff",
"id_modal_t": "uae0",
"id_group_modal_o": "uad7",
"id_color_bars_o": ['uaf9', 'uaf8', 'u992', 'u991'],
"id_gradients_o": ['udf', 'udf', 'udf', 'udf'],
"id_oracle_text_t": "uac2",
"id_oracle_text_o": "uabf",
"id_group_oracle_planeswalker_o": "ua05",
"id_planeswalker_value_t": ['uaab', 'ua7d', 'ua4f', 'ua21'],
"id_planeswalker_value_o": ['uaa8', 'ua7a', 'ua4c', 'ua1e'],
"id_planeswalker_text_t": ['ua94', 'ua66', 'ua38', 'ua0a'],
"id_planeswalker_text_o": ['ua91', 'ua63', 'ua35', 'ua06'],
"id_mask_o": "u975",
"id_value_t": "u9f0",
"id_value_o": "u9ed",
"id_value_short_frame_o": "u999",
"id_value_long_frame_o": "u993",
"id_mask_short_o": "u998",
"id_mask_long_o": "u977",
"id_bottom_o": "u978",
"id_artist_t": "u9d6",
"id_side_indicator_t": "u9bf",
"id_side_indicator_o": "u9b6",
"id_collector_information_t": "u9a2",
"id_set_o": "u99e",
}

mana_types = ["W", "U", "B", "R", "G", "C"]
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
image_types = ["png", "jpg", "jpeg"]

# Other
regex = [
    (["({[A-Z0-9]+})+"], "font", ("KyMana", "")),
    (["Adamant", "Addendum", "Battalion", "Bloodrush", "Channel", "Chroma", "Cohort", "Constellation", "Converge",
      "Council's dilemma", "Coven", "Delirium", "Domain", "Eminence", "Enrage", "Fateful hour", "Ferocious",
      "Formidable", "Grandeur", "Hellbent", "Heroic", "Imprint", "Join forces", "Kinship", "Landfall", "Lieutenant",
      "Magecraft", "Metalcraft", "Morbid", "Pack tactics", "Parley", "Radiance", "Raid", "Rally", "Revolt",
      "Spell mastery", "Strive", "Sweep", "Tempting offer", "Threshold", "Underdog", "Undergrowth",
      "Will of the council"], "font", ("Plantin MT Pro", "Italic")),
    ([" ?\(.+\)"], "type", "reminder")
]
regex_planeswalker = [(["[\+|−]?\d+: "], "type", "loyalty")]
regex_leveler = r"[\"LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)\"]"


def process_cards(card_names: list[(str, str)]):
    for i, card_name in enumerate(card_names):
        start_time = time.time()

        response = requests.get(
            api_url + "/cards/named?exact=" + urllib.parse.quote(card_name[0]) + "&set=" + urllib.parse.quote(
                card_name[1]))

        # Check status code
        if response.status_code != 200:
            info_fail(card_name[0], "Could not fetch card")
            continue

        card = Card(json.loads(response.text))
        if process_card(card):
            info_success(card_name[0], "Successfully processed card")

        end_time = time.time()
        if (end_time - start_time) * 1000 < 100 and i < len(card_names) - 1:
            sleep(0.1)


def process_card(card: Card):
    # Check layout of card
    if card.layout not in supported_layouts:
        info_fail(card.name, "Layout not supported")
        return False

    # Cleansed cardname for saving file
    cleansed_name = card.name.replace("//", "--")

    # Folders
    target_folder_path = f_output + "/" + card.set.upper()
    target_file_path = target_folder_path + "/" + cleansed_name
    target_file_full_path = target_file_path + ".idml"

    # Setup and extract preset
    os.makedirs(target_folder_path, exist_ok=True)
    with zipfile.ZipFile(f_preset, "r") as archive:
        archive.extractall("data/memory")

    if card.layout in ["normal", "class", "saga"]:
        card_fill(card, id_general_front)
        card_delete_backside(id_general_back)
    elif card.layout in ["modal_dfc", "transform"]:
        card_layout_double_faced([id_general_front, id_general_back])
        set_modal(card, [id_general_front, id_general_back], card.layout)
        card_fill(card.card_faces[0], id_general_front)
        card_fill(card.card_faces[1], id_general_back)


    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    if helper_file_exists(target_file_full_path):
        os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    # Remove files from working memory
    # shutil.rmtree("data/memory")
    return True


def card_fill(card: Card, id_set):
    types = helper_get_card_types(card)

    if "Planeswalker" in types:
        card_layout_planeswalker(id_set)
        if card.loyalty == "":
            card_layout_no_value(id_set)
    elif card.power == "" and card.toughness == "":
        card_layout_no_value(id_set)

    # Artwork
    set_artwork(card, id_set)

    # Type Icon
    set_type_icon(card, id_set)

    # Card Name
    set_card_name(card, id_set)

    # Type Line
    set_type_line(card, id_set)

    # Mana Cost
    set_mana_cost(card, id_set)

    # Color Bar
    set_color_bar(card, id_set)

    # Oracle Text
    if "Planeswalker" in types:
        set_planeswalker_text(card, id_set)
    else:
        set_default_oracle_text(card, id_set)

    # Value
    set_value(card, id_set)

    # Artist
    set_artist(card, id_set)

    # Collector Information
    set_collector_information(card, id_set)

    # Set
    set_set(card, id_set)


##############
### LAYOUT ###
##############

def card_layout_double_faced(id_sets):
    for i, id_set in enumerate(id_sets):
        tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
        modal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_MODAL_O] + "']")
        modal.set("Visible", "true")

        shift_by = MODAL_HEIGHT

        color_bars = [tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][0] + "']"),
                      tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][1] + "']")]

        for color_bar in color_bars:
            coordinates = color_bar.attrib["ItemTransform"].split(" ")
            color_bar.set("ItemTransform",
                          coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
                          coordinates[4] + " " + str(float(coordinates[5]) + shift_by))

        oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")

        helper_indesign_shift_y_coordinates(oracle_text, [shift_by, shift_by, 0, 0])

        side_indicator_o = tree.find(".//Group[@Self='" + id_set[ids.SIDE_INDICATOR_O] + "']")
        side_indicator_o.set("Visible", "true")

        if i == 0:
            insert_value_content(id_set[ids.SIDE_INDICATOR_T], "FRONT")
        elif i == 1:
            insert_value_content(id_set[ids.SIDE_INDICATOR_T], "BACK")

        tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_planeswalker(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Show value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "true")

    # Show Planeswalker
    oracle_planeswalker = tree.find(".//Group[@Self='" + id_set[ids.GROUP_ORACLE_PLANESWALKER_O] + "']")
    oracle_planeswalker.set("Visible", "true")

    value_short_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_SHORT_FRAME_O] + "']")
    value_short_frame.set("Visible", "true")
    value_long_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_LONG_FRAME_O] + "']")
    value_long_frame.set("Visible", "false")

    # Change Mask
    mask = tree.find(".//Group[@Self='" + id_set[ids.MASK_O] + "']")
    bottom = tree.find(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']")
    mask_short = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_SHORT_O] + "']")
    mask_long = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_LONG_O] + "']")

    for child in mask.findall("./Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask.remove(child)
    for child in mask_long.findall("./Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_long.remove(child)

    mask_short.append(bottom)

    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")
    oracle_text.set("Visible", "false")

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_layout_no_value(id_set):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    # Hide value
    value_text = tree.find(".//TextFrame[@Self='" + id_set[ids.VALUE_O] + "']")
    value_text.set("Visible", "false")

    value_short_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_SHORT_FRAME_O] + "']")
    value_short_frame.set("Visible", "false")
    value_long_frame = tree.find(".//Rectangle[@Self='" + id_set[ids.VALUE_LONG_FRAME_O] + "']")
    value_long_frame.set("Visible", "false")

    # Remove Mask
    mask = tree.find(".//Group[@Self='" + id_set[ids.MASK_O] + "']")
    bottom = tree.find(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']")
    mask_short = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_SHORT_O] + "']")
    mask_long = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_LONG_O] + "']")

    mask.append(bottom)

    for child in mask_short.findall(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_short.remove(child)
    for child in mask_long.findall(".//Group[@Self='" + id_set[ids.GROUP_BOTTOM_O] + "']"):
        mask_long.remove(child)

    # Expand Oracle Text Box
    oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")

    shift_by = 42.0944859662393 - 37.13385826771649

    bottom_left = oracle_text.find(".//PathPointType[2]")
    bottom_right = oracle_text.find(".//PathPointType[3]")

    for point in [bottom_left, bottom_right]:
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        point.attrib.pop("Anchor")
        point.attrib.pop("LeftDirection")
        point.attrib.pop("RightDirection")

        coordinates = x_coordinate + " " + str(float(y_coordinate) + shift_by)
        point.set("Anchor", coordinates)
        point.set("LeftDirection", coordinates)
        point.set("RightDirection", coordinates)

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def card_delete_backside(id_set):
    os.remove("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    tree = xml.etree.ElementTree.parse("data/memory/designmap.xml")
    element = tree.getroot().find(".//*[@src='Spreads/Spread_" + id_set[ids.SPREAD] + ".xml']")
    tree.getroot().remove(element)

    with open("data/memory/designmap.xml", "wb") as file:
        file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        file.write(b'<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.4(55)" ?>')
        tree.write(file, xml_declaration=False, encoding="utf-8")


########################
### CARD INFORMATION ###
########################


def set_artwork(card, id_set):
    id_spread = id_set[ids.SPREAD]
    id_artwork = id_set[ids.ARTWORK_O]

    path = f_artwork + "/" + card.set.upper() + "/" + card.name
    path_auto = f_artwork_downloaded + "/" + card.set.upper() + "/" + card.name + ".jpg"
    image_type = "na"

    for possible_image_type in image_types:
        if not helper_file_exists(path + "." + possible_image_type):
            continue
        else:
            image_type = possible_image_type

    if image_type == "na":
        info_warn(card.name, "No artwork exists, using Scryfall source")

        if "art_crop" not in card.image_uris:
            info_fail("No artwork on Scryfall")
            return

        response = requests.get(card.image_uris["art_crop"])

        if response.status_code != 200:
            info_fail(card.name, "Could not download artwork")
            return

        os.makedirs(f_artwork_downloaded + "/" + card.set.upper(), exist_ok=True)
        with open(path_auto, "wb") as handler:
            handler.write(response.content)
        insert_graphic(card, id_spread, id_artwork, f_artwork_downloaded + "/" + card.set.upper(), card.name,
                       type_file="jpg",
                       mode_scale_image="fit_priority_x", mode_align_vertical="top")
    else:
        insert_graphic(card, id_spread, id_artwork, f_artwork + "/" + card.set.upper(), card.name, type_file=image_type,
                       mode_scale_image="fit_priority_x", mode_align_vertical="top")


def set_type_icon(card, id_set):
    id_spread = id_set[ids.SPREAD]
    id_type = id_set[ids.TYPE_O]

    # Get types of card
    types = helper_get_card_types(card)
    if "Legendary" in types:
        types.remove("Legendary")

    if len(types) > 1:
        card_type = "Multiple"
    else:
        card_type = types[0]

    if not helper_file_exists(f_icon_types + "/" + card_type.lower() + ".svg"):
        info_warn(card.name, "No icon for card type")
    else:
        insert_graphic(card, id_spread, id_type, f_icon_types, card_type.lower())


def set_card_name(card, id_set):
    id_name = id_set[ids.NAME_T]

    insert_value_content(id_name, card.name)


def set_type_line(card, id_set):
    id_type_line = id_set[ids.TYPE_LINE_T]

    insert_value_content(id_type_line, card.type_line.replace("—", "•"))


def set_mana_cost(card, id_set):
    id_mana_cost = id_set[ids.MANA_COST_T]

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mapping = "".join([mana_mapping["{" + m + "}"] for m in mana])
    if len(mapping) > 5:
        mapping = mapping[:5] + "\n" + mapping[5:]
    insert_value_content(id_mana_cost, mapping)


def set_modal(card, id_sets, modal_type="modal"):
    for i, id_set in enumerate(id_sets):
        face = card.card_faces[(i + 1) % 2]

        caps_type = ""

        if modal_type == "modal_dfc":
            caps_type = "MODAL"
        elif modal_type == "transform":
            caps_type = "TRANSFORM"

        insert_value_content(id_set[ids.MODAL_T], caps_type + " — " + face.type_line.replace("—", "•"))


def set_color_bar(card, id_set):
    id_gradients = id_set[ids.GRADIENTS_O]

    distance = 1.5
    colors_to_apply = card.colors

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    helper_sort_mana_array(colors_to_apply)

    for id_gradient in id_gradients:
        tree = xml.etree.ElementTree.parse("data/memory/Resources/Graphic.xml")
        element = tree.find(".//Gradient[@Self='Gradient/" + id_gradient + "']")

        for gradient_stop in element.findall(".//GradientStop"):
            element.remove(gradient_stop)

        for i, color in enumerate(colors_to_apply):
            position = i * 100 / (len(colors_to_apply))
            position_next = (i + 1) * 100 / (len(colors_to_apply))

            # Left boundary
            position_adjusted = position
            if i > 0:
                position_adjusted += distance
            gradient_stop = xml.etree.ElementTree.Element("GradientStop")
            gradient_stop.set("StopColor", "Color/" + color_mapping[color])
            gradient_stop.set("Location", str(position_adjusted))
            element.append(gradient_stop)

            # Right boundary
            position_adjusted = position_next
            if i < len(colors_to_apply) - 1:
                position_adjusted -= distance
            gradient_stop = xml.etree.ElementTree.Element("GradientStop")
            gradient_stop.set("StopColor", "Color/" + color_mapping[color])
            gradient_stop.set("Location", str(position_adjusted))
            element.append(gradient_stop)

            tree.write("data/memory/Resources/Graphic.xml")


def set_planeswalker_text(card, id_set):
    planeswalker_text = helper_split_string_along_regex(card.oracle_text, *regex_planeswalker)
    amount_abilities = sum(x[2] == "loyalty" for x in planeswalker_text)

    if amount_abilities > 4:
        info_fail(card.name, "Too many abilities")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
    modal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_MODAL_O] + "']")

    amount_textboxes = amount_abilities
    top_y_coordinate = -46.2047244094489

    if modal.attrib["Visible"] == "true":
        top_y_coordinate += MODAL_HEIGHT

    total_height = 37.13385826771649 + abs(top_y_coordinate)

    if card.loyalty == "":
        total_height += 4.960627698522806

    text_boxes = [[(id_set[ids.PLANESWALKER_VALUE_T][0], id_set[ids.PLANESWALKER_VALUE_O][0]),
                   (id_set[ids.PLANESWALKER_TEXT_T][0], id_set[ids.PLANESWALKER_TEXT_O][0])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][1], id_set[ids.PLANESWALKER_VALUE_O][1]),
                   (id_set[ids.PLANESWALKER_TEXT_T][1], id_set[ids.PLANESWALKER_TEXT_O][1])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][2], id_set[ids.PLANESWALKER_VALUE_O][2]),
                   (id_set[ids.PLANESWALKER_TEXT_T][2], id_set[ids.PLANESWALKER_TEXT_O][2])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][3], id_set[ids.PLANESWALKER_VALUE_O][3]),
                   (id_set[ids.PLANESWALKER_TEXT_T][3], id_set[ids.PLANESWALKER_TEXT_O][3])]]

    if planeswalker_text[0][2] != "loyalty":
        text_boxes.insert(0, [(id_set[ids.ORACLE_TEXT_T], id_set[ids.ORACLE_TEXT_O])])
        amount_textboxes += 1
        set_oracle_text(planeswalker_text[0][0], id_set[ids.ORACLE_TEXT_T], left_align=True)
        planeswalker_text = planeswalker_text[1:]

    step_size = total_height / amount_textboxes
    shifter = amount_textboxes - amount_abilities

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    for i, level in enumerate(text_boxes):
        j = i - shifter

        for pair in level:
            object_box = tree.find(".//TextFrame[@Self='" + pair[1] + "']")

            if i < amount_textboxes:
                object_box.set("Visible", "true")
                if i % 2 == 1:
                    object_box.set("FillColor", "Color/Grey")

                helper_indesign_set_y_coordinates(object_box,
                                                  [top_y_coordinate, top_y_coordinate,
                                                   top_y_coordinate + step_size, top_y_coordinate + step_size])
                shift_coordinates = [step_size * i, step_size * i, step_size * i, step_size * i]
                helper_indesign_shift_y_coordinates(object_box, shift_coordinates)
            else:
                object_box.set("Visible", "false")

        if 0 <= j < amount_abilities:
            set_oracle_text(planeswalker_text[2 * j][0][:-1].replace("−", "-"), level[0][0])
            set_oracle_text(planeswalker_text[2 * j + 1][0].rstrip(), level[1][0])

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def set_oracle_text(oracle_text, object_id, left_align=False):
    id_oracle_text = object_id

    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + id_oracle_text + ".xml")
    parent = tree.find(".//ParagraphStyleRange[1]")
    child = tree.find(".//CharacterStyleRange[1]")
    parent.remove(child)

    if len(oracle_text) > 100 | left_align:
        parent.set("Justification", "LeftAlign")

    oracle_text_array = helper_split_string_along_regex(oracle_text, *regex)

    oracle_text_array = list(filter(lambda x: (x[2] != "reminder"), oracle_text_array))
    if oracle_text_array[0][0].find("\n") == 0:
        oracle_text_array[0] = (oracle_text_array[0][0][1:], oracle_text_array[0][1], oracle_text_array[0][2])

    for part in oracle_text_array:
        if part[1] == "type":
            if part[2] == "normal":
                parent.append(insert_text_element(part[0]))
        elif part[1] == "font":
            if part[2][0] == "KyMana":
                mana = []
                for item in re.findall("({[A-Z0-9]+})", part[0]):
                    mana.append(mana_mapping[item])
                mana = "".join(mana)
                parent.append(insert_text_element(mana, part[2]))
            else:
                parent.append(insert_text_element(part[0], part[2]))

    tree.write("data/memory/Stories/Story_" + id_oracle_text + ".xml")


def set_default_oracle_text(card, id_set, left_align=False):
    set_oracle_text(card.oracle_text, id_set[ids.ORACLE_TEXT_T], left_align)


def set_value(card, id_set):
    id_value = id_set[ids.VALUE_T]

    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string.replace(" ", "")

        insert_value_content(id_value, value_string)

    if card.loyalty != "":
        insert_value_content(id_value, card.loyalty)


def set_artist(card, id_set):
    id_artist = id_set[ids.ARTIST_T]

    insert_value_content(id_artist, card.artist)


def set_collector_information(card, id_set):
    id_collector_information = id_set[ids.COLLECTOR_INFORMATION_T]

    insert_value_content(id_collector_information,
                         card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0])


def set_set(card, id_set):
    id_spread = id_set[ids.SPREAD]
    id_set_icon = id_set[ids.SET_O]

    if not helper_file_exists(f_icon_set + "/" + card.set.lower() + ".svg"):
        info_warn(card.name, "No icon for set")
    else:
        insert_graphic(card, id_spread, id_set_icon, f_icon_set, card.set.lower())


##############
### INSERT ###
##############

def insert_value_content(identifier, value):
    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + identifier + ".xml")
    entry = tree.find(".//Content[1]")
    entry.text = value

    tree.write("data/memory/Stories/Story_" + identifier + ".xml")


def insert_text_element(content, font=("", ""), point_size_correction=0):
    parent = xml.etree.ElementTree.Element("CharacterStyleRange")
    parent.set("PointSize", str(8 + point_size_correction))

    if font != ("", ""):
        if font[1] != "":
            parent.set("FontStyle", font[1])

        properties = xml.etree.ElementTree.Element("Properties")
        applied_font = xml.etree.ElementTree.Element("AppliedFont")
        applied_font.set("type", "string")
        applied_font.text = font[0]

        properties.append(applied_font)
        parent.append(properties)

    content_split = helper_split_string_along_regex(content, ("\n", "type", "break"))

    for element in content_split:
        if element[1] == "type" and element[2] == "break":
            break_node = xml.etree.ElementTree.Element("Br")
            parent.append(break_node)
        else:
            content_node = xml.etree.ElementTree.Element("Content")
            content_node.text = element[0]
            parent.append(content_node)

    return parent


def insert_graphic(card, identifier_spread, identifier_field, path_file, name_file, type_file="svg",
                   mode_scale_image="fit", mode_align_vertical="center"):
    if not helper_file_exists(path_file + "/" + name_file + "." + type_file):
        info_fail(card.name, "Specified graphic does not exist")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + identifier_spread + ".xml")
    element = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    coordinates = helper_indesign_get_coordinates(element)

    # Size of the container
    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    # Bounding box defined in the file
    if type_file == "svg":
        xml_element = xml.etree.ElementTree.Element("SVG")
        bounding_box = helper_vector_bounding_box(path_file, name_file)
    elif type_file in image_types:
        xml_element = xml.etree.ElementTree.Element("Image")
        with Image.open(path_file + "/" + name_file + "." + type_file) as img:
            bounding_box = img.size
    else:
        info_fail(card.name, "Unknown graphics type")
        return

    # Factor to scale the graphic by to fit in the container
    factor_x = size_box_x / bounding_box[0]
    factor_y = size_box_y / bounding_box[1]

    if mode_scale_image == "fit":
        factor = min(factor_x, factor_y)
    elif mode_scale_image == "fit_priority_x":
        if factor_x * bounding_box[1] >= size_box_y:
            factor = factor_x
        else:
            factor = factor_y

    # Final size of the scaled graphic
    size_insert_x = bounding_box[0] * factor
    size_insert_y = bounding_box[1] * factor

    # Distance to move graphic by to fit into center of container
    graphic_position_x = (size_box_x - size_insert_x) / 2 + coordinates[0][0]
    graphic_position_y = coordinates[0][1]
    if mode_align_vertical == "center":
        graphic_position_y += (size_box_y - size_insert_y) / 2

    # Factor (Rotation) (Rotation) Factor TranslateX TranslateY
    xml_element.set("ItemTransform",
                    str(factor) + " 0 0 " + str(factor) + " " + str(graphic_position_x) + " " + str(
                        graphic_position_y))

    xml_prop = xml.etree.ElementTree.Element("Properties")

    # Important to keep all 4 elements, otherwise sizing does not get applied
    xml_bounds = xml.etree.ElementTree.Element("GraphicBounds")
    xml_bounds.set("Left", str(0))
    xml_bounds.set("Top", str(0))
    xml_bounds.set("Right", str(bounding_box[0]))
    xml_bounds.set("Bottom", str(bounding_box[1]))

    xml_link = xml.etree.ElementTree.Element("Link")
    xml_link.set("LinkResourceURI", "file:" + path_file + "/" + name_file + "." + type_file)

    xml_prop.append(xml_bounds)
    xml_element.append(xml_prop)
    xml_element.append(xml_link)
    element.append(xml_element)

    tree.write("data/memory/Spreads/Spread_" + identifier_spread + ".xml")


##############
### HELPER ###
##############

def helper_get_card_types(card):
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))
    return types


def helper_split_string_along_regex(string, *matchers: ([str], str, str)):
    # Build list of all available regex
    all_regex = []
    for triple in matchers:
        for regex in triple[0]:
            all_regex.append(regex)
    all_regex = list(dict.fromkeys(all_regex))

    working_string = string
    result = []

    while len(working_string) > 0:
        current_span = [math.inf, 0]
        current_regex = ""

        # Check which regex matches first, disregard regex that matches after already found ones
        for regex in all_regex:
            pattern = re.compile(regex)
            matches = list(pattern.finditer(working_string))
            if len(matches) > 0 and matches[0].span()[0] < current_span[0]:
                current_span = matches[0].span()
                current_regex = regex
                if current_span[0] == 0:
                    break

        # If no regex matched we are dealing with a normal string
        if current_span[0] == math.inf:
            result.append((working_string, "type", "normal"))
            working_string = ""
        else:
            # Split into two parts
            part_one = working_string[:current_span[0]]
            part_two = working_string[current_span[0]:]

            # Everything before match is normal, remove it first
            rectifier = 0
            if current_span[0] > 0:
                result.append((part_one, "type", "normal"))
                rectifier = len(part_one)

            part_one = part_two[:current_span[1] - rectifier]
            part_two = part_two[current_span[1] - rectifier:]

            # Search which regex matched and add to result
            for triple in matchers:
                if current_regex in triple[0]:
                    result.append((part_one, triple[1], triple[2]))
                    working_string = part_two
                    break

    return result


def helper_file_exists(path):
    return os.path.exists(path)


def helper_vector_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def helper_truncate(string, size=20):
    return string[:size - 2] + ".." if len(string) > size else string


def helper_indesign_get_coordinates(element):
    point_top_left = element.find(".//PathPointType[1]")
    point_bottom_left = element.find(".//PathPointType[2]")
    point_top_right = element.find(".//PathPointType[4]")
    point_bottom_right = element.find(".//PathPointType[3]")

    values = point_top_left.attrib["Anchor"].split(" ")
    coordinates_top_left = float(values[0]), float(values[1])

    values = point_bottom_left.attrib["Anchor"].split(" ")
    coordinates_bottom_left = float(values[0]), float(values[1])

    values = point_top_right.attrib["Anchor"].split(" ")
    coordinates_top_right = float(values[0]), float(values[1])

    values = point_bottom_right.attrib["Anchor"].split(" ")
    coordinates_bottom_right = float(values[0]), float(values[1])

    return coordinates_top_left, coordinates_top_right, coordinates_bottom_left, coordinates_bottom_right


def helper_indesign_set_y_coordinates(indesign_object, set_to):
    top_left = indesign_object.find(".//PathPointType[1]")
    top_right = indesign_object.find(".//PathPointType[4]")
    bottom_left = indesign_object.find(".//PathPointType[2]")
    bottom_right = indesign_object.find(".//PathPointType[3]")

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        point.attrib.pop("Anchor")
        point.attrib.pop("LeftDirection")
        point.attrib.pop("RightDirection")

        coordinates = x_coordinate + " " + str(set_to[i])
        point.set("Anchor", coordinates)
        point.set("LeftDirection", coordinates)
        point.set("RightDirection", coordinates)

    return indesign_object


def helper_indesign_shift_y_coordinates(indesign_object, shift_by):
    top_left = indesign_object.find(".//PathPointType[1]")
    top_right = indesign_object.find(".//PathPointType[4]")
    bottom_left = indesign_object.find(".//PathPointType[2]")
    bottom_right = indesign_object.find(".//PathPointType[3]")

    set_to = []

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        set_to.append(float(y_coordinate) + shift_by[i])

    return helper_indesign_set_y_coordinates(indesign_object, set_to)


def helper_sort_mana_array(mana_array):
    mana_array.sort(key=lambda x: mana_types.index(x))


def helper_generate_ids(name, spread):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + spread + ".xml")

    # IDs to determine
    names = [("Artwork", ids.ARTWORK_O),
             ("Type", ids.TYPE_O),
             ("Name", ids.NAME_T, True),
             ("Type Line", ids.TYPE_LINE_T, True),
             ("Mana Cost", ids.MANA_COST_T, True),
             ("Modal Text", ids.MODAL_T, True),
             ("Modal", ids.GROUP_MODAL_O),
             ("Upper Color Bar", ids.COLOR_BARS_O),
             ("Upper Color Bar Bleed", ids.COLOR_BARS_O),
             ("Lower Color Bar", ids.COLOR_BARS_O),
             ("Lower Color Bar Bleed", ids.COLOR_BARS_O),
             ("Upper Color Bar", ids.GRADIENTS_O, "FillColor"),
             ("Upper Color Bar Bleed", ids.GRADIENTS_O, "FillColor"),
             ("Lower Color Bar", ids.GRADIENTS_O, "FillColor"),
             ("Lower Color Bar Bleed", ids.GRADIENTS_O, "FillColor"),
             ("Oracle Text", ids.ORACLE_TEXT_T, True),
             ("Oracle Text", ids.ORACLE_TEXT_O),
             ("Layout Planeswalker", ids.GROUP_ORACLE_PLANESWALKER_O),
             ("Planeswalker Value 1", ids.PLANESWALKER_VALUE_T, True),
             ("Planeswalker Value 2", ids.PLANESWALKER_VALUE_T, True),
             ("Planeswalker Value 3", ids.PLANESWALKER_VALUE_T, True),
             ("Planeswalker Value 4", ids.PLANESWALKER_VALUE_T, True),
             ("Planeswalker Value 1", ids.PLANESWALKER_VALUE_O),
             ("Planeswalker Value 2", ids.PLANESWALKER_VALUE_O),
             ("Planeswalker Value 3", ids.PLANESWALKER_VALUE_O),
             ("Planeswalker Value 4", ids.PLANESWALKER_VALUE_O),
             ("Planeswalker Text 1", ids.PLANESWALKER_TEXT_T, True),
             ("Planeswalker Text 2", ids.PLANESWALKER_TEXT_T, True),
             ("Planeswalker Text 3", ids.PLANESWALKER_TEXT_T, True),
             ("Planeswalker Text 4", ids.PLANESWALKER_TEXT_T, True),
             ("Planeswalker Text 1", ids.PLANESWALKER_TEXT_O),
             ("Planeswalker Text 2", ids.PLANESWALKER_TEXT_O),
             ("Planeswalker Text 3", ids.PLANESWALKER_TEXT_O),
             ("Planeswalker Text 4", ids.PLANESWALKER_TEXT_O),
             ("Mask", ids.MASK_O),
             ("Value", ids.VALUE_T, True),
             ("Value", ids.VALUE_O),
             ("Value Short Frame", ids.VALUE_SHORT_FRAME_O),
             ("Value Long Frame", ids.VALUE_LONG_FRAME_O),
             ("Mask Short", ids.MASK_SHORT_O),
             ("Mask Long", ids.MASK_LONG_O),
             ("Bottom", ids.GROUP_BOTTOM_O),
             ("Artist", ids.ARTIST_T, True),
             ("Side Indicator Text", ids.SIDE_INDICATOR_T, True),
             ("Side Indicator", ids.SIDE_INDICATOR_O),
             ("Collector Information", ids.COLLECTOR_INFORMATION_T, True),
             ("Set Icon", ids.SET_O)]

    print("id_general_" + name + " = {")
    print("\"" + ids.SPREAD + "\": " + "\"" + spread + "\",")

    entries = []

    for name in names:
        element = tree.find(".//*[@Name='" + name[0] + "']")

        if len(name) > 2 and name[2] is True:
            to_add = "\"" + element.attrib["ParentStory"] + "\","
        elif len(name) > 2:
            to_add = "\"" + element.attrib[name[2]].split("/")[1] + "\","
        else:
            to_add = "\"" + element.attrib["Self"] + "\","

        entries.append(("\"" + name[1] + "\"", to_add))

    duplicates = dict()

    # Count occurrences
    for name in names:
        if name[1] not in duplicates:
            duplicates[name[1]] = 0
        duplicates[name[1]] += 1

    # Print non-duplicates
    carry = []
    previous_entry = ""
    for i, entry in enumerate(entries):
        key = entry[0].replace("\"", "")

        if len(carry) > 1 and entry[0] != previous_entry:
            print(previous_entry + ": " + str(carry) + ",")
            carry = []

        if duplicates[key] <= 1:
            print(entry[0] + ": " + entry[1])
        else:
            previous_entry = entry[0]
            carry.append(entry[1].split(",")[0].replace("\"", ""))

        if i == len(entries) - 1 and len(carry) > 1:
            print(previous_entry + ": " + str(carry) + ",")

    print("}")


############
### INFO ###
############


def info_success(cardname, message):
    print(f"{bcolors.OKGREEN}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_skip(cardname, message):
    print(f"{bcolors.OKBLUE}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_warn(cardname, message):
    print(f"{bcolors.WARNING}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


def info_fail(cardname, message):
    print(f"{bcolors.FAIL}[{helper_truncate(cardname)}]{bcolors.ENDC} \t\t{message}")


if __name__ == '__main__':
    process_cards([("Waking the Trolls", ""),
                   ("Druid Class", "")])

    # helper_generate_ids("front", "uff")
    # helper_generate_ids("back", "u96e")
