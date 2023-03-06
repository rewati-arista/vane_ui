import os

def test_assert():
    assert True

def test_cleaning_table(xc, table):

    correct_table = {'row1' : {'value1': 1, 'value2': 2, 'value3': 3},
                     'row2' : {'value1': None, 'value2': 2, 'value3': 3},
                     }
    new_table = xc._clean_table(table)

    assert new_table == correct_table

def test_column_return(xc, columns):

    table_dimensions = columns['table_dimensions']
    multi_cols = columns['multi_cols']
    correct_cols = [1, 2, 6, 7, 8]

    cols = xc._return_cols(table_dimensions, multi_cols)

    assert cols == correct_cols