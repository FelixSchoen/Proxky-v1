import xml.etree
import zipfile

from src.utility.variables import id_names, ids, file_template, file_print


def generate_ids(name, spread, root_element, mode="standard"):
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
        (id_names.GROUP_FOOTER, ids.GROUP_FOOTER_O),

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

        (id_names.NAME, ids.NAME_T, "ParentStory"),
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

        # (id_names.MASK_COLOR_INDICATOR_BOT, ids.MASK_COLOR_INDICATOR_BOT_O),
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


def generate_all_ids():
    front_id = "uce"
    back_id = "u4122"
    print_front_id = "ue7"
    print_back_id = "u16c"

    open('data/ids.txt', 'w').close()

    with zipfile.ZipFile(file_template, "r") as archive:
        archive.extractall("data/memory")
    with zipfile.ZipFile(file_print, "r") as archive:
        archive.extractall("data/memory_print")

    generate_ids("front", front_id, id_names.GROUP_NORMAL)
    generate_ids("split_top_front", front_id, id_names.GROUP_SPLIT_TOP, mode="split")
    generate_ids("split_bot_front", front_id, id_names.GROUP_SPLIT_BOT, mode="split")
    generate_ids("front_adventure", front_id, id_names.GROUP_NORMAL, mode="adventure")
    generate_ids("back", back_id, id_names.GROUP_NORMAL)
    generate_ids("print_front", print_front_id, None, mode="printing")
    generate_ids("print_back", print_back_id, None, mode="printing")

    # shutil.rmtree("data/memory")
    # shutil.rmtree("data/memory_print")
