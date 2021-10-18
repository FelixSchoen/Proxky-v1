import json
import urllib.parse
from os.path import basename

import requests
import zipfile
import os
import shutil
import xml.etree.ElementTree

from card import Card

api_url = "https://api.scryfall.com"

f_preset = "D:/Drive/Creative/Magic/Proxky/Types/General.idml"
f_output = "D:/Games/Magic/Proxky/v1/Documents/Test/"

values_general_card = {
    "id_name": "u2be",
    "id_type_line": "u2eb",
    "id_transforms": "u320",
    "id_oracle_text": "u3ee",
    "id_value": "u49f",
    "id_artist": "u23f",
    "id_side_indicator": "u3d2",
    "id_collector_information": "u25f",
}


def search_for_cards(cardnames: list[str]):
    cards = []

    for cardname in cardnames:
        response = requests.get(api_url + "/cards/named?exact=" + urllib.parse.quote(cardname))
        card = Card(json.loads(response.text))
        do_something(card)


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

    shutil.make_archive(target_file_path, "zip", "data/memory")
    os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    shutil.rmtree("data/memory")


def set_information(card: Card, id_set):
    # Cardname
    xml_set_simple_content(id_set["id_name"], card.name)

    # Type Line
    xml_set_simple_content(id_set["id_type_line"], card.type_line.replace("-", "•"))

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


if __name__ == '__main__':
    search_for_cards(["Ancient Greenwarden"])
