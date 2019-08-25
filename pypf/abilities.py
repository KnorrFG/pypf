from attrdict import AttrDict


def ability_mod(val):
    offset = 10 if val >= 10 else 11
    return int((val - offset) / 2)


def ability_detail(base, bonus):
    final = base + bonus
    return {
        "Base": base, 
        "Bonus": bonus,
        "Final": final, 
        "Mod": ability_mod(final)}


def ability_table(str_base, str_adj, dex_base, dex_adj, con_base, con_adj, 
                  int_base, int_adj, wis_base, wis_adj, cha_base, cha_adj):
    ad = ability_detail
    return AttrDict({
        'Str': ad(str_base, str_adj),
        'Dex': ad(dex_base, dex_adj),
        'Con': ad(con_base, con_adj),
        'Int': ad(int_base, int_adj),
        'Wis': ad(wis_base, wis_adj),
        'Cha': ad(cha_base, cha_adj)
    })


def spells_per_day_bonus(mod, lvl):
    if mod <= 0: return 0
    elif mod == 1:
        if lvl == 1: return 1
    elif mod == 2:
        if lvl in (1, 2): return 1
    elif mod == 3:
        if lvl in (1, 2, 3): return 1
    elif mod == 4:
        if lvl in (1, 2, 3, 4): return 1 
    elif mod == 5:
        if lvl == 1: return 2
        elif lvl in (2, 3, 4, 5): return 1
    elif mod == 6:
        if lvl in (1, 2): return 2
        elif lvl in (3, 4, 5, 6): return 1
    elif mod == 7:
        if lvl in (1, 2, 3): return 2
        elif lvl in (4, 5, 6, 7): return 1
    elif mod == 8:
        if lvl in (1, 2, 3, 4): return 2
        elif lvl in (5, 6, 7, 8): return 1
    elif mod == 9:
        if level in (1,): return 3
        elif level in (2, 3, 4, 5): return 2
        else: return 1
    elif mod == 10:
        if level in (1, 2): return 3
        elif level in (3, 4, 5, 6): return 2
        else: return 1
    else:
        raise NotImplemented()