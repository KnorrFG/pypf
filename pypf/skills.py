import re
from collections import defaultdict

from attrdict import AttrDict


def make_skill(name, mod, untrained): 
    return AttrDict({
        "name": name, 
        "ability": mod,
        "untrained": untrained})


all_skills = [make_skill(name, mod, untrained) for name, mod, untrained in [
    ("Acrobatics", "Dex", True),
    ("Appraise", "Int", True),
    ("Bluff", "Cha", True),
    ("Climb", "Str", True),
    ("Craft", "Int", True),
    ("Diplomacy", "Cha", True),
    ("Disable device", "Dex", True),
    ("Disguise", "Cha", True),
    ("Escape artist", "Dex", True),
    ("Fly", "Dex", True),
    ("Handle animal", "Cha", False),
    ("Heal", "Wis", True),
    ("Intimidate", "Cha", True),
    ("Knowledge (arcana)", "Int", False),
    ("Knowledge (dungeoneering)", "Int", False),
    ("Knowledge (engineering)", "Int", False),
    ("Knowledge (geography)", "Int", False),
    ("Knowledge (history)", "Int", False),
    ("Knowledge (local)", "Int", False),
    ("Knowledge (nature)", "Int", False),
    ("Knowledge (nobility)", "Int", False),
    ("Knowledge (planes)", "Int", False),
    ("Knowledge (religion)", "Int", False),
    ("Linguistics", "Int", False),
    ("Perception", "Wis", True),
    ("Perform", "Cha", True),
    ("Profession", "Wis", False),
    ("Ride", "Dex", True),
    ("Sense motive", "Wis", True),
    ("Sleight of hand", "Dex", False),
    ("Spellcraft", "Int", False),
    ("Stealth", "Dex", True),
    ("Survival", "Wis", True),
    ("Swim", "Str", True),
    ("Use magic device", "Cha", False)
]]

skill_names = [s.name for s in all_skills]


def make_class_skill_mask(*names):
    invalid_names = [n for n in names if not any(re.match(n, skname)
                                                 for skname in skill_names)]
    if invalid_names:
        raise ValueError(f"Not a skill: {invalid_names}")

    return [True if any(re.match(pattern, skill.name) for pattern in names)
            else False
            for skill in all_skills]


class_skill_masks = {
    "Sorcerer": make_class_skill_mask(
        'Appraise', 'Bluff', 'Craft', 'Fly', 'Intimidate',
        r'Knowledge \(arcana\)',
        'Profession', 'Spellcraft', 'Use magic device'),
    "Draconic": make_class_skill_mask('Perception'),
    "Dragon Disciple": make_class_skill_mask(
        'Diplomacy', 'Escape artist', 'Fly', 'Knowledge.*', 'Perception',
        'Spellcraft'),
    "Twilight Assassin": make_class_skill_mask(
        'Acrobatics', 'Bluff', 'Climb', 'Disguise', 'Escape artist',
        'Intimidate', 'Perception', 'Sense motive', 'Sleight of hand',
        'Stealth', 'Swim', r'Knowledge \(local\)'),
    "Druid": make_class_skill_mask(
        "Climb", "Craft", "Fly", "Handle animal", "Heal", 
        r"Knowledge \(geography\)", r"Knowledge \(nature\)", "Perception",
        "Profession", "Ride", "Spellcraft", "Survival", "Swim")
}


def combined_class_skill_mask(classes):
    masks = [class_skill_masks[class_] for class_ in classes]
    return list(map(any, zip(*masks)))


def make_skill_table(input_dict, abilities, *classes):
    wrong_keys = [key for key in input_dict if key not in skill_names]
    if wrong_keys:
        print("The following keys are probably misstyped:",
              wrong_keys)
        exit(1)
    if not all(cl in class_skill_masks for cl in classes):
        print("You either misstyped your class, or it is not yet supported")
        exit(1)

    in_dict = defaultdict(int, input_dict)
    contained_mask = (True if in_dict[skill.name] > 0 or skill.untrained
                      else False for skill in all_skills)
    mask = combined_class_skill_mask(classes)
    return {skill.name: in_dict[skill.name]
                        + abilities[skill.ability]['Mod']
                        + (3 if is_cs and in_dict[skill.name] else 0)
            for skill, is_cs, contained in zip(all_skills, mask, contained_mask)
            if contained}
