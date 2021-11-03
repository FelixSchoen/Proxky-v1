import json
import shutil
import time
import urllib.parse
import zipfile
from os import listdir
from time import sleep

from card import *
from carddata import *
from layout import *


def process_decklist(path):
    cards = []

    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            if re.match(regex_decklist_id, line) is not None:
                result = re.match(regex_decklist_id, line)
                id = result.group("id")
                cards.append(("ID Card", "id", id))
            else:
                result = re.match(regex_decklist, line)
                name = result.group("name")
                card_set = result.group("set")

                if card_set is not None:
                    cards.append((name, "set", card_set))
                else:
                    cards.append((name, "normal"))
    process_cards(cards)


def process_cards(card_names: list[(str, str, str)]):
    for i, card_name in enumerate(card_names):
        start_time = time.time()

        if card_name[1] == "set":
            response = requests.get(
                api_url + "/cards/named?exact=" + urllib.parse.quote(card_name[0]) + "&set=" + urllib.parse.quote(
                    card_name[2]))
        elif card_name[1] == "id":
            response = requests.get(
                api_url + "/cards/" + urllib.parse.quote(card_name[2]))
        else:
            response = requests.get(
                api_url + "/cards/named?exact=" + urllib.parse.quote(card_name[0]))

        # Check status code
        if response.status_code != 200:
            info_fail(card_name[0], "Could not fetch card")
            continue

        card = Card(json.loads(response.text))
        if process_card(card):
            info_success(card.name, "Successfully processed card")

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

        card_fill(card, id_general_front, card.layout)
    elif card.layout in ["modal_dfc", "transform"]:
        card_layout_double_faced([id_general_front, id_general_back])

        set_modal(card, [id_general_front, id_general_back], card.layout)

        card_fill(card.card_faces[0], id_general_front, card.layout)
        card_fill(card.card_faces[1], id_general_back, card.layout)
    elif card.layout in ["split"]:
        card_layout_split(id_general_front)
        card_delete_backside(id_general_back)

        card_fill(card.card_faces[0], id_general_front_st, card.layout)
        card_fill(card.card_faces[1], id_general_front_sb, card.layout)
    elif card.layout in ["adventure"]:
        card_layout_adventure(id_general_front)
        card_delete_backside(id_general_back)

        id_adventure_right = id_general_front.copy()
        id_adventure_right[ids.ORACLE_TEXT_T] = id_general_front_adventure[ids.ADVENTURE_ORACLE_TEXT_R_T]
        id_adventure_right[ids.ORACLE_TEXT_O] = id_general_front_adventure[ids.ADVENTURE_ORACLE_TEXT_R_O]

        id_adventure_left = id_general_front_adventure.copy()
        id_adventure_left[ids.ORACLE_TEXT_T] = id_adventure_left[ids.ADVENTURE_ORACLE_TEXT_L_T]

        card_fill(card.card_faces[1], id_adventure_left, card.layout)
        card_fill(card.card_faces[0], id_adventure_right, card.layout)
    elif card.layout in ["token"]:
        card_layout_token(id_general_front, card)
        card_delete_backside(id_general_back)

        card_fill(card, id_general_front, card.layout)

    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    if helper_file_exists(target_file_full_path):
        os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    # Remove files from working memory
    # shutil.rmtree("data/memory")
    return True


def card_fill(card: Card, id_set, layout):
    types = helper_get_card_types(card)

    # Check if basic
    if "Basic Land" in card.type_line:
        card_layout_no_oracle_text(id_set, card)

    # Value
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
    elif layout in ["adventure"]:
        set_default_oracle_text(card, id_set, left_align=True)
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
    process_decklist("data/decks/decklist.txt")

    # helper_generate_all_ids()
