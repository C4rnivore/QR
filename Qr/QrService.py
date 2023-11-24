from Tables import versions_table, blocks_amount_table, data_count, correction_bytes_amount_table, generating_polynomials_table, galua_field, reversed_galua_field

QR_VERSION = '-1'

#Способ кодирования 
code_type = '0010'
#Количество кодируемых символов
code_symbols_count = 45

def get_qr_version():
    return QR_VERSION

#--------------------- Service Info --------------------------# +
def add_service(encoded_data):
    result = code_type
    global QR_VERSION 

    data_bytes_count = len(encoded_data)
    qr_version = get_version(data_bytes_count)
    print(data_bytes_count, qr_version)
    
    QR_VERSION = qr_version

    data_count_field_len = get_field_len(qr_version)
    
    if data_count_field_len == 9:
        service_data_count = '{0:09b}'.format(code_symbols_count)
    elif data_count_field_len == 11:
        service_data_count = '{0:011b}'.format(code_symbols_count)
    elif data_count_field_len == 13:
        service_data_count = '{0:013b}'.format(code_symbols_count)
    else:
        raise Exception('Something went wrong during service infotrmation!')
    
    result += service_data_count
    result += encoded_data
    return result

def get_version(amount):
    for k, v in versions_table.items():
        if amount <= k:
            return v


def get_field_len(qr_version):
    for k, v in data_count.items():
        if int(qr_version) <= int(k):
            return v
        



#--------------------- Filling Qr --------------------------# +

def fill_qr(encoded_data_with_service):
    zero_amount = get_zeros_amount(encoded_data_with_service)
    encoded_data_with_service += '0' * zero_amount
    
    filling_distance = get_len_for_qr_version() - len(encoded_data_with_service)

    encoded_data_with_service = fill_data_to_fit_version_size(encoded_data_with_service, filling_distance // 8 )

    return encoded_data_with_service

def get_zeros_amount(encoded_data_with_service):
    return ((len(encoded_data_with_service) // 8 + 1) * 8 ) - len(encoded_data_with_service)

def get_len_for_qr_version():
    global QR_VERSION 
    for k, v in versions_table.items():
        if v == QR_VERSION:
            return k
        
def fill_data_to_fit_version_size(data, steps):
    fillers = ['11101100', '00010001']
    temp = data
    for i in range(0,steps):
        if i == 0:
            temp+=fillers[0]
        else:
            temp+=fillers[i % 2]
    return temp

#--------------------- Splitting by blocks --------------------------# +

def split_by_blocks(filled_encoded_data_with_service):
    if(QR_VERSION == '1'):
        return [filled_encoded_data_with_service]
    
    blocks_amount = blocks_amount_table[QR_VERSION]
    result_blocks =  [None]*blocks_amount

    bytes_amount = len(filled_encoded_data_with_service) / 8
    bytes_per_block = bytes_amount // blocks_amount
    extra_bytes = bytes_amount % blocks_amount

    default_blocks_count = blocks_amount - extra_bytes

    for i in range(blocks_amount):
        if i <= default_blocks_count - 1:
            block_content = filled_encoded_data_with_service[:int(bytes_per_block)*8]
            filled_encoded_data_with_service = filled_encoded_data_with_service[int(bytes_per_block)*8+8:]
        else:
            block_content = filled_encoded_data_with_service[:(int(bytes_per_block) * 8) + 8]
            filled_encoded_data_with_service = filled_encoded_data_with_service[(int(bytes_per_block) * 8) + 16:]

        result_blocks[i] = block_content

    return(result_blocks)


# --------------------- Qr Correction --------------------------# ?
def create_correction(data_blocks):
    global QR_VERSION

    blocks_with_corr = []

    cor_bytes_count = correction_bytes_amount_table[QR_VERSION]
    cor_bytes = generating_polynomials_table[cor_bytes_count]
    byte_blocks = convert_bites_to_bytes_block(data_blocks)
    
    for block in byte_blocks:
        length = max(cor_bytes_count, len(block))
        temp = [0] *  length
        i=0

        for byte_num in block:
            temp[i] = byte_num
            i+=1

        #Расчет байтов коррекции для данного блока данных
        for i in block:
            a = temp.pop(0)
            temp.append(0)

            if(a == 0):
                continue
            else:
                b = reversed_galua_field[a]
                for j in range(cor_bytes_count):
                    v = cor_bytes[j] + b  
                    if(v > 254):
                        v = v % 255

                    temp[j] = galua_field[v] ^ temp[j]
        
        blocks_with_corr.append(block)
        blocks_with_corr.append(temp)
    return blocks_with_corr
    


def convert_bites_to_bytes_block(data_blocks):
    temp = [None]*len(data_blocks)
    i = 0

    for block in data_blocks:
        sub_array =[]
        l = [''.join(i) for i in grouper(block, 8)]

        for el in l:
            sub_array.append(int(el,2))
        temp[i] = sub_array
        i += 1
    
    return temp

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)

# --------------------- Qr Combining --------------------------# ?

def combine_blocks_with_correction(correction_list):
    bytes_flow = []
    blocks, corrections = extract_values(correction_list)
    range_block = 0
    range_corr = 0 

    for block in blocks:
        if len(block) > range_block:
            range_block = len(block)

    for corr in corrections:
        if len(corr) > range_corr:
            range_corr = len(corr)
    
    for i in range(range_block):
        for block in blocks:
            if i < len(block):
                bytes_flow.append(block[i])
            else:
                continue

    for i in range(range_corr):
        for corr in corrections:
            if i < len(corr):
                bytes_flow.append(corr[i])
            else:
                continue
    return bytes_flow
    
    
def extract_values(correction_list):
    blocks = []
    corrections = []
    prev_was_block = False

    for el in correction_list:
        if not prev_was_block:
            blocks.append(el)
            prev_was_block = True
        else:
            corrections.append(el)
            prev_was_block = False

    return blocks, corrections

