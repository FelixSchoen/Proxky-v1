import math
import os
from os import listdir

import requests

import utility
from utility import utility_sort_mana_array, utility_indesign_set_y_coordinates, utility_indesign_shift_y_coordinates, \
    utility_get_card_types
from info import info_warn, info_normal
from insert_xml import *
from insert_xml import insert_multi_font_text
from variables import ids, f_artwork, f_artwork_downloaded, f_icon_card_types, COORDINATE_TOP_ORACLE, \
    VALUE_MODAL_HEIGHT, COORDINATE_BOT_ORACLE, mana_mapping, \
    regex_template_planeswalker, color_mapping, FONT_SANS, FONT_SANS_STYLE, regex_template_regular, regex_add_mana, \
    regex_card_name, VALUE_SPACING_PLANESWALKER


def set_artwork(card, id_set):
    if ids.ARTWORK_O not in id_set:
        return

    id_spread = id_set[ids.SPREAD]
    id_artwork = id_set[ids.ARTWORK_O]

    path_cn = f_artwork + "/" + card.set.upper() + "/" + str(card.collector_number) + " - " + card.name
    path_name = f_artwork + "/" + card.set.upper() + "/" + card.name
    path_auto = f_artwork_downloaded + "/" + card.set.upper() + "/" + card.name + ".jpg"
    image_type = "na"
    filename = ""

    for possible_image_type in image_types:
        if utility_file_exists(path_cn + "." + possible_image_type):
            filename = str(card.collector_number) + " - " + card.name
            image_type = possible_image_type
            break
        elif utility_file_exists(path_name + "." + possible_image_type):
            filename = card.name
            image_type = possible_image_type
            break

    if image_type == "na":
        # Check if alternative artwork exists
        paths = os.walk(f_artwork)
        for path in paths:
            for file in path[2]:
                file_name = re.match(regex_card_name, file).group("name").split(".")[0]
                if card.name == file_name:
                    info_warn(card.name, "Artwork from different set exists: [{}]".format(path[0][-3:]))
                    break

        if "art_crop" not in card.image_uris:
            info_fail(card.name, "No artwork on Scryfall")
            return

        response = requests.get(card.image_uris["art_crop"])

        if response.status_code != 200:
            info_fail(card.name, "Could not download artwork")
            return

        os.makedirs(f_artwork_downloaded + "/" + card.set.upper(), exist_ok=True)
        with open(path_auto, "wb") as handler:
            handler.write(response.content)
        insert_graphic(card, id_spread, id_artwork, f_artwork_downloaded + "/" + card.set.upper(), card.name,
                       type_file="jpg",
                       mode_scale_image="fit_priority_x", mode_align_vertical="top")
    else:
        insert_graphic(card, id_spread, id_artwork, f_artwork + "/" + card.set.upper(), filename, type_file=image_type,
                       mode_scale_image="fit_priority_x", mode_align_vertical="top")


def set_type_icon(card, id_set):
    id_spread = id_set[ids.SPREAD]
    id_type = id_set[ids.TYPE_ICON_O]

    # Get types of card
    types = utility_get_card_types(card)
    if "Legendary" in types:
        types.remove("Legendary")
    if "Basic" in types:
        types.remove("Basic")
    if "Token" in types:
        types.remove("Token")
    if "Snow" in types:
        types.remove("Snow")

    if len(types) != 1:
        card_type = "Multiple"
    else:
        card_type = types[0]

    if not utility_file_exists(f_icon_card_types + "/" + card_type.lower() + ".svg"):
        info_warn(card.name, "No icon for card type")
    else:
        insert_graphic(card, id_spread, id_type, f_icon_card_types, card_type.lower())


def set_card_name(card, id_set):
    id_name = id_set[ids.TITLE_T]

    insert_content(id_name, card.name)


def set_type_line(card, id_set):
    id_type_line = id_set[ids.TYPE_LINE_T]

    insert_content(id_type_line, card.type_line.replace("—", "•"))


def set_mana_cost(card, id_set):
    id_mana_cost = id_set[ids.MANA_COST_T]

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mapping = "".join([mana_mapping["{" + m + "}"] for m in mana])
    if len(mapping) > 5:
        cutoff_point = math.floor(len(mapping) / 2)
        mapping = mapping[:cutoff_point] + "\n" + mapping[cutoff_point:]
    insert_content(id_mana_cost, mapping)


def set_modal(card, id_sets, modal_type="modal"):
    for i, id_set in enumerate(id_sets):
        face = card.card_faces[(i + 1) % 2]

        caps_type = ""

        if modal_type == "modal_dfc":
            caps_type = "MODAL"
        elif modal_type == "transform":
            caps_type = "TRANSFORM"
        elif modal_type == "meld":
            caps_type = "MELD"
        elif modal_type == "double_faced_token":
            caps_type = "FLIP"

        line_to_insert = caps_type + " — " + face.type_line.replace("Creature — ", "").replace("—", "•")

        if len(face.mana_cost) > 0:
            line_to_insert += " • " + face.mana_cost

        if "Land" in face.type_line:
            match = re.search(regex_add_mana, face.oracle_text)
            if match:
                line_to_insert += " • " + match.group("match")

        line_to_insert = "{◄}\t" + line_to_insert + "\t{►}"

        insert_multi_font_text(line_to_insert, id_set[ids.MODAL_T], align="center", font=FONT_SANS,
                               style=FONT_SANS_STYLE, size="4.5", regex=regex_template_regular)


def set_color_bar(card, id_set):
    id_gradients = id_set[ids.GRADIENTS_O]

    distance = 1.5
    colors_to_apply = card.colors

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    utility_sort_mana_array(colors_to_apply)

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


def set_planeswalker_text(card, id_set):
    planeswalker_text = utility_split_string_along_regex(card.oracle_text, *regex_template_planeswalker)
    amount_abilities = sum(x[2] == "loyalty" for x in planeswalker_text)

    if amount_abilities > 4:
        info_fail(card.name, "Too many abilities")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
    modal = tree.find(".//TextFrame[@Self='" + id_set[ids.MODAL_O] + "']")

    amount_textboxes = amount_abilities
    top_y_coordinate = COORDINATE_TOP_ORACLE

    if modal.attrib["Visible"] == "true":
        top_y_coordinate += VALUE_MODAL_HEIGHT

    total_height = COORDINATE_BOT_ORACLE + abs(top_y_coordinate)

    text_boxes = [[(id_set[ids.PLANESWALKER_VALUE_T][0], id_set[ids.PLANESWALKER_VALUE_O][0]),
                   (id_set[ids.PLANESWALKER_ORACLE_NUMBERED_T][0], id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][0])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][1], id_set[ids.PLANESWALKER_VALUE_O][1]),
                   (id_set[ids.PLANESWALKER_ORACLE_NUMBERED_T][1], id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][1])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][2], id_set[ids.PLANESWALKER_VALUE_O][2]),
                   (id_set[ids.PLANESWALKER_ORACLE_NUMBERED_T][2], id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][2])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][3], id_set[ids.PLANESWALKER_VALUE_O][3]),
                   (id_set[ids.PLANESWALKER_ORACLE_NUMBERED_T][3], id_set[ids.PLANESWALKER_ORACLE_NUMBERED_O][3])]]

    # Insert pre text
    if planeswalker_text[0][2] != "loyalty":
        tf = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_O] + "']")
        tfp = tf.find(".//TextFramePreference[1]")
        tfp.set("VerticalJustification", "CenterAlign")

        text_boxes.insert(0, [(id_set[ids.ORACLE_T], id_set[ids.ORACLE_O])])
        amount_textboxes += 1
        insert_multi_font_text(planeswalker_text[0][0], id_set[ids.ORACLE_T], align="left")
        planeswalker_text = planeswalker_text[1:]

    potential_additional_box = utility_split_string_along_regex(planeswalker_text[-1][0], ("\n", "type", "break"))
    if len(potential_additional_box) > 1:
        tf = tree.find(".//TextFrame[@Self='" + id_set[ids.PLANESWALKER_ORACLE_FINAL_O] + "']")
        tfp = tf.find(".//TextFramePreference[1]")
        tfp.set("VerticalJustification", "CenterAlign")

        text_boxes = text_boxes[0:amount_textboxes]
        text_boxes.append([(id_set[ids.PLANESWALKER_ORACLE_FINAL_T], id_set[ids.PLANESWALKER_ORACLE_FINAL_O])])
        amount_textboxes += 1

        insert_string = ""

        for i in range(2, len(potential_additional_box)):
            insert_string += potential_additional_box[i][0]

        insert_multi_font_text(insert_string, id_set[ids.PLANESWALKER_ORACLE_FINAL_T], align="left")

        planeswalker_text.pop()
        planeswalker_text.append(potential_additional_box[0])

    box_size = (total_height - VALUE_SPACING_PLANESWALKER * (amount_textboxes - 1)) / amount_textboxes
    shifter = 1 if amount_textboxes > amount_abilities else 0

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    for i, level in enumerate(text_boxes):
        j = i - shifter

        for pair in level:
            object_box = tree.find(".//TextFrame[@Self='" + pair[1] + "']")

            if i < amount_textboxes:
                object_box.set("Visible", "true")
                # if i % 2 == 1:
                #     object_box.set("FillColor", "Color/Grey")

                top_left = object_box.find(".//PathPointType[1]")
                x_coordinate, y_coordinate = top_left.attrib["Anchor"].split(" ")
                y_coordinate = float(y_coordinate)

                utility_indesign_set_y_coordinates(object_box,
                                                   [y_coordinate, y_coordinate,
                                                    y_coordinate + box_size, y_coordinate + box_size])
                shift_length = (box_size + VALUE_SPACING_PLANESWALKER) * i
                shift_coordinates = [shift_length, shift_length, shift_length, shift_length]
                utility_indesign_shift_y_coordinates(object_box, shift_coordinates)
            else:
                object_box.set("Visible", "false")

        if 0 <= j < amount_abilities:
            insert_multi_font_text(planeswalker_text[2 * j][0][:-1].replace("−", "-"), level[0][0])
            insert_multi_font_text(planeswalker_text[2 * j + 1][0].rstrip(), level[1][0])

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def set_oracle_text(card, id_set, align=None):
    if ids.ORACLE_T not in id_set:
        return
    if align is not None:
        insert_multi_font_text(card.oracle_text, id_set[ids.ORACLE_T], flavor_text=card.flavor_text, align=align)
    else:
        insert_multi_font_text(card.oracle_text, id_set[ids.ORACLE_T], flavor_text=card.flavor_text)


def set_value(card, id_set):
    id_value = id_set[ids.VALUE_T]

    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string = value_string.replace(" ", "")

        insert_content(id_value, value_string)

    if card.loyalty != "":
        insert_content(id_value, card.loyalty)


def set_artist(card, id_set):
    if ids.ARTIST_T not in id_set:
        return

    id_artist = id_set[ids.ARTIST_T]

    insert_content(id_artist, card.artist)


def set_collector_information(card, id_set):
    id_collector_information = id_set[ids.COLLECTOR_INFORMATION_T]

    string_to_insert = card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0]
    if len(card.side) > 0:
        string_to_insert = card.side.upper() + " • " + string_to_insert

    insert_content(id_collector_information, string_to_insert)
