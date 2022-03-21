# import container_db as tools


def generate_header(headers):
    res_string = f'<tr>\n'
    for header in headers:
        res_string += f'<th>{header}</th>\n'
    res_string += f'</tr>\n'

    return res_string


def generate_rows(table_data, n_rows, n_cols):
    res_string = ''
    for row in range(n_rows):
        item = '<tr>\n'
        for col in range(n_cols):
            item += f'<td>{table_data[row][col]}</td>\n'
            # item += f'<td></td>\n'
        item += '</tr>\n'
        res_string += item

    return res_string


def table(headers, table_data, n_rows, n_cols):
    T = '<table class="docker-tabular" id ="">\n'
    H = generate_header(headers)
    R = generate_rows(table_data, n_rows, n_cols)
    T += H
    T += R
    T += '\n</table>\n'
    return T
