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
    ("Handle", "Cha", False),
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

def make_class_skill_mask(*names):
    return [True if any(re.match(pattern, skill.name) for pattern in names) 
            else False
            for skill in all_skills]
            
class_skill_masks = {
    "Sorcerer": make_class_skill_mask(
        'Appraise', 'Bluff', 'Craft', 'Fly', 'Intimidate', 'Knowledge (arcana)',
        'Profession', 'Spellcraft', 'Use magic device'),
    "Draconic": make_class_skill_mask('Perception'),
    "Dragon Disciple": make_class_skill_mask(
        'Diplomacy', 'Escape artist', 'Fly', 'Knowledge.*', 'Perception', 
        'Spellcraft')
}

def combined_class_skill_mask(classes):
    masks = [class_skill_masks[class_] for class_ in classes]
    return list(map(any, zip(*masks)))


def make_skill_table(input_dict, abilities, *classes):
    in_dict = defaultdict(int, input_dict)
    contained_mask = (True if in_dict[skill.name] > 0 or skill.untrained 
                        else False for skill in all_skills)
    mask = combined_class_skill_mask(classes)
    return {skill.name: in_dict[skill.name] 
                        + abilities[skill.ability]['Mod']
                        + (3 if is_cs and in_dict[skill.name] else 0)
            for skill, is_cs, contained in zip(all_skills, mask, contained_mask)
            if contained}
