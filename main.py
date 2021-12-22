import getopt
import json
import shutil
import time
import urllib.parse
import zipfile
import sys
from time import sleep

import win32com.client

from card import *
from carddata import *
from info import *
from layout import *
from settings import api_url
from utility import *


def process_decklist(path):
    cards = []

    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            dictionary = dict()
            options = dict()
            match = re.match(regex_card_entry, line)

            dictionary["options"] = options
            dictionary["amount"] = match.group("amount")
            dictionary["name"] = match.group("name")

            option_string = match.group("flags")

            if option_string is not None:
                specified_options = option_string[2:-1].split(", ")

                for option in specified_options:
                    option_match = re.match(regex_card_options, option)
                    if option_match.group("type") in ["set", "id"]:
                        dictionary[option_match.group("type")] = option_match.group("id")
                    else:
                        options[option_match.group("type")] = option_match.group("id")

            cards.append(dictionary)

    return cards


def process_cards(card_names):
    for i, entry in enumerate(card_names):
        start_time = time.time()

        card = Card.get_card_object(entry)
        if card is None:
            continue

        if process_card(card, entry["options"]):
            info_success(card.name, "Successfully processed card")

        end_time = time.time()
        if (end_time - start_time) * 1000 < 100 and i < len(card_names) - 1:
            sleep(0.1)


def process_card(card: Card, options):
    # Check layout of card
    if card.layout not in supported_layouts:
        info_fail(card.name, "Layout not supported")
        return False

    # Cleansed card name for saving file
    cleansed_name = card.name.replace("//", "--")

    # Folders
    target_folder_path = f_documents + "/" + card.set.upper()
    target_file_path = target_folder_path + "/" + card.collector_number + " - " + cleansed_name
    target_file_full_path = target_file_path + ".idml"

    # Setup and extract preset
    os.makedirs(target_folder_path, exist_ok=True)
    with zipfile.ZipFile(f_preset, "r") as archive:
        archive.extractall("data/memory")

    # General operations
    if "fba" in options:
        if options["fba"] in ["front", "both"]:
            card_layout_full_body_art(id_general_front, card)
        if options["fba"] in ["back", "both"]:
            card_layout_full_body_art(id_general_back, card)

    if card.layout not in double_faced_layouts:
        card_delete_backside(id_general_back)

    if card.layout in ["normal", "class", "saga"]:
        card_fill(card, id_general_front, card.layout)
    elif card.layout in double_faced_layouts:
        card_layout_double_faced([id_general_front, id_general_back])

        set_modal(card, [id_general_front, id_general_back], card.layout)

        card_fill(card.card_faces[0], id_general_front, card.layout)
        card_fill(card.card_faces[1], id_general_back, card.layout)
    elif card.layout in ["split"]:
        card_layout_split(id_general_front)

        card_fill(card.card_faces[0], id_general_front_st, card.layout)
        card_fill(card.card_faces[1], id_general_front_sb, card.layout)
    elif card.layout in ["adventure"]:
        card_layout_adventure(id_general_front)

        id_adventure_right = id_general_front.copy()
        id_adventure_right[ids.ORACLE_TEXT_T] = id_general_front_adventure[ids.ADVENTURE_ORACLE_TEXT_R_T]
        id_adventure_right[ids.ORACLE_TEXT_O] = id_general_front_adventure[ids.ADVENTURE_ORACLE_TEXT_R_O]

        id_adventure_left = id_general_front_adventure.copy()
        id_adventure_left[ids.ORACLE_TEXT_T] = id_adventure_left[ids.ADVENTURE_ORACLE_TEXT_L_T]

        card_fill(card.card_faces[1], id_adventure_left, card.layout)
        card_fill(card.card_faces[0], id_adventure_right, card.layout)
    elif card.layout in ["token", "emblem"]:
        card_layout_token(id_general_front, card)

        card_fill(card, id_general_front, card.layout)

    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    if utility_file_exists(target_file_full_path):
        os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    return True


def card_fill(card: Card, id_set, layout):
    types = utility_get_card_types(card)

    # Check if basic
    if "Basic" in types and "Land" in types:
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
        set_oracle_text(card, id_set, align="left")
    else:
        set_oracle_text(card, id_set)

    # Value
    set_value(card, id_set)

    # Artist
    set_artist(card, id_set)

    # Collector Information
    set_collector_information(card, id_set)

    # Set
    set_set(card, id_set)


def process_print(card_names):
    list_of_cards = []

    for i, entry in enumerate(card_names):
        card = Card.get_card_object(entry)
        if card is None:
            continue

        for j in range(0, int(entry["amount"])):
            if card.layout in double_faced_layouts:
                list_of_cards.insert(0, card)
            else:
                list_of_cards.append(card)

    # Folders
    target_folder_path = f_print
    for filename in os.listdir(target_folder_path):
        file_path = os.path.join(target_folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    app = win32com.client.Dispatch("InDesign.Application.2022")

    handled_cards = []

    for i, page in enumerate(list(utility_divide_chunks(list_of_cards, 9))):
        target_file_path = target_folder_path + "/" + str(i)
        target_file_full_path = target_file_path + ".idml"

        os.makedirs(target_folder_path, exist_ok=True)
        with zipfile.ZipFile(f_preset_print, "r") as archive:
            archive.extractall("data/memory_print")

        for j, card in enumerate(page):
            name = utility_cleanse_id_name(card)

            # Convert to PDF
            if card.id not in handled_cards:
                utility_cardfile_to_pdf(app, card)
                handled_cards.append(card.id)

            # Frontside
            insert_pdf(card, id_general_print_front[ids.SPREAD], id_general_print_front[ids.PRINTING_FRAME_O][j],
                       f_pdf + "/" + card.set.upper(), name)

            # Backside
            if card.layout in double_faced_layouts:
                modulo = j % 3
                carry = int(j / 3)
                result = carry * 3 + (2 - modulo)
                insert_pdf(card, id_general_print_back[ids.SPREAD],
                           id_general_print_back[ids.PRINTING_FRAME_O][result],
                           f_pdf + "/" + card.set.upper(), name, page_number=2)

        shutil.make_archive(target_file_path, "zip", "data/memory_print")
        if utility_file_exists(target_file_full_path):
            os.remove(target_file_full_path)
        os.rename(target_file_path + ".zip", target_file_path + ".idml")
        shutil.rmtree("data/memory_print")


def main(argv):
    mode = ""
    deck = ""

    try:
        opts, args = getopt.getopt(argv, "m:d:", ["mode=", "deck="])
    except getopt.GetoptError:
        info_fail("[ProxKy]", "Invalid command line options")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-d", "--deck"):
            deck = arg

    if mode == "standard":
        cards = process_decklist("data/decks/" + deck + ".txt")
        process_cards(cards)
        process_print(cards)

        shutil.rmtree("data/memory")
    elif mode == "generate_id":
        utility_generate_all_ids()


if __name__ == '__main__':
    main(sys.argv[1:])
