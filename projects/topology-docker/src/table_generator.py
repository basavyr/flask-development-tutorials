
def generate_header(headers):
    res_string = f'<tr>\n'
    id_string = f'<th>#id</th>\n'
    res_string += id_string
    for header in headers:
        res_string += f'<th>{header}</th>\n'

    # add the button with start and stop
    start_button = f'<th>Start Container</th>\n'
    stop_button = f'<th>Stop Container</th>\n'
    res_string += start_button
    res_string += stop_button
    res_string += f'</tr>\n'
    return res_string


def generate_rows(table_data, n_rows, n_cols):
    res_string = ''
    for row in range(n_rows):
        item = '<tr>\n'
        item += f'<td class="nr">{row+1}</td>'
        for col in range(n_cols):
            if(int(table_data[row][3]) == 1):
                item += f'<td style="color:green;">{table_data[row][col]}</td>\n'
            else:
                item += f'<td style="color:red;">{table_data[row][col]}</td>\n'
        item += f'<td><button type="button" class="btn btn-success action-start-container">START</button></td>'
        item += f'<td><button type="button" class="btn btn-danger action-stop-container" >STOP</button></td>'
        item += '</tr>\n'
        res_string += item

    return res_string


def table(headers, table_data, n_rows, n_cols):
    T = '<table class="docker-tabular">\n'
    H = generate_header(headers)
    R = generate_rows(table_data, n_rows, n_cols)
    T += H
    T += R
    T += '\n</table>\n'

    return T
