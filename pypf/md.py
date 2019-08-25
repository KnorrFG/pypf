from yattag import Doc
from .utils import first, keymap, valmap, line

def _html_table(header, rows, caption=None, col_align=None):
    col_align = col_align or 'center'
    doc, tag, text = Doc().tagtext()
    if type(col_align) == str:
        col_align = [col_align] * len(header)
    with tag('table'):
        if caption:
            with tag('caption'):
                with tag('b'):
                    doc.asis(str(caption))
        with tag('tr'):
            for ind in header:
                with tag('th'):
                    doc.asis(str(ind))
        for row in rows:
            with tag('tr'):
                for val, al in zip(row, col_align):
                    with tag('td', align=al):
                        doc.asis(str(val))
    return doc.getvalue()


def flat_table(index_or_dict, *vals, caption=None, col_aligns=None):
    """Returns a string that represents a flat  table.
    The table will have only one single row. The first argument is expected to
    be a string, which contains the index, where the fields are seperated by a
    comma. After that the values are provided one by one"""
    if isinstance(index_or_dict, dict):
        assert len(vals) == 0
        indices = index_or_dict.keys()
        vals = index_or_dict.values()
    else:
        indices = index_or_dict.split(',')
        assert len(vals) == len(indices)
    return _html_table(indices, [vals], caption, col_aligns)
        

def table(d: dict, index_column_name, caption=None, col_align=None):
    indices = [index_column_name, *first(d.values()).keys()]
    rows = [(key, *row.values()) for key, row in d.items()]
    return _html_table(indices, rows, caption, col_align)


def long_table(index_or_dict, *vals, l_col_name='Name', r_col_name='Bonus', 
               bold_index=True, caption=None, col_align=None):
    '''Makes a table with 2 columns, and as many rows as the input provides.
    If the first argument is a dict the keys are taken as the left column, and
    the values as the right column, otherwise the first argument should be a
    string containing the left column separated by commas and then the values
    one by one.'''
    col_align = col_align or ['right', 'left']
    d = dict(zip(index_or_dict.split(','), vals)) \
        if isinstance(index_or_dict, str) else index_or_dict
    if bold_index:
        d = keymap('<b>{}</b>'.format, d)
    d = valmap(lambda x: line(str(x)), d)
    return _html_table([l_col_name, r_col_name], d.items(), caption, 
                       col_align)
