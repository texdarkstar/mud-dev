from commands.command import Command
from evennia import search_script, create_object, create_script


class CmdCraft(Command):
    '''Attempt to craft a recipe based on the components.
        You can add or remove multiple items if the name is comma separated
        craft <add/remove> <item>[,<item>,<item>]
        craft <confirm/cancel>
    '''
    key = 'craft'
    locks = 'cmd:all()'


    def func(self):
        args = self.args.strip().split()
        if not args:
            self.caller.msg("Craft what?")
            return

        items = list()
        action = args.pop(0).lower()

        if action not in ["add", "remove", "recipe", "cancel"]:
            self.caller.msg("Invalid syntax.")
            return

        if action in ["add", "remove"]:
            args = " ".join(args).split(",")

            for item in args:
                items.append(item.strip())

           
        self.items = items
        self.action = action

        caller = self.caller
        recipe_script = search_script("recipescript", typeclass="world.recipescript.RecipeScript")

        try:
            recipe_script = recipe_script[0]
        except IndexError:
            recipe_script = create_script(key="recipescript", typeclass="world.recipescript.RecipeScript")


        if self.action == "add":
            for _item in self.items:
                item = caller.search(_item, location=caller)
                if not item:
                    continue

                if item.tags.get(category="craftable"):
                    caller.db.craft_stack.append(item)
                    caller.msg("Added '%s' to the crafting stack..." % item)

        elif self.action == "remove":
            pass
        elif self.action == "cancel":
            pass
        elif self.action == "recipe":
            inv = []
            recipe_name = " ".join(self.args.strip().split()[1:])

            # caller.msg(recipe_name)
            for item in caller.db.craft_stack:
                tag = item.tags.get(category="craftable")

                if type(tag) is type(""):
                    inv.append(tag.lower())

                elif type(tag) is type([]):
                    inv.extend(t.lower() for t in tag)

            found_recipe = None

            for recipe_key in recipe_script.recipes.keys():
                if recipe_key.lower() == recipe_name.lower():
                    found_recipe = recipe_script.recipes[recipe_key]
                    break


            if not found_recipe:
                caller.msg("No such recipe.")
                return

            recipe = found_recipe
            missing = []

            for comp in recipe["components"]:
                needed_count = recipe["components"][comp]
                inv_count = inv.count(comp)

                if inv_count < needed_count:
                    # missing ingredients
                    missing.append((needed_count - inv_count, comp))
                else:
                    # we have all we need of this ingredient
                    pass

            if len(missing) > 0:
                for row in missing:
                    caller.msg("You are missing %s %s." % row)

                return

            obj = create_object(key=recipe_name, typeclass=recipe['typeclass'], location=caller)

            # for component in recipe['components']:

                # for c in range(recipe['components'][component]):
                    # remove component from caller
            for item in self.caller.db.craft_stack:
                # if item.tags.get(component, category="craftable"):
                    item.at_craft_use(caller, obj)
                    item.delete()

                            # _item = caller.search("#%i" % item.id, use_dbref=True, quiet=True)
                            # if _item:
                                # _item.pop().delete()

            caller.msg("You crafted %s." % obj)
            caller.db.craft_stack = list()