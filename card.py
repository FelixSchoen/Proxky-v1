from helper import helper_mana_cost_to_color_array


class Card:

    def __init__(self, args: dict):
        super().__init__()

        self.name = ""
        self.layout = ""
        self.mana_cost = ""
        self.type_line = ""
        self.colors = []
        self.color_identity = []
        self.produced_mana = []
        self.keywords = []
        self.oracle_text = ""
        self.power = ""
        self.toughness = ""
        self.loyalty = ""
        self.artist = ""
        self.collector_number = ""
        self.set = ""
        self.rarity = ""
        self.card_faces = []
        self.image_uris = []

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
        if "produced_mana" in args:
            self.produced_mana = args["produced_mana"]
        if "keywords" in args:
            self.keywords = args["keywords"]
        if "card_faces" in args:
            for card_face in args["card_faces"]:
                self.card_faces.append(Card(card_face))
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
        if "set" in args:
            self.set = args["set"]
        if "rarity" in args:
            self.rarity = args["rarity"]
        if "image_uris" in args:
            self.image_uris = args["image_uris"]

        for face in self.card_faces:
            if len(face.colors) == 0:
                if face.type_line in ["Land"]:
                    face.colors.extend(self.produced_mana)
                if self.layout in ["split"]:
                    face.colors.extend(helper_mana_cost_to_color_array(face.mana_cost))
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
