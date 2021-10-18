class Card:
    card_faces = []
    name = ""
    type_line = ""
    mana_cost = ""
    colors = []
    oracle_text = ""
    power = ""
    toughness = ""
    artist = ""
    collector_number = ""
    set = ""
    rarity = ""

    def __init__(self, args: dict):
        super().__init__()

        if "name" in args:
            self.name = args["name"]
        if "type_line" in args:
            self.type_line = args["type_line"]
        if "mana_cost" in args:
            self.mana_cost = args["mana_cost"]
        if "colors" in args:
            self.colors = args["colors"]
        if "oracle_text" in args:
            self.oracle_text = args["oracle_text"]
        if "power" in args:
            self.power = args["power"]
        if "toughness" in args:
            self.toughness = args["toughness"]
        if "artist" in args:
            self.artist = args["artist"]
        if "collector_number" in args:
            self.collector_number = args["collector_number"]
        if "set" in args:
            self.set = args["set"]
        if "rarity" in args:
            self.rarity = args["rarity"]
