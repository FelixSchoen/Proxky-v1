import math
import os
import re
import shutil
import xml.etree.ElementTree
import zipfile

import variables
from info import info_fail
from variables import *


def utility_get_card_types(card):
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))
    return types


def utility_split_string_along_regex(string, *matchers: ([str], str, str), standard_category="type",
                                     standard_identifier="normal"):
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
            result.append((working_string, standard_category, standard_identifier))
            working_string = ""
        else:
            # Split into two parts
            part_one = working_string[:current_span[0]]
            part_two = working_string[current_span[0]:]

            # Everything before match is normal, remove it first
            rectifier = 0
            if current_span[0] > 0:
                result.append((part_one, standard_category, standard_identifier))
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


def utility_make_object_transparent(element, opacity, mode="Fill"):
    transparency = xml.etree.ElementTree.Element(mode + "TransparencySetting")
    blending = xml.etree.ElementTree.Element("BlendingSetting")
    blending.set("Opacity", str(opacity))
    transparency.append(blending)
    element.append(transparency)


def utility_nested_reminder_text(text_array):
    array_to_return = []

    for element in text_array:
        if element[2] != "reminder":
            array_to_return.append(element)
        else:
            returned_array = utility_split_string_along_regex(element[0], *regex_template_mana,
                                                              standard_identifier="reminder")
            array_to_return.extend(returned_array)

    return array_to_return


def utility_file_exists(path):
    return os.path.exists(path)


def utility_vector_bounding_box(path, filename):
    tree = xml.etree.ElementTree.parse(path + "/" + filename + ".svg")
    values = tree.getroot().attrib["viewBox"].split(" ")
    return float(values[2]), float(values[3])


def utility_indesign_get_coordinates(element):
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


def utility_indesign_set_y_coordinates(indesign_object, set_to):
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


def utility_indesign_shift_y_coordinates(indesign_object, shift_by):
    top_left = indesign_object.find(".//PathPointType[1]")
    top_right = indesign_object.find(".//PathPointType[4]")
    bottom_left = indesign_object.find(".//PathPointType[2]")
    bottom_right = indesign_object.find(".//PathPointType[3]")

    set_to = []

    for i, point in enumerate([top_left, top_right, bottom_left, bottom_right]):
        x_coordinate, y_coordinate = point.attrib["Anchor"].split(" ")
        set_to.append(float(y_coordinate) + shift_by[i])

    return utility_indesign_set_y_coordinates(indesign_object, set_to)


def utility_sort_mana_array(mana_array):
    mana_array.sort(key=lambda x: mana_types.index(x))


def utility_mana_cost_to_color_array(mana_cost):
    color_array = []
    for entry in mana_cost:
        if entry in mana_types and entry not in color_array:
            color_array.append(entry)
    utility_sort_mana_array(color_array)
    return color_array


def utility_cardfile_to_pdf(app, card):
    cleansed_name = card.name.replace("//", "--")
    input_folder_path = f_documents + "/" + card.set.upper()
    input_file_path = input_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".idml"
    output_folder_path = f_pdf + "/" + card.set.upper()
    output_file_path = output_folder_path + "/" + card.collector_number + " - " + cleansed_name + ".pdf"

    return_code = ""

    if utility_file_exists(output_file_path):
        return_code = FLAG_FILE_EXISTS

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    myDoc = app.Open(input_file_path)

    profile = app.PreflightProfiles.Item(1)
    process = app.PreflightProcesses.Add(myDoc, profile)
    process.WaitForProcess()
    results = process.processResults

    if "None" not in results:
        # Fix errors
        script = open("script.jsx")
        app.DoScript(script.read(), 1246973031, variables.resize_array)

        process.WaitForProcess()
        results = process.processResults

        # Check if problems were resolved
        if "None" not in results:
            info_fail(card.name, "Error while running preflight")
            myDoc.Close(1852776480)
            return FLAG_PREFLIGHT_FAIL

    myPDFPreset = app.PDFExportPresets.Item(7)
    idPDFType = 1952403524
    myDoc.Export(idPDFType, output_file_path, False, myPDFPreset)
    myDoc.Close(1852776480)

    if return_code == "":
        return_code = FLAG_OK

    return return_code


def utility_divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def utility_cleanse_id_name(card):
    cleansed_name = card.name.replace("//", "--")
    return card.collector_number + " - " + cleansed_name


def utility_generate_ids(name, spread, root_element, mode="standard"):
    """
    :param name: Name of the ID set to generate
    :param spread: Which spread to check the IDs on
    :param root_element: Root XML to search in, e.g. for split use only the split element as root
    :param mode: Which mode to generate IDs for, e.g. different treatment for split and double sided cards
    :return: None
    For the names, each entry consists of a string to match in the actual document, the internal ID to match it to, a
    boolean that states whether it is a text box or not or a component to extract.
    """
    global tree
    if mode != "printing":
        tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + spread + ".xml")
        base_tree = tree
        if root_element is not None:
            tree = tree.find(".//*[@Name='" + root_element + "']")
    else:
        tree = xml.etree.ElementTree.parse("data/memory_print/Spreads/Spread_" + spread + ".xml")

    # IDs base case
    names_base = [
        # Groups
        (id_names.GROUP_NORMAL, ids.GROUP_NORMAL_O, "root"),
        (id_names.GROUP_HEADER, ids.GROUP_HEADER_O),

        # Header
        (id_names.TYPE_ICON, ids.TYPE_ICON_O),
        (id_names.TITLE, ids.TITLE_T, "ParentStory"),
        (id_names.TYPE_LINE, ids.TYPE_LINE_T, "ParentStory"),
        (id_names.MANA_COST, ids.MANA_COST_T, "ParentStory"),
        (id_names.COLOR_INDICATOR_TOP, ids.COLOR_INDICATOR_TOP_O),
        (id_names.COLOR_INDICATOR_TOP, ids.GRADIENTS_O, "FillColor"),
        (id_names.COLOR_INDICATOR_BOT, ids.GRADIENTS_O, "FillColor"),

        # Body
        (id_names.ORACLE, ids.ORACLE_T, "ParentStory"),
        (id_names.ORACLE, ids.ORACLE_O),

        # Footer
        (id_names.COLOR_INDICATOR_BOT, ids.COLOR_INDICATOR_BOT_O),
        (id_names.VALUE, ids.VALUE_T, "ParentStory"),
        (id_names.VALUE, ids.VALUE_O),
        (id_names.ARTIST_INFORMATION, ids.ARTIST_INFORMATION_T, "ParentStory"),
        (id_names.ARTIST_INFORMATION, ids.ARTIST_INFORMATION_O),
        (id_names.COLLECTOR_INFORMATION, ids.COLLECTOR_INFORMATION_T, "ParentStory"),
        (id_names.COLLECTOR_INFORMATION, ids.COLLECTOR_INFORMATION_O),
        (id_names.ARTWORK, ids.ARTWORK_O),
        (id_names.BACKDROP, ids.BACKDROP_O),
    ]

    # IDs to add for standard cards
    names_standard = [
        # Groups
        (id_names.GROUP_SPLIT, ids.GROUP_SPLIT_O, "base_tree"),
        (id_names.GROUP_PLANESWALKER, ids.GROUP_PLANESWALKER_O),
        (id_names.GROUP_ADVENTURE, ids.GROUP_ADVENTURE_O),

        (id_names.MODAL, ids.MODAL_T, "ParentStory"),
        (id_names.MODAL, ids.MODAL_O),

        (id_names.PLANESWALKER_VALUE_1, ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (id_names.PLANESWALKER_VALUE_2, ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (id_names.PLANESWALKER_VALUE_3, ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (id_names.PLANESWALKER_VALUE_4, ids.PLANESWALKER_VALUE_T, "ParentStory"),
        (id_names.PLANESWALKER_VALUE_1, ids.PLANESWALKER_VALUE_O),
        (id_names.PLANESWALKER_VALUE_2, ids.PLANESWALKER_VALUE_O),
        (id_names.PLANESWALKER_VALUE_3, ids.PLANESWALKER_VALUE_O),
        (id_names.PLANESWALKER_VALUE_4, ids.PLANESWALKER_VALUE_O),
        (id_names.PLANESWALKER_ORACLE_1, ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (id_names.PLANESWALKER_ORACLE_2, ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (id_names.PLANESWALKER_ORACLE_3, ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (id_names.PLANESWALKER_ORACLE_4, ids.PLANESWALKER_ORACLE_NUMBERED_T, "ParentStory"),
        (id_names.PLANESWALKER_ORACLE_1, ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (id_names.PLANESWALKER_ORACLE_2, ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (id_names.PLANESWALKER_ORACLE_3, ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (id_names.PLANESWALKER_ORACLE_4, ids.PLANESWALKER_ORACLE_NUMBERED_O),
        (id_names.PLANESWALKER_ORACLE_FINAL, ids.PLANESWALKER_ORACLE_FINAL_T, "ParentStory"),
        (id_names.PLANESWALKER_ORACLE_FINAL, ids.PLANESWALKER_ORACLE_FINAL_O),
    ]

    # IDs to add for adventure cards
    names_adventure = [(id_names.ADVENTURE_TYPE_ICON, ids.TYPE_ICON_O),
                       (id_names.ADVENTURE_TITLE, ids.TITLE_T, "ParentStory"),
                       (id_names.ADVENTURE_TYPE_LINE, ids.TYPE_LINE_T, "ParentStory"),
                       (id_names.ADVENTURE_MANA_COST, ids.MANA_COST_T, "ParentStory"),
                       (id_names.ADVENTURE_COLOR_INDICATOR, ids.COLOR_INDICATOR_TOP_O),
                       (id_names.ADVENTURE_COLOR_INDICATOR, ids.GRADIENTS_O, "FillColor"),
                       # A bit hacky
                       (id_names.ADVENTURE_COLOR_INDICATOR, ids.GRADIENTS_O, "FillColor"),
                       (id_names.ADVENTURE_ORACLE_LEFT, ids.ADVENTURE_ORACLE_LEFT_T, "ParentStory"),
                       (id_names.ADVENTURE_ORACLE_LEFT, ids.ADVENTURE_ORACLE_LEFT_O),
                       (id_names.ADVENTURE_ORACLE_RIGHT, ids.ADVENTURE_ORACLE_RIGHT_T, "ParentStory"),
                       (id_names.ADVENTURE_ORACLE_RIGHT, ids.ADVENTURE_ORACLE_RIGHT_O)
                       ]

    # IDs to use for printing
    names_printing = [
        (id_names.P_FRAME + " 1", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 2", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 3", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 4", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 5", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 6", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 7", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 8", ids.PRINTING_FRAME_O),
        (id_names.P_FRAME + " 9", ids.PRINTING_FRAME_O),
    ]

    names = names_base

    # Modes
    if mode == "standard":
        names.extend(names_standard)
    elif mode == "adventure":
        names = names_adventure
    elif mode == "printing":
        names = names_printing

    with open("data/ids.txt", "a") as f:
        print("id_general_" + name + " = {", file=f)
        print("\"" + ids.SPREAD + "\": " + "\"" + spread + "\",", file=f)

        entries = []

        for name in names:
            name_to_search_for = name[0]

            element = tree.find(".//*[@Name='" + name_to_search_for + "']")

            # Text box
            if len(name) > 2:
                # Get ID of root element
                if name[2] == "root":
                    to_add = "\"" + tree.attrib["Self"] + "\","
                # Get ID of element outside of current tree
                elif name[2] == "base_tree":
                    element = base_tree.find(".//*[@Name='" + name_to_search_for + "']")
                    to_add = "\"" + element.attrib["Self"] + "\","
                elif name[2] == "FillColor":
                    to_add = "\"" + element.attrib[name[2]].split("/")[1] + "\","
                else:
                    to_add = "\"" + element.attrib[name[2]] + "\","
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
                print(previous_entry + ": " + str(carry) + ",", file=f)
                carry = []

            if duplicates[key] <= 1:
                print(entry[0] + ": " + entry[1], file=f)
            else:
                previous_entry = entry[0]
                carry.append(entry[1].split(",")[0].replace("\"", ""))

            if i == len(entries) - 1 and len(carry) > 1:
                print(previous_entry + ": " + str(carry) + ",", file=f)

        print("}", file=f)


def utility_generate_all_ids():
    front_id = "uce"
    back_id = "u2069"
    print_front_id = "ue7"
    print_back_id = "u11d"

    open('data/ids.txt', 'w').close()

    with zipfile.ZipFile(file_template, "r") as archive:
        archive.extractall("data/memory")
    with zipfile.ZipFile(file_print, "r") as archive:
        archive.extractall("data/memory_print")

    utility_generate_ids("front", front_id, id_names.GROUP_NORMAL)
    utility_generate_ids("split_top_front", front_id, id_names.GROUP_SPLIT_TOP, mode="split")
    utility_generate_ids("split_bot_front", front_id, id_names.GROUP_SPLIT_BOT, mode="split")
    utility_generate_ids("front_adventure", front_id, id_names.GROUP_NORMAL, mode="adventure")
    utility_generate_ids("back", back_id, id_names.GROUP_NORMAL)
    utility_generate_ids("print_front", print_front_id, None, mode="printing")
    utility_generate_ids("print_back", print_back_id, None, mode="printing")

    # shutil.rmtree("data/memory")
    # shutil.rmtree("data/memory_print")
