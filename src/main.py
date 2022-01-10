import getopt
import re
import shutil
import time
import sys
import zipfile
from time import sleep

import win32com.client

from src.cards import *
from src.utility.util_magic import get_card_types, cleanse_name_with_id
from src.utility.util_generate_id import generate_all_ids
from src.utility.util_info import info_success, info_fail
from src.utility.util_misc import does_file_exist, divide_into_chunks
from src.utility.util_xml import convert_card_to_pdf, insert_pdf
from src.utility.variables import *


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
                    if option_match.group("type") in ["set", "id", "cn"]:
                        dictionary[option_match.group("type")] = option_match.group("id")
                    else:
                        options[option_match.group("type")] = option_match.group("id")

            cards.append(dictionary)

    return cards


def process_cards(card_names):
    for i, entry in enumerate(card_names):
        start_time = time.time()

        card_object = Card.get_card_object(entry)
        if card_object is None:
            continue

        if process_card(card_object, entry["options"]):
            info_success(card_object.name, "Successfully processed cards")

        end_time = time.time()
        if (end_time - start_time) * 1000 < 100 and i < len(card_names) - 1:
            sleep(0.1)


def process_card(card_object: Card, options):
    # Check layout of cards
    if card_object.layout not in supported_layouts:
        info_fail(card_object.name, "Layout not supported")
        return False

    # Cleansed cards name for saving file
    cleansed_name = card_object.name.replace("//", "--")

    # Folders
    target_folder_path = f_documents + "/" + card_object.set.upper()
    target_file_path = target_folder_path + "/" + card_object.collector_number + " - " + cleansed_name
    target_file_full_path = target_file_path + ".idml"

    # Setup and extract preset
    os.makedirs(target_folder_path, exist_ok=True)
    with zipfile.ZipFile(file_template, "r") as archive:
        archive.extractall("data/memory")

    # General operations
    if "tba" in options:
        if options["tba"] in ["front", "both"]:
            card_layout_transparent_body_art(id_general_front)
        if options["tba"] in ["back", "both"]:
            card_layout_transparent_body_art(id_general_back)
    elif "fba" in options:
        if options["fba"] in ["front", "both"]:
            card_layout_full_body_art(id_general_front)
        if options["fba"] in ["back", "both"]:
            card_layout_full_body_art(id_general_back)

    if card_object.layout not in double_sided_layouts:
        card_delete_backside(id_general_back)

    if card_object.layout in ["normal", "class", "saga"]:
        card_fill(card_object, id_general_front, card_object.layout)
    elif card_object.layout in double_sided_layouts:
        card_layout_double_faced([id_general_front, id_general_back])

        set_modal(card_object, [id_general_front, id_general_back], card_object.layout)

        card_fill(card_object.card_faces[0], id_general_front, card_object.layout)
        card_fill(card_object.card_faces[1], id_general_back, card_object.layout)
    elif card_object.layout in ["split", "flip"]:
        card_layout_split(id_general_front)

        card_fill(card_object.card_faces[0], id_general_split_top_front, card_object.layout)
        card_fill(card_object.card_faces[1], id_general_split_bot_front, card_object.layout)
    elif card_object.layout in ["adventure"]:
        card_layout_adventure(id_general_front)

        id_adventure_right = id_general_front.copy()
        id_adventure_right[ids.ORACLE_T] = id_general_front_adventure[ids.ADVENTURE_ORACLE_RIGHT_T]
        id_adventure_right[ids.ORACLE_O] = id_general_front_adventure[ids.ADVENTURE_ORACLE_RIGHT_O]

        id_adventure_left = id_general_front_adventure.copy()
        id_adventure_left[ids.ORACLE_T] = id_adventure_left[ids.ADVENTURE_ORACLE_LEFT_T]

        card_fill(card_object.card_faces[1], id_adventure_left, card_object.layout)
        card_fill(card_object.card_faces[0], id_adventure_right, card_object.layout)
    elif card_object.layout in ["token", "emblem"]:
        card_layout_token(id_general_front, card_object)

        card_fill(card_object, id_general_front, card_object.layout)

    # Repackage preset, remove old files and rename to correct extension
    shutil.make_archive(target_file_path, "zip", "data/memory")
    if does_file_exist(target_file_full_path):
        os.remove(target_file_full_path)
    os.rename(target_file_path + ".zip", target_file_path + ".idml")

    return True


def card_fill(card_object: Card, id_set, layout_spec):
    types = get_card_types(card_object)

    # Check if basic
    if "Basic" in types and "Land" in types:
        card_layout_no_oracle_text(id_set, card_object)

    # Value
    if "Planeswalker" in types:
        card_layout_planeswalker(id_set)
        if card_object.loyalty == "":
            card_layout_no_value(id_set)
    elif card_object.power == "" and card_object.toughness == "":
        card_layout_no_value(id_set)

    # Artwork
    set_artwork(card_object, id_set)

    # Type Icon
    set_type_icon(card_object, id_set)

    # Card Name
    set_card_name(card_object, id_set)

    # Type Line
    set_type_line(card_object, id_set)

    # Mana Cost
    set_mana_cost(card_object, id_set)

    # Color Bar
    set_color_indicator(card_object, id_set)

    # Oracle Text
    if "Planeswalker" in types:
        set_planeswalker_text(card_object, id_set)
    elif layout_spec in ["adventure"]:
        set_oracle_text(card_object, id_set, align="left")
    else:
        set_oracle_text(card_object, id_set)

    # Value
    set_value(card_object, id_set)

    # Artist
    set_artist(card_object, id_set)

    # Collector Information
    set_collector_information(card_object, id_set)


def process_print(card_names):
    list_of_cards = []

    for i, entry in enumerate(card_names):
        card_object = Card.get_card_object(entry)
        if card_object is None:
            continue

        for j in range(0, int(entry["amount"])):
            if card_object.layout in double_sided_layouts:
                list_of_cards.insert(0, card_object)
            else:
                list_of_cards.append(card_object)

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

    for i, page in enumerate(list(divide_into_chunks(list_of_cards, 8))):
        target_file_path = target_folder_path + "/" + str(i)
        target_file_full_path = target_file_path + ".idml"

        os.makedirs(target_folder_path, exist_ok=True)
        with zipfile.ZipFile(file_print, "r") as archive:
            archive.extractall("data/memory_print")

        for j, card_object in enumerate(page):
            name = cleanse_name_with_id(card_object)

            # Convert to PDF
            if card_object.id not in handled_cards:
                convert_card_to_pdf(app, card_object)
                handled_cards.append(card_object.id)

            # Frontside
            insert_pdf(card_object, id_general_print_front[ids.SPREAD], id_general_print_front[ids.PRINTING_FRAME_O][j],
                       f_pdf + "/" + card_object.set.upper(), name)

            # Backside
            if card_object.layout in double_sided_layouts:
                insert_pdf(card_object, id_general_print_back[ids.SPREAD],
                           id_general_print_back[ids.PRINTING_FRAME_O][j],
                           f_pdf + "/" + card_object.set.upper(), name, page_number=2)

        shutil.make_archive(target_file_path, "zip", "data/memory_print")
        if does_file_exist(target_file_full_path):
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

        # shutil.rmtree("data/memory")
    elif mode == "generate_id":
        generate_all_ids()


if __name__ == '__main__':
    main(sys.argv[1:])
