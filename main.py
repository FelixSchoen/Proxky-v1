import json
import os
import re
import shutil
import urllib.parse
import xml.etree.ElementTree
import zipfile
from time import sleep

import requests

from card import Card

api_url = "https://api.scryfall.com"

f_preset = "D:/Drive/Creative/Magic/Proxky/Types/General.idml"
f_output = "D:/Games/Magic/Proxky/v1/Documents/Test/"
f_icon_set = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Set"
f_icon_mana = "D:/Drive/Creative/Magic/Proxky/Resource/Icons/Mana"

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


def search_for_cards(cardnames: list[str]):
    cards = []

    for cardname in cardnames:
        response = requests.get(api_url + "/cards/named?exact=" + urllib.parse.quote(cardname))
        card = Card(json.loads(response.text))
        do_something(card)
        sleep(0.1)


def do_something(card: Card):
    cleansed_name = card.name.replace("//", "--")
    target_folder_path = f_output + card.set.upper()
    target_file_path = target_folder_path + "/" + cleansed_name
    target_file_full_path = target_file_path + ".idml"

    os.makedirs(target_folder_path, exist_ok=True)
    shutil.copyfile(f_preset, target_file_full_path)

    with zipfile.ZipFile(target_file_full_path, "r") as archive:
        archive.extractall("data/memory")

    set_information(card, values_general_card)

    # TODO
    insert_svg(values_general_card["id_spread"], values_general_card["id_type"], f_icon_set, "znr", "1")

    shutil.make_archive(target_file_path, "zip", "data/memory")
    os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    # shutil.rmtree("data/memory")


def set_information(card: Card, id_set):
    # Card Name
    xml_set_simple_content(id_set["id_name"], card.name)

    # Type Line
    xml_set_simple_content(id_set["id_type_line"], card.type_line.replace("—", "•"))

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
            parent.append(generate_text_element(mapping[0], "mana", mapping[1] if len(mapping) > 1 else ""))
            text_carry = text_carry[text_carry.find("}") + 1:]
        elif text_carry.find("{") >= 0:
            parent.append(generate_text_element(text_carry[:text_carry.find("{")]))
            text_carry = text_carry[text_carry.find("{"):]
        else:
            parent.append(generate_text_element(text_carry))
            break

    tree.write("data/memory/Stories/Story_" + identifier + ".xml")

    # Value
    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string.replace(" ", "")

        xml_set_simple_content(id_set["id_value"], value_string)

    # Artist
    xml_set_simple_content(id_set["id_artist"], card.artist)

    # Collector Information
    xml_set_simple_content(id_set["id_collector_information"],
                           card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0])


def xml_set_simple_content(identifier, value):
    tree = xml.etree.ElementTree.parse("data/memory/Stories/Story_" + identifier + ".xml")
    entry = tree.find(".//Content[1]")
    entry.text = value

    tree.write("data/memory/Stories/Story_" + identifier + ".xml")


def generate_text_element(content, font="", point_size=""):
    parent = xml.etree.ElementTree.Element("CharacterStyleRange")
    parent.set("AppliedCharacterStyle", "CharacterStyle/$ID/[No character style]")

    if point_size != "":
        parent.set("PointSize", str(8 + point_size))

    if font != "":
        properties = xml.etree.ElementTree.Element("Properties")
        applied_font = xml.etree.ElementTree.Element("AppliedFont")
        applied_font.set("type", "string")
        applied_font.text = "Mana"

        properties.append(applied_font)
        parent.append(properties)

    content_node = xml.etree.ElementTree.Element("Content")
    content_node.text = content
    parent.append(content_node)

    return parent


def get_vector_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def get_coordinates(element):
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


def insert_svg(identifier_spread, identifier_field, path_svg, name_svg, id):
    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + identifier_spread + ".xml")
    element = tree.find(".//Rectangle[@Self='" + identifier_field + "']")
    coordinates = get_coordinates(element)

    size_box_x = abs(coordinates[1][0] - coordinates[0][0])
    size_box_y = abs(coordinates[2][1] - coordinates[1][1])

    bounding_box = get_vector_bounding_box(path_svg, name_svg)

    factor_x = size_box_x / bounding_box[0]
    factor_y = size_box_y / bounding_box[1]

    factor = min(factor_x, factor_y)

    size_insert_x = bounding_box[0] * factor
    size_insert_y = bounding_box[1] * factor

    size_translate_center_x = (size_box_x - size_insert_x) / 2 + coordinates[0][0]
    size_translate_center_y = (size_box_y - size_insert_y) / 2 + coordinates[0][1]

    xml_svg = xml.etree.ElementTree.Element("SVG")
    xml_svg.set("ItemTransform",
                str(factor) + " 0 0 " + str(factor) + " " + str(size_translate_center_x) + " " + str(
                    size_translate_center_y))

    xml_prop = xml.etree.ElementTree.Element("Properties")

    xml_bounds = xml.etree.ElementTree.Element("GraphicBounds")
    xml_bounds.set("Left", str(0))
    xml_bounds.set("Top", str(0))
    xml_bounds.set("Right", str(bounding_box[0]))
    xml_bounds.set("Bottom", str(bounding_box[1]))

    xml_link = xml.etree.ElementTree.Element("Link")
    xml_link.set("Self", "ul" + id.zfill(2))
    xml_link.set("LinkResourceURI", "file:" + path_svg + "/" + name_svg + ".svg")

    xml_prop.append(xml_bounds)
    xml_svg.append(xml_prop)
    xml_svg.append(xml_link)
    element.append(xml_svg)

    tree.write("data/memory/Spreads/Spread_" + identifier_spread + ".xml")


if __name__ == '__main__':
    search_for_cards(["Neverwinter Dryad"])
