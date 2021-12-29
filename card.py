import json
import re
import urllib

import requests

from info import info_fail
from settings import api_url
from utility import utility_mana_cost_to_color_array
from variables import regex_add_mana, regex_mana, double_sided_layouts


class Card:

    def __init__(self, args: dict):
        super().__init__()

        self.id = ""
        self.name = ""
        self.layout = ""
        self.mana_cost = ""
        self.type_line = ""
        self.colors = []
        self.color_identity = []
        self.keywords = []
        self.produced_mana = []
        self.keywords = []
        self.oracle_text = ""
        self.power = ""
        self.toughness = ""
        self.loyalty = ""
        self.artist = ""
        self.collector_number = ""
        self.flavor_text = ""
        self.set = ""
        self.rarity = ""
        self.card_faces = []
        self.image_uris = []
        self.side = ""

        if "id" in args:
            self.id = args["id"]
        if "name" in args:
            self.name = args["name"]
        if "layout" in args:
            self.layout = args["layout"]
        if "type_line" in args:
            self.type_line = args["type_line"]
        if "mana_cost" in args:
            self.mana_cost = args["mana_cost"]
        if "colors" in args:
            self.colors = args["colors"]
        if "color_identity" in args:
            self.color_identity = args["color_identity"]
        if "keywords" in args:
            self.keywords = args["keywords"]
        if "produced_mana" in args:
            self.produced_mana = args["produced_mana"]
        if "keywords" in args:
            self.keywords = args["keywords"]
        if "card_faces" in args:
            for i, card_face in enumerate(args["card_faces"]):
                face = Card(card_face)

                if self.layout in double_sided_layouts:
                    if i == 0:
                        face.side = "front"
                    else:
                        face.side = "back"

                self.card_faces.append(face)
        if "oracle_text" in args:
            self.oracle_text = args["oracle_text"]
        if "power" in args:
            self.power = args["power"]
        if "toughness" in args:
            self.toughness = args["toughness"]
        if "loyalty" in args:
            self.loyalty = args["loyalty"]
        if "artist" in args:
            self.artist = args["artist"]
        if "collector_number" in args:
            self.collector_number = args["collector_number"]
        if "flavor_text" in args:
            self.flavor_text = args["flavor_text"]
        if "rarity" in args:
            self.rarity = args["rarity"]
        if "set" in args:
            self.set = args["set"]
        if "image_uris" in args:
            self.image_uris = args["image_uris"]

        if len(self.colors) == 0:
            if "Land" in self.type_line:
                self.colors.extend(self.produced_mana)

        # Add meld card as backside
        if self.layout in ["meld"] and "all_parts" in args:
            parts = args["all_parts"]
            meld_result_dict = next(obj for obj in parts if obj["component"] == "meld_result")

            if self.id != meld_result_dict["id"]:
                dictionary = dict()
                dictionary["id"] = meld_result_dict["id"]
                meld_result = Card.get_card_object(dictionary)
                self.card_faces.append(self)
                self.card_faces.append(meld_result)

        # Manual fix for faces
        for face in self.card_faces:
            if len(face.image_uris) == 0:
                face.image_uris = self.image_uris

            if len(face.colors) == 0:
                if "Land" in face.type_line:
                    if len(face.produced_mana) > 1:
                        face.colors.extend(face.produced_mana)
                    else:
                        # Search for oracle text additions
                        matches = re.finditer(regex_add_mana, face.oracle_text)
                        for match in matches:
                            produced_mana = match.group("prod")

                            colors = []
                            color_matches = re.finditer(regex_mana, produced_mana)
                            for color_match in color_matches:
                                colors.append(color_match.group("mana"))

                            face.colors.extend(colors)
                            face.produced_mana.extend(colors)
                        # Sort and format mana
                        face.colors = utility_mana_cost_to_color_array(face.colors)
                        face.produced_mana = utility_mana_cost_to_color_array(face.colors)
                if self.layout in ["split", "adventure"]:
                    face.colors.extend(utility_mana_cost_to_color_array(face.mana_cost))

            if len(face.keywords) == 0:
                face.keywords = self.keywords

            if face.artist == "":
                face.artist = self.artist

            if face.collector_number == "":
                face.collector_number = self.collector_number

            if face.set == "":
                face.set = self.set

            if face.rarity == "":
                face.rarity = self.rarity

    def __repr__(self) -> str:
        return "[{}]".format(self.name)

    @staticmethod
    def get_card_object(dictionary):
        if "id" in dictionary:
            response = requests.get(
                api_url + "/cards/" + urllib.parse.quote(dictionary["id"]))
        elif "set" in dictionary:
            response = requests.get(
                api_url + "/cards/named?exact=" + urllib.parse.quote(dictionary["name"]) + "&set=" + urllib.parse.quote(
                    dictionary["set"]))
        else:
            response = requests.get(
                api_url + "/cards/named?exact=" + urllib.parse.quote(dictionary["name"]))

        # Check status code
        if response.status_code != 200:
            info_fail(dictionary["name"], "Could not fetch card")
            return None

        return Card(json.loads(response.text))
