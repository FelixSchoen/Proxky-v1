import json
import shutil
import time
import urllib.parse
import zipfile
from time import sleep

from card import *
from carddata import *
from layout import *


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
        card_delete_backside(id_general_back)

        card_fill(card, id_general_front)
    elif card.layout in ["modal_dfc", "transform"]:
        card_layout_double_faced([id_general_front, id_general_back])

        set_modal(card, [id_general_front, id_general_back], card.layout)

        card_fill(card.card_faces[0], id_general_front)
        card_fill(card.card_faces[1], id_general_back)
    elif card.layout in ["split"]:
        card_layout_split(id_general_front)
        card_delete_backside(id_general_back)

        card_fill(card.card_faces[0], id_general_front_st)
        card_fill(card.card_faces[1], id_general_front_sb)

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


if __name__ == '__main__':
    process_cards([("Life // Death", ""), ])

    # helper_generate_ids("front", "uff")
    # helper_generate_ids("front", "uff", mode="split", prefix="ST")
    # helper_generate_ids("front", "uff", mode="split", prefix="SB")
    # helper_generate_ids("back", "u2635")
