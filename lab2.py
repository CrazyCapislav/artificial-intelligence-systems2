from pyswip import Prolog


def get_main_characters_from_prolog(prolog):
    characters = []
    for sol in prolog.query("main_character(Character)"):
        characters.append(sol['Character'])
    return characters


def parse_character(input_str, characters):
    for character in characters:
        if character.lower() in input_str.lower():
            return character
    return None


def get_items_from_prolog(main_character, prolog):
    items = []
    if main_character == 'kratos':
        query = "god_slayer_weapon(Item)"
    elif main_character == 'arthas':
        query = "lich_king_attributes(Item)"
    else:
        return items

    for sol in prolog.query(query):
        items.append(sol['Item'])

    return items


def get_goals_from_prolog(main_character, prolog):
    goals = []
    if main_character == 'kratos':
        query = "kratos_goal(Goal)"
    elif main_character == 'arthas':
        query = "arthas_goal(Goal)"
    else:
        return goals

    for sol in prolog.query(query):
        goals.append(sol['Goal'])

    return goals


def parse_goal(input_str, main_character, prolog):
    goals = get_goals_from_prolog(main_character, prolog)
    for goal in goals:
        if goal in input_str.lower():
            return goal
    return None


def recommend_actions(goal, prolog, owned_item):
    if goal.startswith("obtain_"):
        goal = goal.replace("obtain_", "")
    elif goal.startswith("defeat_"):
        goal = goal.replace("defeat_", "")
    else:
        goal = None

    keeper_query = f"keeperOf(Keeper, {goal})"
    keeper = None
    for sol in prolog.query(keeper_query):
        keeper = sol['Keeper']
        break

    if keeper:
        print(f"System: The item '{goal}' is currently held by {keeper}. Defeat {keeper} to obtain it.")
        print(f"System: After defeating {keeper}, you can proceed to obtain {goal}.")
        return

    weakness_query = f"hasWeakness({goal}, WeaknessItem)"
    weakness_item = None
    for sol in prolog.query(weakness_query):
        weakness_item = sol['WeaknessItem']
        break

    guards_query = f"guardOf(Guard, {goal})"
    guards = []
    for sol in prolog.query(guards_query):
        guards.append(sol['Guard'])

    if weakness_item:
        print(f"System: {goal.capitalize()} has a weakness. You need to obtain the item: {weakness_item}.")
        if weakness_item == owned_item:
            print(f"You already obtain the item: {weakness_item}.")
        else:
            keeper_query = f"keeperOf(Keeper, {weakness_item})"
            for sol in prolog.query(keeper_query):
                keeper = sol['Keeper']
                print(
                    f"System: The item '{weakness_item}' is currently held by {keeper}. Defeat {keeper} to obtain it.")

    if guards:
        print(f"System: Before defeating {goal.capitalize()}, you need to defeat all the guards.")
        for guard in guards:
            print(f"System: Defeat {guard} first.")
            weakness_query = f"hasWeakness({guard}, WeaknessItem)"
            weakness_item = None
            for sol in prolog.query(weakness_query):
                weakness_item = sol['WeaknessItem']
                break

            guards_query = f"guardOf(Guard, {guard})"
            guards = []
            for sol in prolog.query(guards_query):
                guards.append(sol['Guard'])

            if weakness_item:
                print(f"System: {guard.capitalize()} has a weakness. You need to obtain the item: {weakness_item}.")
                if weakness_item == owned_item:
                    print(f"You already obtain the item: {weakness_item}.")
                else:
                    keeper_query = f"keeperOf(Keeper, {weakness_item})"
                    for sol in prolog.query(keeper_query):
                        keeper = sol['Keeper']
                        print(
                            f"System: The item '{weakness_item}' is currently held by {keeper}. Defeat {keeper} to obtain it.")

            if guards:
                print(f"System: Before defeating {goal.capitalize()}, you need to defeat all the guards.")
                for guard in guards:
                    print(f"System: Defeat {guard} first.")

    print(f"System: Finally, you can proceed to defeat {goal.capitalize()}.")


if __name__ == "__main__":
    prolog = Prolog()
    prolog.consult('lab2.pl')

    characters = get_main_characters_from_prolog(prolog)

    print(f"System: Choose your main character ({', '.join(characters)}):")
    character_input = input("User: ").lower()
    main_character = parse_character(character_input, characters)
    if not main_character:
        print("System: Character not recognized. Please try again.")
        exit()

    items = get_items_from_prolog(main_character, prolog)
    print(f"System: What items does {main_character.capitalize()} have? List of available items: {', '.join(items)}")
    owned_item = input("User: ")

    available_goals = get_goals_from_prolog(main_character, prolog)
    print(
        f"System: What is the goal of {main_character.capitalize()}? List of available goals: {', '.join(available_goals)}")

    goal_input = input("User: ")
    goal = parse_goal(goal_input, main_character, prolog)
    if not goal:
        print("System: Goal not recognized. Please try again.")
        exit()

    recommend_actions(goal, prolog, owned_item)
