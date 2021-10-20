import json
import os
import shutil
import urllib.parse
import xml.etree.ElementTree
import zipfile
from time import sleep

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
f_icon_types = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Card Types"
f_icon_mana = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Mana"
f_icon_set = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Set"

# Enumerations
supported_layouts = ["normal"]
values_general_card = {
    "id_spread": "uce",
    "id_type": "u2d6",
    "id_name": "u2be",
    "id_type_line": "u2eb",
    "id_mana_1": "u39b",
    "id_mana_2": "u3a2",
    "id_mana_3": "u694",
    "id_mana_4": "u695",
    "id_mana_5": "u696",
    "id_transforms": "u320",
    "id_oracle_text": "u3ee",
    "id_value": "u49f",
    "id_artist": "u23f",
    "id_side_indicator": "u3d2",
    "id_collector_information": "u25f",
    "id_set": "u293",
}
mana_mapping = {
    "{T}": [""],
    "{W}": [""],
    "{U}": [""],
    "{B}": [""],
    "{R}": [""],
    "{G}": [""],
    "{C}": [""],
    "{0}": ["", -0.5],
    "{1}": ["", -0.5],
    "{2}": ["", -0.5],
    "{3}": ["", -0.5]
}


def process_cards(card_names: list[(str, str)]):
    for card_name in card_names:
        sleep(0.1)
        response = requests.get(
            api_url + "/cards/named?exact=" + urllib.parse.quote(card_name[0]) + "&set=" + urllib.parse.quote(
                card_name[1]))

        # Check status code
        if response.status_code != 200:
            info_fail(card_name[0], "Could not fetch card")
            continue

        card = Card(json.loads(response.text))
        if process_card(card):
            info_success(card_name[0], "\t\t\t\tSuccessfully processed card")


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
        card_fill(card, values_general_card)
        # TODO Delete backside

    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    # Remove files from working memory
    # shutil.rmtree("data/memory")
    return True


def card_fill(card: Card, id_set):
    # Type
    card_type = "na"
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))

    # Prioritize creatures
    for candidate in types:
        if "creature" in candidate.lower():
            card_type = "Creature"

    if card_type == "na":
        card_type = types[0]

    if not helper_file_exists(f_icon_types + "/" + card_type.lower() + ".svg"):
        info_warn(card.name, "No icon for card type")
    else:
        insert_svg(id_set["id_spread"], id_set["id_type"], f_icon_types, card_type.lower())

    # Card Name
    insert_value_content(id_set["id_name"], card.name)

    # Type Line
    insert_value_content(id_set["id_type_line"], card.type_line.replace("—", "•"))

    # Mana Cost
    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mana.reverse()

    if len(mana) > 5:
        info_warn(card.name, "Too many mana values")
    else:
        for i, cost in enumerate(mana):
            if not helper_file_exists(f_icon_mana + "/" + cost.lower() + ".svg"):
                info_warn(card.name, "No icon for mana type")
            else:
                insert_svg(id_set["id_spread"], id_set["id_mana_" + str(i + 1)], f_icon_mana, cost.lower())

    # Oracle Text
    identifier = id_set["id_oracle_text"]
    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + identifier + ".xml")
    parent = tree.find(".//ParagraphStyleRange[1]")
    child = tree.find(".//CharacterStyleRange[1]")
    parent.remove(child)

    text_carry = card.oracle_text

    if len(text_carry) > 100:
        parent.set("Justification", "LeftAlign")

    while len(text_carry) > 0:
        if text_carry[0] == "{":
            mapping = mana_mapping[text_carry[:text_carry.find("}") + 1]]
            parent.append(insert_text_element(mapping[0], "Mana", mapping[1] if len(mapping) > 1 else 0))
            text_carry = text_carry[text_carry.find("}") + 1:]
        elif text_carry.find("{") >= 0:
            parent.append(insert_text_element(text_carry[:text_carry.find("{")]))
            text_carry = text_carry[text_carry.find("{"):]
        else:
            parent.append(insert_text_element(text_carry))
            break

    tree.write("data/memory/Stories/Story_" + identifier + ".xml")

    # Value
    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string.replace(" ", "")

        insert_value_content(id_set["id_value"], value_string)

    # Artist
    insert_value_content(id_set["id_artist"], card.artist)

    # Collector Information
    insert_value_content(id_set["id_collector_information"],
                         card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0])

    # Set
    if not helper_file_exists(f_icon_set + "/" + card.set.lower() + ".svg"):
        info_warn(card.name, "No icon for set")
    else:
        insert_svg(id_set["id_spread"], id_set["id_set"], f_icon_set, card.set.lower())


def card_layout_basic():
    print("not implemented")


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

    content_node = xml.etree.ElementTree.Element("Content")
    content_node.text = content
    parent.append(content_node)

    return parent


def insert_svg(identifier_spread, identifier_field, path_svg, name_svg):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + identifier_spread + ".xml")
    element = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    coordinates = indesign_get_coordinates(element)

    # Size of the container
    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    # Bounding box defined in the SVG
    bounding_box = helper_vector_bounding_box(path_svg, name_svg)

    # Factor to scale the SVG by to fit in the container
    factor_x = size_box_x / bounding_box[0]
    factor_y = size_box_y / bounding_box[1]

    factor = min(factor_x, factor_y)

    # Final size of the scaled SVG
    size_insert_x = bounding_box[0] * factor
    size_insert_y = bounding_box[1] * factor

    # Distance to move SVG by to fit into center of container
    size_translate_center_x = (size_box_x - size_insert_x) / 2 + coordinates[0][0]
    size_translate_center_y = (size_box_y - size_insert_y) / 2 + coordinates[0][1]

    # InDesign SVG stuff
    xml_svg = xml.etree.ElementTree.Element("SVG")
    # Factor (Rotation) (Rotation) Factor TranslateX TranslateY
    xml_svg.set("ItemTransform",
                str(factor) + " 0 0 " + str(factor) + " " + str(size_translate_center_x) + " " + str(
                    size_translate_center_y))

    xml_prop = xml.etree.ElementTree.Element("Properties")

    # Important to keep all 4 elements, otherwise sizing does not get applied
    xml_bounds = xml.etree.ElementTree.Element("GraphicBounds")
    xml_bounds.set("Left", str(0))
    xml_bounds.set("Top", str(0))
    xml_bounds.set("Right", str(bounding_box[0]))
    xml_bounds.set("Bottom", str(bounding_box[1]))

    xml_link = xml.etree.ElementTree.Element("Link")
    xml_link.set("LinkResourceURI", "file:" + path_svg + "/" + name_svg + ".svg")

    xml_prop.append(xml_bounds)
    xml_svg.append(xml_prop)
    xml_svg.append(xml_link)
    element.append(xml_svg)

    tree.write("data/memory/Spreads/Spread_" + identifier_spread + ".xml")


def helper_file_exists(path):
    return os.path.exists(path)


def helper_vector_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def indesign_get_coordinates(element):
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


def info_success(cardname, message):
    print(f"{bcolors.OKGREEN}[{cardname}]{bcolors.ENDC} {message}")


def info_warn(cardname, message):
    print(f"{bcolors.WARNING}[{cardname}]{bcolors.ENDC} {message}")


def info_fail(cardname, message):
    print(f"{bcolors.FAIL}[{cardname}]{bcolors.ENDC} {message}")


if __name__ == '__main__':
    process_cards([("Neverwinter Dryad", ""), ("Kazandu Mammoth", "")])
