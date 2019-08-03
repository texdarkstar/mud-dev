from typeclasses.scripts import Script


class RecipeScript(Script):
    def at_script_creation(self):
        self.persistent = False
        self.interval = 0

        self.recipes = {
            "steel": {
                "typeclass": "typeclasses.resources.Steel",
                "components": {
                    "iron": 2,
                    },
            },
            "leather strip": {
                "typeclass": "typeclasses.components.LeatherStrip",
                "components": {
                    "leather": 2,
                    },
            },
            "small steel blade": {
                "typeclass": "typeclasses.components.SmallSteelBlade",
                "components": {
                    "steel": 5,
                    },
            },
            "large steel blade": {
                "typeclass": "typeclasses.components.LargeSteelBlade",
                "components": {
                    "steel": 10,
                    },
            },
            "steel hilt": {
                "typeclass": "typeclasses.components.SteelHilt",
                "components": {
                    "steel": 2,
                    },
            },
            "steel dagger": {
                "typeclass": "typeclasses.weapons.SteelDagger",
                "components": {
                    "small steel blade": 1,
                    "steel hilt": 1,
                    "leather strip": 1
                },
            },
        }

    def at_server_reload(self):
        self.stop()
