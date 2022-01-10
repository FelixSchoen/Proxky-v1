from src.utility.variables import mana_types


def get_card_types(card):
    types = card.type_line.split("—")
    types = list(filter(None, types[0].split(" ")))
    return types


def cleanse_name_with_id(card):
    cleansed_name = card.name.replace("//", "--")
    return card.collector_number + " - " + cleansed_name


def sort_mana_array(mana_array):
    mana_array.sort(key=lambda x: mana_types.index(x))


def mana_cost_to_color_array(mana_cost):
    color_array = []
    for entry in mana_cost:
        if entry in mana_types and entry not in color_array:
            color_array.append(entry)
    sort_mana_array(color_array)
    return color_array