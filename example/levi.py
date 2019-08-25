import datasheet as ds
import pypf as pf

name = 'Levi'
sorc_lvl = 5
dd_lvl = 1
lvl = sorc_lvl + dd_lvl
caster_lvl = lvl - 1
abilities = pf.ability_table(14, 0, 
                          12, 0, 
                          15, 0, 
                          10, 0, 
                          12, 0, 
                          (16 + 2),  2) # first 2 by human, 2 by headband
concentration = caster_lvl + abilities.Cha.Mod
hp = (6 + 6 + 5 + 4 + 1 + 12 # Rolls
      + abilities.Con.Mod * lvl
      + lvl ) # Toughness bonus
bab = 2 + 0
cmb = bab + abilities.Str.Mod + 0 #special size mod

# A creature can also add any circumstance, deflection, dodge, insight, luck,
# morale, profane, and sacred bonuses to AC to its CMD. Any penalties to a
# creature’s AC also apply to its CMD. A flat-footed creature does Falset add its
# Dexterity bonus to its CMD.
cmd = (bab + 10 + abilities.Dex.Mod
       + 1 # Insect-helmet
       + 1) # Ring of deflection
fort = (1 # Sorc lvl 5
        + 1 # DD lvl 1
        + abilities.Con.Mod)
reflex = (1
          + 0 
          + abilities.Dex.Mod)
will = (4
        + 1
        + abilities.Wis.Mod)


def spdb(lvl): return pf.spells_per_day_bonus(abilities.Cha.Mod, lvl)
spells_per_day = {
    1: 6 + spdb(1),
    2: 4 + spdb(2),
    "Claws": 3 + abilities.Cha.Mod
}


nat_attacks = {
    "2 x Claws (Magic dmg)": {
        "Atk": bab + 1 + abilities.Str.Mod, # Weapon focus Nat. weapons bonus
        "Dmg": f"1d4 + {abilities.Str.Mod}"} # Will increase to 1d6 on bloodline lvl 7
}


nat_armor = (1 # Dragon resistances
                + 1) # DD lvl 1
stacking_ac = 1 #insect helmet
deflection = 1 # ring of deflection
AC = {
    "Abs": 10 + nat_armor + stacking_ac + deflection + abilities.Dex.Mod,
    "Touch": 10 + deflection + abilities.Dex.Mod,
    "Flat": 10 + deflection + stacking_ac + nat_armor}

skills = pf.make_skill_table({
    'Bluff': 1,
    'Fly': 3, 
    'Intimidate': 1,
    'Knowledge (arcana)': 5,
    'Perception': 6,
    'Spellcraft': 3,
    'Use magic device': 1,
    'Linguistics': 1,
    'Knowledge (planes)': 1
}, abilities, 'Sorcerer', 'Draconic', 'Dragon Disciple')

spells_by_level = [
    {'Dancing Lights':
        f'V,S; 1min 1-4 lights that can freely move. Range: {100 + 10 * caster_lvl} ft',
     'Detect Magic':
        f''' V,S; Range: 60ft cone; Dur: up to 3 rounds. R1: presence of magic auras;  
        R2: number and power of strongest; R3: strength and location of each aura. 
        DC 15 + spelllvl knowledge arcana check for spell school''',
     'Mage Hand': 
        f'V,S; Range: {25 + 5 * (caster_lvl // 2)} ; max obj weight: up to 5lbs',
     'Message': f'V,S,F; Range: {100 + (10 * caster_lvl)}ft; Duration {10 * caster_lvl} min',
     'Prestidigitation': 'V,S; Any sort of magical trick without much power',
     'Mending': 'V, S; Repair objects for 1d4'},
    {'Burning Hands': f'V,S; Range: 15ft cone; ST: Reflex halves; Dmg: 5d4+5',
     'Feather Fall': 
        f'V; Range {25 + 5 * (caster_lvl // 2)};Dur:{caster_lvl}; Fallspeed: 60ft/round',
     'Shield': 
        f'''V,S; Dur: {caster_lvl}min; negates magic missile; 
        +4AC (shield bonus (also vs touch))''',
     'Mage Armor': f'V,S,F; Dur: {caster_lvl}h; +4AC (armor bonus (also vs touch))',
     'Magic Missile':
        f''''V, S, {100 + 10 * caster_lvl}ft. Dmg 1d4+1/missile; 
        {1 + (caster_lvl // 2)} missiles. Hits ALWAY.'''
    },
    {'Flaming Sphere': 
        f'''V,S; d=5ft;Speed 30ft;Reflex negates; dmg: 3d6+3; Range: 
        {100 + 10 * caster_lvl}; Duration: 1 round per level; 
        moving the sphere is a movement action for the caster.''',
     'Resist Energy': 
        f'V, S, DF; duration: {10 * caster_lvl}min. Resist 10 vs chosen energy type',
     'Pyrotechnics':
        f'''V,S, M; dur: 1d4+1 rounds; range: 400ft + 40/lvl. Turns a fire into a 
        firework or a smoke cloud.  *Firework*: Creatures within 120ft and direct line 
        of sight become blinded. (Will negates, Spell resistance negates) 
        *SmokeCloud*: dur: {caster_lvl} rounds.All sight (even darkvision) is negated. 
        All within cloud take -4str and -4 dex. Duration starts after leaving the cloud. 
        Fortitude negates, Spellresistance doesn't apply'''
    }
]

feats = {
    'Combat Casting': 
        '+4 on concentration checks while casting defensively or grappled',
    'Eschew Materials': 
        "Don't need material components worth less than 1gp",
    'Spellfocus (Evo)': '+1 DC on saving throws vs my evocations',
    'Toughness': '+1 HP per lvl',
    'Weapon Focus Natural Weapons': '+1 on attack rolls with natural weapons',
    'Skilled': 'HUmans get one extra skillpoint per level',
    'Claws': 'Can grow claws',
    'Bloodline Arcana': '+1 dmg per die for firespells',
    'Dragon Resistance': '+1 Natural armor; resist fire 5'
}

items = {
    'Insect Helmet': '+1AC that stacks with mage armor',
    'Ring of Protection': '+1 Deflection Bonus',
    'Charisma Headband': '+2 Charisma',
    'Boots of vaulting': 
        '''Ignore an additional 10ft of falling distance when using acrobatics.
        Once per round as Free action gain a +10 bonus to jump. The jump is
        treated as if having a running start. +10 bonus on acrobatics check to
        avoid AOO after landing.''',
    'Shimmerrobe': 'Delay 50% of all dmg taken to the end of my next turn'
}


sheet = ds.Sheet('Levi', standalone=True)
sheet << '# Levi'
sheet << ds.HLayout((
            pf.md.long_table(skills, 'Name', caption="Skills", 
                             col_align=['right', 'center']), 
            ds.VLayout((
                pf.md.flat_table('Abs, Sorc, DD, Caster',
                                  lvl, sorc_lvl, dd_lvl, caster_lvl,
                                  caption='Level'),
                pf.md.table(abilities, "Ability"),
                pf.md.flat_table('Concent., HP, CMB, CMD, Fort, Ref, Will',
                                 concentration, hp, cmb, cmd, fort, reflex,
                                 will),
                ds.HLayout((
                    pf.md.flat_table(spells_per_day, 
                                     caption='Spells per day'),
                    pf.md.flat_table(AC, caption='AC'))),
                pf.md.table(nat_attacks, 'Weapon', caption='Natural attacks',
                            col_align=['right', 'center', 'center']),
                f'''
                    **Languages:** common, draconic  
                    Spell resistance DC for enemies: {10 + abilities.Cha.Mod} +
                    Spell-lvl (+ 1 for Evos) '''))))
sheet << '## Spells'
for i, spells in enumerate(spells_by_level):
    sheet << pf.md.long_table(spells, r_col_name='Effect', caption=f'Lvl {i}')
sheet << '## Feats'
sheet << pf.md.long_table(feats)
sheet << '## Items'
sheet << pf.md.long_table(items)
sheet.render()

