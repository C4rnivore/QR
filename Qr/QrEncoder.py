import re
from Tables import encode_table

#буквенно цифоровое кодирование
def encode(input):
    output = ''
    for pair in split_input(input):
        if len(pair) == 2:
            output += calc_bin_for_pair(pair[0], pair[1])
        else:
            output += calc_bin_for_pair(pair[0])

    return output
        

def calc_bin_for_pair(first_symbol, second_symbol = None):
    if second_symbol != None:
        value = encode_table[first_symbol] * 45 + encode_table[second_symbol]
        value = '{0:011b}'.format(value)
    else:
        value = encode_table[first_symbol]
        value = '{0:06b}'.format(value)
    
    return value

def split_input(input):
    splitted = []

    if len(input) % 2 == 0:
        splitted = re.findall('..',input)
    else:
        splitted = re.findall('..',input)
        splitted.append(input[len(input) - 1])

    return splitted