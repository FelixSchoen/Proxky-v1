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


# API
api_url = "https://api.scryfall.com"

# Folders
f_preset = "D:/Drive/Creative/Magic/Proxky/Types/General.idml"
f_output = "D:/Games/Magic/Proxky/v1/Documents/Test"
f_artwork = "D:/Games/Magic/Proxky/v1/Artwork"
f_icon_types = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Card Types"
f_icon_mana = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Mana"
f_icon_set = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Set"

# Enumerations
supported_layouts = ["normal"]
id_general_frontside = {
    "id_spread": "uce",
    "id_artwork": "u128",
    "id_type": "u2d6",
    "id_name": "u2be",
    "id_type_line": "u2eb",
    "id_mana": "u7fc",
    "id_transforms": "u320",
    "id_color_bars": ["u12a", "u816", "u5e1", "u818"],
    "id_gradients": ["u9a0", "u9a2", "u9a1", "u9a3"],
    "id_oracle_text": "u3ee",
    "id_value": "u49f",
    "id_artist": "u23f",
    "id_side_indicator": "u3d2",
    "id_collector_information": "u25f",
    "id_set": "u293",
}
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
        card_fill(card, id_general_frontside)
        # TODO Delete backside

    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    if helper_file_exists(target_file_full_path):
        os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    # Remove files from working memory
    # shutil.rmtree("data/memory")
    return True


def card_fill(card: Card, id_set):
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


##############
### LAYOUT ###
##############

def layout_basic():
    print("not implemented")


def set_artwork(card, id_set):
    id_spread = id_set["id_spread"]
    id_artwork = id_set["id_artwork"]

    path = f_artwork + "/" + card.set.upper() + "/" + card.name
    image_type = "na"

    for possible_image_type in image_types:
        if not helper_file_exists(path + "." + possible_image_type):
            continue
        else:
            image_type = possible_image_type

    if image_type == "na":
        info_warn(card.name, "No artwork for card exists")
    else:
        insert_graphic(card, id_spread, id_artwork, f_artwork + "/" + card.set.upper(), card.name, type_file=image_type,
                       mode_scale_image="fit_x", mode_align_vertical="top")


def set_type_icon(card, id_set):
    id_spread = id_set["id_spread"]
    id_type = id_set["id_type"]

    # Get types of card
    card_type = "na"
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))

    # Prioritize some types
    for candidate in types:
        if "creature" in candidate.lower():
            card_type = "Creature"

    if card_type == "na":
        card_type = types[0]

    if not helper_file_exists(f_icon_types + "/" + card_type.lower() + ".svg"):
        info_warn(card.name, "No icon for card type")
    else:
        insert_graphic(card, id_spread, id_type, f_icon_types, card_type.lower())


def set_card_name(card, id_set):
    id_name = id_set["id_name"]

    insert_value_content(id_name, card.name)


def set_type_line(card, id_set):
    id_type_line = id_set["id_type_line"]

    insert_value_content(id_type_line, card.type_line.replace("—", "•"))


def set_mana(card, id_set):
    id_mana = id_set["id_mana"]

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mapping = "".join([mana_mapping["{" + m + "}"] for m in mana])
    insert_value_content(id_mana, mapping)


def set_oracle_text(card, id_set, left_align=False):
    id_oracle_text = id_set["id_oracle_text"]

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
    id_value = id_set["id_value"]

    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string.replace(" ", "")

        insert_value_content(id_value, value_string)


def set_artist(card, id_set):
    id_artist = id_set["id_artist"]

    insert_value_content(id_artist, card.artist)


def set_collector_information(card, id_set):
    id_collector_information = id_set["id_collector_information"]

    insert_value_content(id_collector_information,
                         card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0])


def set_set(card, id_set):
    id_spread = id_set["id_spread"]
    id_set_icon = id_set["id_set"]

    if not helper_file_exists(f_icon_set + "/" + card.set.lower() + ".svg"):
        info_warn(card.name, "No icon for set")
    else:
        insert_graphic(card, id_spread, id_set_icon, f_icon_set, card.set.lower())


def set_color_bar(card, id_set):
    id_gradients = id_set["id_gradients"]

    distance = 1.5
    colors_to_apply = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))

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
        info_warn(card.name, "Specified graphic does not exist")
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
    process_cards([("Neverwinter Dryad", ""), ("Brushfire Elemental", "ZNR"), ("Kazandu Mammoth", "")])
