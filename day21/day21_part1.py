# --- Day 21: Allergen Assessment ---
# You reach the train's last stop and the closest you can get to your vacation island without getting wet. There aren't even any boats here, but nothing can stop you now: you build a raft. You just need a few days' worth of food for your journey.
#
# You don't speak the local language, so you can't read any ingredients lists. However, sometimes, allergens are listed in a language you do understand.
# You should be able to use this information to determine which ingredient contains which allergen and work out which foods are safe to take with you on your trip.
#
# You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's ingredients list followed by some or all of the allergens the food contains.
#
# Each allergen is found in exactly one ingredient. Each ingredient contains zero or one allergen.
# Allergens aren't always marked; when they're listed (as in (contains nuts, shellfish) after an ingredients list),
# the ingredient that contains each listed allergen will be somewhere in the corresponding ingredients list.
# However, even if an allergen isn't listed, the ingredient that contains that allergen could still be present:
# maybe they forgot to label it, or maybe it was labeled in a language you don't know.
#
# For example, consider the following list of foods:
#
# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)
# The first food in the list has four ingredients (written in a language you don't understand): mxmxvkd, kfcds, sqjhc, and nhms.
# While the food might contain other allergens, a few allergens the food definitely contains are listed afterward: dairy and fish.
#
# The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
# In the above example, none of the ingredients kfcds, nhms, sbzzf, or trh can contain an allergen.
# Counting the number of times any of these ingredients appear in any ingredients list produces 5: they all appear once each except sbzzf, which appears twice.
#
# Determine which ingredients cannot possibly contain any of the allergens in your list. How many times do any of those ingredients appear?
#
# To begin, get your puzzle input.

# ok, so it's about sets of possibilities..
# any given set of ingredients has a corresponding list of allergens
# for each allergen, those ingredients are the possibilities
# if we get a subsequent list of ingredients for the same allergen then the list narrows to the matching subset
# once we have a single ingredient that is known to contain a given allergen, that ingredient is no longer a candidate for any other allergen
from typing import List


class FoodDB:
    def __init__(self):
        self.ingredient_counts = dict()
        self.allergen_possibilities = dict()
        self.known_allergens = dict()

    def part1_answer(self):
        """
        a total of the number of appearances of any ingredient which could not possibly have an allergen in it
        """
        suspect_list = set()
        for this_allergen in self.allergen_possibilities:
            suspect_list.update(self.allergen_possibilities[this_allergen])
        print(f"Final suspect ingredient list is ({len(suspect_list)}): {suspect_list}")

        result = 0
        for this_ingredient in self.ingredient_counts.keys():
            # is this ingredient in any of the allergen suspect lists ?
            if this_ingredient not in suspect_list:
                result += self.ingredient_counts[this_ingredient]
                print(
                    f"part1: including {self.ingredient_counts[this_ingredient]} instances of {this_ingredient}"
                )
            else:
                print(
                    f"part1: ignoring {self.ingredient_counts[this_ingredient]} instances of {this_ingredient}"
                )
        print(f"Final result for part1 is : {result}")
        return result

    def update_certain_knowledge(self):
        """
        look for any allergen possibilities where there is only a single possibility and update the state accordingly
        """
        NeedToCheck = True
        while NeedToCheck:
            NeedToCheck = False

            # look through each allergen_possibility, ignoring anything in known_allergens
            for this_allergen in [
                a
                for a in self.allergen_possibilities.keys()
                if a not in self.known_allergens
            ]:
                possibility_count = len(self.allergen_possibilities[this_allergen])
                if 1 == possibility_count:
                    the_definite_ingredient = list(
                        self.allergen_possibilities[this_allergen]
                    )[0]
                    # ok, let's go boys.. we've got a new fact!
                    print(
                        f"We now know that ingredient {the_definite_ingredient} has the allergen {this_allergen}"
                    )
                    # we can add this to known_allergens list
                    self.known_allergens[this_allergen] = the_definite_ingredient

                    # we must remove this ingredient as an option from all the other allergens in the known universe
                    for target_allergen in self.allergen_possibilities:
                        if this_allergen != target_allergen:
                            if (
                                the_definite_ingredient
                                in self.allergen_possibilities[target_allergen]
                            ):
                                self.allergen_possibilities[target_allergen].remove(
                                    the_definite_ingredient
                                )
                    # and we need to go round again..
                    NeedToCheck = True

    def print(self):
        """
        Output what we know
        """
        print(
            f"FoodDB: {len(self.allergen_possibilities.keys())} allergens, {len(self.known_allergens.keys())} identified, {len(self.ingredient_counts.keys())} ingredients"
        )

    def add_one_recipe(
        self, ingredient_list: List[str], allergen_list: List[str], verbose=False
    ):
        """
        Adding some observed facts about the food universe
        we know that any one of the ingredients is a candidate for any one of the allergens
        """
        # 1) Add the number of times we have seen this ingredient
        for this_ingredient in ingredient_list:
            if this_ingredient not in self.ingredient_counts:
                self.ingredient_counts[this_ingredient] = 1
            else:
                self.ingredient_counts[this_ingredient] += 1

        # 2) next, for each allergen we now have a candidate list
        # ignoring anything that we have already assigned..
        the_possible_ingredients = set(ingredient_list)
        for this_allergen in allergen_list:
            # this might be the first time we're seeing this allergen
            if this_allergen not in self.allergen_possibilities:
                self.allergen_possibilities[this_allergen] = set(
                    the_possible_ingredients
                )
                if verbose:
                    print(
                        f"Initial possibilities for ingredients containing {this_allergen}: {the_possible_ingredients}"
                    )
            else:
                # we already have a list..
                new_possibilities = self.allergen_possibilities[
                    this_allergen
                ].intersection(the_possible_ingredients)
                if verbose:
                    print(
                        f"Updating possibilities for ingredients containing {this_allergen} with {the_possible_ingredients}"
                    )
                    print(
                        f"Current possibilities for ingredients containing {this_allergen} are {self.allergen_possibilities[this_allergen]}"
                    )
                    print(
                        f"Updated possibilities for ingredients containing {this_allergen}: {new_possibilities}"
                    )
                self.allergen_possibilities[this_allergen] = new_possibilities


def load_food_info(filename: str):
    """
    Load a food file and return the resulting FoodDB object
    """
    result = FoodDB()

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # we have one food line..
                # format is abc def ghi (contains fish[, peanuts])
                # we need 2 lists before we can add them to the food database object
                paren_idx = this_line.find("(")
                if -1 == paren_idx:
                    raise RuntimeError(
                        f"This line doesn't have a paren in it: {this_line}"
                    )
                ingredients = this_line[:paren_idx]
                allergens = this_line[paren_idx:]
                # split the ingredient list into bits..
                ingredient_list = [
                    x.strip() for x in ingredients.split(" ") if x.strip() != ""
                ]
                # more sanity checking
                if not allergens.startswith("(contains ") or not allergens.endswith(
                    ")"
                ):
                    raise RuntimeError(
                        f"Weird allergens list doesn't have the boilerplate: {allergens}"
                    )
                allergens = allergens[9:-1]
                allergen_list = [
                    x.strip() for x in allergens.split(",") if x.strip() != ""
                ]
                # print(                    f"inp:{this_line}\ning:{ingredients}\ninl:{ingredient_list}\nalg:{allergens}\nall:{allergen_list}"                )
                result.add_one_recipe(ingredient_list, allergen_list)

    # and now we can be certain about some stuff..
    result.update_certain_knowledge()

    return result


# main loop, load the file and get the FoodDB object
filename = "input.txt"
fdb = load_food_info(filename)
fdb.print()
fdb.part1_answer()
