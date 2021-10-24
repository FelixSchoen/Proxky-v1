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
    ARTWORK_O = "id_artwork"
    TYPE_O = "id_type"
    NAME_T = "id_name"
    TYPE_LINE_T = "id_type_line"
    MANA_COST_T = "id_mana_cost"
    MODAL_T = "id_modal"
    MODAL_O = "id_modal_tb"
    COLOR_BARS_O = "id_color_bars"
    GRADIENTS_O = "id_gradients"
    ORACLE_TEXT_T = "id_oracle_text"
    ORACLE_TEXT_O = "id_oracle_text_tb"
    MASK_O = "id_mask"
    VALUE_T = "id_value"
    VALUE_O = "id_value_tb"
    VALUE_SHORT_FRAME_O = "id_value_short_frame"
    VALUE_LONG_FRAME_O = "id_value_long_frame"
    MASK_SHORT_O = "id_mask_short"
    MASK_LONG_O = "id_mask_long"
    BOTTOM_O = "id_bottom"
    ARTIST_T = "id_artist"
    SIDE_INDICATOR_O = "id_side_indicator"
    COLLECTOR_INFORMATION_T = "id_collector_information"
    SET_O = "id_set"


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
supported_layouts = ["normal", "modal_dfc"]
id_general_front = {
    ids.SPREAD: "uce",
    ids.ARTWORK_O: "u128",
    ids.TYPE_O: "u2d6",
    ids.NAME_T: "u2be",
    ids.TYPE_LINE_T: "u2eb",
    ids.MANA_COST_T: "u7fc",
    ids.MODAL_T: "u320",
    ids.MODAL_O: "u597",
    ids.COLOR_BARS_O: ["u12a", "u816", "u5e1", "u818"],
    ids.GRADIENTS_O: ["u9a0", "u9a2", "u9a1", "u9a3"],
    ids.ORACLE_TEXT_T: "u3ee",
    ids.ORACLE_TEXT_O: "u400",
    ids.MASK_O: "u5e7",
    ids.VALUE_T: "u49f",
    ids.VALUE_O: "u4b1",
    ids.VALUE_SHORT_FRAME_O: "u4e7",
    ids.VALUE_LONG_FRAME_O: "u4fd",
    ids.MASK_SHORT_O: "u41e",
    ids.MASK_LONG_O: "u4f1",
    ids.BOTTOM_O: "u5c1",
    ids.ARTIST_T: "u23f",
    ids.SIDE_INDICATOR_O: "u698",
    ids.COLLECTOR_INFORMATION_T: "u25f",
    ids.SET_O: "u293",
}
id_general_back = {
    "id_spread": "ub1e",
    "id_artwork": "uc6a",
    "id_type": "uc69",
    "id_name": "uc55",
    "id_type_line": "uc3e",
    "id_mana_cost": "uc27",
    "id_modal": "uc07",
    "id_modal_tb": "ubfc",
    "id_oracle_text": "ube7",
    "id_oracle_text_tb": "ube4",
    "id_mask": "ub25",
    "id_value": "ub9f",
    "id_value_tb": "ub9c",
    "id_value_short_frame": "ub4a",
    "id_value_long_frame": "ub43",
    "id_mask_short": "ub49",
    "id_mask_long": "ub27",
    "id_bottom": "ub28",
    "id_artist": "ub85",
    "id_side_indicator": "ub66",
    "id_collector_information": "ub52",
    "id_set": "ub4e",
    "id_color_bars": ['uc21', 'uc20', 'ub42', 'ub41'],
    "id_gradients": ['u832', 'u832', 'u832', 'u832'],
}

mana_types = ["W", "U", "B", "R", "G"]
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
    (["{[A-Z0-9]+}"], "font", "KyMana"),
    (["Adamant", "Addendum", "Battalion", "Bloodrush", "Channel", "Chroma", "Cohort", "Constellation", "Converge",
      "Council's dilemma", "Coven", "Delirium", "Domain", "Eminence", "Enrage", "Fateful hour", "Ferocious",
      "Formidable", "Grandeur", "Hellbent", "Heroic", "Imprint", "Join forces", "Kinship", "Landfall", "Lieutenant",
      "Magecraft", "Metalcraft", "Morbid", "Pack tactics", "Parley", "Radiance", "Raid", "Rally", "Revolt",
      "Spell mastery", "Strive", "Sweep", "Tempting offer", "Threshold", "Underdog", "Undergrowth",
      "Will of the council"], "font", "MPlantin-Italic"),
    ([" ?\(.+\)"], "type", "reminder"),
    # (["LEVEL [\d]+(-[\d]+|\+)\\n([\d]+|\*)/([\d]+|\*)"], "type", "special")
]


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

    if card.layout == "normal":
        card_fill(card, id_general_front)
        card_delete_backside(id_general_back)
    elif card.layout == "modal_dfc":
        set_layout_double_faced([id_general_front, id_general_back])
        set_modal(card, [id_general_front, id_general_back])
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
    if "Creature" not in types:
        set_layout_non_creature(id_set)

    # Artwork
    set_artwork(card, id_set)

    # Type Icon
    set_type_icon(card, id_set)

    # Card Name
    set_card_name(card, id_set)

    # Type Line
    set_type_line(card, id_set)

    # Mana Cost
    set_mana(card, id_set)

    # Color Bar
    set_color_bar(card, id_set)

    # Oracle Text
    set_oracle_text(card, id_set)

    # Value
    set_value(card, id_set)

    # Artist
    set_artist(card, id_set)

    # Collector Information
    set_collector_information(card, id_set)

    # Set
    set_set(card, id_set)


def card_delete_backside(id_set):
    os.remove("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    tree = xml.etree.ElementTree.parse("data/memory/designmap.xml")
    element = tree.getroot().find(".//*[@src='Spreads/Spread_" + id_set[ids.SPREAD] + ".xml']")
    tree.getroot().remove(element)

    with open("data/memory/designmap.xml", "wb") as file:
        file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        file.write(b'<?aid style="50" type="document" readerVersion="6.0" featureSet="257" product="16.4(55)" ?>')
        tree.write(file, xml_declaration=False, encoding="utf-8")


##############
### LAYOUT ###
##############

def set_layout_double_faced(id_sets):
    for id_set in id_sets:
        tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
        modal = tree.find(".//Group[@Self='" + id_set[ids.MODAL_O] + "']")
        modal.set("Visible", "true")

        shift_by = 10.27559055118109

        color_bars = [tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][0] + "']"),
                      tree.find(".//Rectangle[@Self='" + id_set[ids.COLOR_BARS_O][1] + "']")]

        for color_bar in color_bars:
            coordinates = color_bar.attrib["ItemTransform"].split(" ")
            color_bar.set("ItemTransform",
                          coordinates[0] + " " + coordinates[1] + " " + coordinates[2] + " " + coordinates[3] + " " +
                          coordinates[4] + " " + str(float(coordinates[5]) + shift_by))

        oracle_text = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")

        top_left = oracle_text.find(".//PathPointType[1]")
        top_right = oracle_text.find(".//PathPointType[4]")

        for point in [top_left, top_right]:
            x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
            point.attrib.pop("Anchor")
            point.attrib.pop("LeftDirection")
            point.attrib.pop("RightDirection")

            coordinates = x_coordinate + " " + str(float(y_coordinate) + shift_by)
            point.set("Anchor", coordinates)
            point.set("LeftDirection", coordinates)
            point.set("RightDirection", coordinates)

        side_indicator = tree.find(".//Group[@Self='" + id_set[ids.SIDE_INDICATOR_O] + "']")
        side_indicator.set("Visible", "true")

        tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def set_layout_non_creature(id_set):
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
    bottom = tree.find(".//Group[@Self='" + id_set[ids.BOTTOM_O] + "']")
    mask_short = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_SHORT_O] + "']")
    mask_long = tree.find(".//Polygon[@Self='" + id_set[ids.MASK_LONG_O] + "']")

    mask.append(bottom)

    for child in mask_short.findall(".//Group[@Self='" + id_set[ids.BOTTOM_O] + "']"):
        mask_short.remove(child)
    for child in mask_long.findall(".//Group[@Self='" + id_set[ids.BOTTOM_O] + "']"):
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
                       mode_scale_image="fit_x", mode_align_vertical="top")
    else:
        insert_graphic(card, id_spread, id_artwork, f_artwork + "/" + card.set.upper(), card.name, type_file=image_type,
                       mode_scale_image="fit_x", mode_align_vertical="top")


def set_type_icon(card, id_set):
    id_spread = id_set[ids.SPREAD]
    id_type = id_set[ids.TYPE_O]

    # Get types of card
    types = helper_get_card_types(card)
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


def set_mana(card, id_set):
    id_mana_cost = id_set[ids.MANA_COST_T]

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mapping = "".join([mana_mapping["{" + m + "}"] for m in mana])
    insert_value_content(id_mana_cost, mapping)


def set_modal(card, id_sets, type="MODAL"):
    for i, id_set in enumerate(id_sets):
        face = card.card_faces[(i + 1) % 2]
        insert_value_content(id_set[ids.MODAL_T], type + " — " + face.type_line.replace("—", "•"))


def set_color_bar(card, id_set):
    id_gradients = id_set[ids.GRADIENTS_O]

    distance = 1.5
    colors_to_apply = card.colors

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

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


def set_oracle_text(card, id_set, left_align=False):
    id_oracle_text = id_set[ids.ORACLE_TEXT_T]

    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + id_oracle_text + ".xml")
    parent = tree.find(".//ParagraphStyleRange[1]")
    child = tree.find(".//CharacterStyleRange[1]")
    parent.remove(child)

    if len(card.oracle_text) > 100 | left_align:
        parent.set("Justification", "LeftAlign")

    oracle_text_array = helper_split_string_along_regex(card.oracle_text, *regex)

    for part in oracle_text_array:
        if part[1] == "type":
            if part[2] == "normal":
                parent.append(insert_text_element(part[0]))
        elif part[1] == "font":
            if part[2] == "KyMana":
                parent.append(insert_text_element(mana_mapping[part[0]], part[2]))
            else:
                parent.append(insert_text_element(part[0], part[2]))

    tree.write("data/memory/Stories/Story_" + id_oracle_text + ".xml")


def set_value(card, id_set):
    id_value = id_set[ids.VALUE_T]

    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string.replace(" ", "")

        insert_value_content(id_value, value_string)


def set_artist(card, id_set):
    id_artist = id_set[ids.ARTIST_T]

    insert_value_content(id_artist, card.artist)


def set_collector_information(card, id_set):
    id_collector_information = id_set["id_collector_information"]

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


def insert_text_element(content, font="", point_size_correction=0):
    parent = xml.etree.ElementTree.Element("CharacterStyleRange")
    parent.set("PointSize", str(8 + point_size_correction))

    if font != "":
        properties = xml.etree.ElementTree.Element("Properties")
        applied_font = xml.etree.ElementTree.Element("AppliedFont")
        applied_font.set("type", "string")
        applied_font.text = font

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
    elif mode_scale_image == "fit_x":
        factor = factor_x

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


def helper_generate_ids(spread):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + spread + ".xml")

    names = [("Artwork", ids.ARTWORK_O),
             ("Type", ids.TYPE_O),
             ("Name", ids.NAME_T, True),
             ("Type Line", ids.TYPE_LINE_T, True),
             ("Mana Cost", ids.MANA_COST_T, True),
             ("Modal Text", ids.MODAL_T, True),
             ("Modal", ids.MODAL_O),
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
             ("Mask", ids.MASK_O),
             ("Value", ids.VALUE_T, True),
             ("Value", ids.VALUE_O),
             ("Value Short Frame", ids.VALUE_SHORT_FRAME_O),
             ("Value Long Frame", ids.VALUE_LONG_FRAME_O),
             ("Mask Short", ids.MASK_SHORT_O),
             ("Mask Long", ids.MASK_LONG_O),
             ("Bottom", ids.BOTTOM_O),
             ("Artist", ids.ARTIST_T, True),
             ("Side Indicator", ids.SIDE_INDICATOR_O),
             ("Collector Information", ids.COLLECTOR_INFORMATION_T, True),
             ("Set Icon", ids.SET_O)]

    print("id_general_xyz = {")
    print("\"" + ids.SPREAD + "\": " + "\"" + spread + "\",")

    array = []

    for name in names:
        element = tree.find(".//*[@Name='" + name[0] + "']")
        if len(name) > 2 and name[2] is True:
            array.append(("\"" + name[1] + "\"", "\"" + element.attrib["ParentStory"] + "\","))
        elif len(name) > 2:
            array.append(("\"" + name[1] + "\"", "\"" + element.attrib[name[2]].split("/")[1] + "\","))
        else:
            array.append(("\"" + name[1] + "\"", "\"" + element.attrib["Self"] + "\","))

    for entry in array:
        if "color_bars" not in entry[0] and "gradients" not in entry[0]:
            print(entry[0] + ": " + entry[1])

    color_bars = []

    for entry in array:
        if "color_bars" in entry[0]:
            color_bars.append(entry[1].split(",")[0].replace("\"", ""))

    print("\"id_color_bars\": " + str(color_bars) + ",")

    gradients = []

    for entry in array:
        if "gradients" in entry[0]:
            gradients.append(entry[1].split(",")[0].replace("\"", ""))

    print("\"id_gradients\": " + str(gradients) + ",")

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
    # process_cards([("Neverwinter Dryad", ""), ("Brushfire Elemental", "ZNR"), ("Roiling Regrowth", "ZNR")])
    process_cards([("Kazandu Mammoth", ""), ("Tangled Florahedron", "")])
    # helper_generate_ids(id_general_back["id_spread"])
