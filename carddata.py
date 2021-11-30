import os
from os import listdir

import requests

from helper import helper_sort_mana_array, helper_indesign_set_y_coordinates, helper_indesign_shift_y_coordinates, \
    helper_get_card_types
from info import info_warn, info_normal
from insert_xml import *
from insert_xml import insert_multi_font_text
from variables import ids, f_artwork, f_artwork_downloaded, f_icon_types, COORDINATE_TOP_ORACLE_TEXT, \
    VALUE_MODAL_HEIGHT, COORDINATE_BOT_ORACLE_TEXT, VALUE_DISTANCE_VALUE, mana_mapping, f_icon_set, \
    regex_planeswalker, color_mapping, font_sans, font_sans_style


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
        if helper_file_exists(path_cn + "." + possible_image_type):
            filename = str(card.collector_number) + " - " + card.name
            image_type = possible_image_type
            break
        elif not helper_file_exists(path_name + "." + possible_image_type):
            if any(helper_file_exists(f_artwork + "/" + possible_set + "/" + card.name + "." + possible_image_type) for
                   possible_set in listdir(f_artwork)):
                image_type = "other"
            continue
        else:
            filename = card.name
            image_type = possible_image_type
            break

    if image_type == "other":
        info_warn(card.name, "Artwork from different set exists")
        image_type = "na"

    if image_type == "na":
        info_normal(card.name, "No artwork exists, using Scryfall source")

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
    id_type = id_set[ids.TYPE_O]

    # Get types of card
    types = helper_get_card_types(card)
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

    if not helper_file_exists(f_icon_types + "/" + card_type.lower() + ".svg"):
        info_warn(card.name, "No icon for card type")
    else:
        insert_graphic(card, id_spread, id_type, f_icon_types, card_type.lower())


def set_card_name(card, id_set):
    id_name = id_set[ids.NAME_T]

    insert_value_content(id_name, card.name)


def set_type_line(card, id_set):
    id_type_line = id_set[ids.TYPE_LINE_T]

    insert_value_content(id_type_line, card.type_line.replace("—", "•"))


def set_mana_cost(card, id_set):
    id_mana_cost = id_set[ids.MANA_COST_T]

    mana = list(filter(None, [s.replace("{", "") for s in card.mana_cost.split("}")]))
    mapping = "".join([mana_mapping["{" + m + "}"] for m in mana])
    if len(mapping) > 5:
        mapping = mapping[:5] + "\n" + mapping[5:]
    insert_value_content(id_mana_cost, mapping)


def set_modal(card, id_sets, modal_type="modal"):
    for i, id_set in enumerate(id_sets):
        face = card.card_faces[(i + 1) % 2]

        caps_type = ""
        line_to_insert = ""

        if modal_type == "modal_dfc":
            caps_type = "MODAL"
        elif modal_type == "transform":
            caps_type = "TRANSFORM"

        line_to_insert = caps_type + " — " + face.type_line.replace("—", "•")

        if len(face.mana_cost) > 0:
            line_to_insert += " • " + face.mana_cost

        insert_multi_font_text(line_to_insert, id_set[ids.MODAL_T], align="center", font=font_sans, style=font_sans_style, size="5")


def set_color_bar(card, id_set):
    id_gradients = id_set[ids.GRADIENTS_O]

    distance = 1.5
    colors_to_apply = card.colors

    if len(colors_to_apply) == 0:
        colors_to_apply.append("C")
    if len(colors_to_apply) == 1:
        colors_to_apply.append(colors_to_apply[0])

    helper_sort_mana_array(colors_to_apply)

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
    planeswalker_text = helper_split_string_along_regex(card.oracle_text, *regex_planeswalker)
    amount_abilities = sum(x[2] == "loyalty" for x in planeswalker_text)

    if amount_abilities > 4:
        info_fail(card.name, "Too many abilities")
        return

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")
    modal = tree.find(".//Group[@Self='" + id_set[ids.GROUP_MODAL_O] + "']")

    amount_textboxes = amount_abilities
    top_y_coordinate = COORDINATE_TOP_ORACLE_TEXT

    if modal.attrib["Visible"] == "true":
        top_y_coordinate += VALUE_MODAL_HEIGHT

    total_height = COORDINATE_BOT_ORACLE_TEXT + abs(top_y_coordinate)

    if card.loyalty == "":
        total_height += VALUE_DISTANCE_VALUE

    text_boxes = [[(id_set[ids.PLANESWALKER_VALUE_T][0], id_set[ids.PLANESWALKER_VALUE_O][0]),
                   (id_set[ids.PLANESWALKER_TEXT_T][0], id_set[ids.PLANESWALKER_TEXT_O][0])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][1], id_set[ids.PLANESWALKER_VALUE_O][1]),
                   (id_set[ids.PLANESWALKER_TEXT_T][1], id_set[ids.PLANESWALKER_TEXT_O][1])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][2], id_set[ids.PLANESWALKER_VALUE_O][2]),
                   (id_set[ids.PLANESWALKER_TEXT_T][2], id_set[ids.PLANESWALKER_TEXT_O][2])],

                  [(id_set[ids.PLANESWALKER_VALUE_T][3], id_set[ids.PLANESWALKER_VALUE_O][3]),
                   (id_set[ids.PLANESWALKER_TEXT_T][3], id_set[ids.PLANESWALKER_TEXT_O][3])]]

    if planeswalker_text[0][2] != "loyalty":
        tf = tree.find(".//TextFrame[@Self='" + id_set[ids.ORACLE_TEXT_O] + "']")
        tfp = tf.find(".//TextFramePreference[1]")
        tfp.set("VerticalJustification", "CenterAlign")

        text_boxes.insert(0, [(id_set[ids.ORACLE_TEXT_T], id_set[ids.ORACLE_TEXT_O])])
        amount_textboxes += 1
        insert_multi_font_text(planeswalker_text[0][0], id_set[ids.ORACLE_TEXT_T], align="left")
        planeswalker_text = planeswalker_text[1:]

    potential_additional_box = helper_split_string_along_regex(planeswalker_text[-1][0], ("\n", "type", "break"))
    if len(potential_additional_box) > 1:
        tf = tree.find(".//TextFrame[@Self='" + id_set[ids.PLANESWALKER_ORACLE_O] + "']")
        tfp = tf.find(".//TextFramePreference[1]")
        tfp.set("VerticalJustification", "CenterAlign")

        text_boxes = text_boxes[0:amount_textboxes]
        text_boxes.append([(id_set[ids.PLANESWALKER_ORACLE_T], id_set[ids.PLANESWALKER_ORACLE_O])])
        amount_textboxes += 1

        insert_string = ""

        for i in range(2, len(potential_additional_box)):
            insert_string += potential_additional_box[i][0]

        insert_multi_font_text(insert_string, id_set[ids.PLANESWALKER_ORACLE_T], align="Left")

        planeswalker_text.pop()
        planeswalker_text.append(potential_additional_box[0])

    step_size = total_height / amount_textboxes
    shifter = 1 if amount_textboxes > amount_abilities else 0

    tree = xml.etree.ElementTree.parse("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")

    for i, level in enumerate(text_boxes):
        j = i - shifter

        for pair in level:
            object_box = tree.find(".//TextFrame[@Self='" + pair[1] + "']")

            if i < amount_textboxes:
                object_box.set("Visible", "true")
                if i % 2 == 1:
                    object_box.set("FillColor", "Color/Grey")

                top_left = object_box.find(".//PathPointType[1]")
                x_coordinate, y_coordinate = top_left.attrib["Anchor"].split(" ")
                y_coordinate = float(y_coordinate)

                helper_indesign_set_y_coordinates(object_box,
                                                  [y_coordinate, y_coordinate,
                                                   y_coordinate + step_size, y_coordinate + step_size])
                shift_coordinates = [step_size * i, step_size * i, step_size * i, step_size * i]
                helper_indesign_shift_y_coordinates(object_box, shift_coordinates)
            else:
                object_box.set("Visible", "false")

        if 0 <= j < amount_abilities:
            insert_multi_font_text(planeswalker_text[2 * j][0][:-1].replace("−", "-"), level[0][0])
            insert_multi_font_text(planeswalker_text[2 * j + 1][0].rstrip(), level[1][0])

    tree.write("data/memory/Spreads/Spread_" + id_set[ids.SPREAD] + ".xml")


def set_default_oracle_text(card, id_set, align="center"):
    if ids.ORACLE_TEXT_T not in id_set:
        return
    insert_multi_font_text(card.oracle_text, id_set[ids.ORACLE_TEXT_T], align)


def set_value(card, id_set):
    if ids.VALUE_T not in id_set:
        return

    id_value = id_set[ids.VALUE_T]

    if card.power != "" or card.toughness != "":
        value_string = card.power + " / " + card.toughness
        if len(card.power) > 1 or len(card.toughness) > 1:
            value_string = value_string.replace(" ", "")

        insert_value_content(id_value, value_string)

    if card.loyalty != "":
        insert_value_content(id_value, card.loyalty)


def set_artist(card, id_set):
    if ids.ARTIST_T not in id_set:
        return

    id_artist = id_set[ids.ARTIST_T]

    insert_value_content(id_artist, card.artist)


def set_collector_information(card, id_set):
    if ids.COLLECTOR_INFORMATION_T not in id_set:
        return

    id_collector_information = id_set[ids.COLLECTOR_INFORMATION_T]

    insert_value_content(id_collector_information,
                         card.collector_number.zfill(3) + " • " + card.set.upper() + " • " + card.rarity.upper()[0])


def set_set(card, id_set):
    if ids.SET_O not in id_set:
        return

    id_spread = id_set[ids.SPREAD]
    id_set_icon = id_set[ids.SET_O]

    if not helper_file_exists(f_icon_set + "/" + card.set.lower() + ".svg"):
        if card.set.lower()[0] == "t" and helper_file_exists(f_icon_set + "/" + card.set.lower()[1:] + ".svg"):
            info_warn(card.name, "Assuming that card is token")
            insert_graphic(card, id_spread, id_set_icon, f_icon_set, card.set.lower()[1:])
        else:
            info_warn(card.name, "No icon for set: " + card.set.lower())
    else:
        insert_graphic(card, id_spread, id_set_icon, f_icon_set, card.set.lower())
