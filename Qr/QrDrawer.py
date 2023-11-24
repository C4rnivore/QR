from PIL import Image, ImageColor
from Tables import version_to_width, version_codes


def draw_qr(qr_version, data_flow):
#Data
    data = convert_bytes_flow_to_bits_str(data_flow)
#CanvasSettings
    padding = 4
    if qr_version == '1':
        qr_width = 21
    else:
        qr_width = version_to_width[int(qr_version)][len(version_to_width[int(qr_version)]) -1]
    total_width = qr_width + padding * 2
    width = total_width - 1
    sqare_inner_width = 9

#maskData
    mask_code = '111011111000100' # (M 0)

    qr = Image.new('P', (total_width,total_width), 'red')
    qr = qr.convert('RGB')


# Border
    for x in range(total_width):
        for y in range(total_width):
            if (y >= 0 and y < padding) or (y <= width and y > width-padding):
                 qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))
            if (x >= 0 and x < padding) or (x <= width and x > width-padding ):
                 qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))


#Search squares
    def draw_sqare(fromX, toX, fromY, toY):
        for x in range(fromX,toX):
            for y in range(fromY, toY):
                qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))

        for x in range(fromX+1,toX-1):
            for y in range(fromY+1, toY-1):
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))

        for x in range(fromX+2,toX-2):
            for y in range(fromY+2, toY-2):
                qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))

        for x in range(fromX+3,toX-3):
            for y in range(fromY+3, toY-3):
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))
        
#Leveling pattern
    def draw_leveling_pattern(X,Y):
        fromX, toX = X-5, X
        fromY, toY = Y-5, Y
        for x in range(fromX, toX ):
            for y in range(fromY, toY):
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))
        for x in range(fromX+1, toX-1 ):
            for y in range(fromY+1, toY-1):
                qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))
        qr.putpixel((X-3,Y-3), ImageColor.getcolor('black', 'P'))

#SyncLines
    def draw_sync_lines():
        white = True
        
        x = padding + sqare_inner_width-3
        y_from = padding + sqare_inner_width-1
        y_to = width - padding - sqare_inner_width+2

        for y in range(y_from,y_to):
            if white:
                qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))
                qr.putpixel((y,x), ImageColor.getcolor('white', 'P'))
    
                white = False
            else:
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))
                qr.putpixel((y,x), ImageColor.getcolor('black', 'P'))
                white = True

#VersionCodes
    def draw_version_code():
        version_code = version_codes[int(qr_version)]

        pass
    
    def draw_mask_and_level_code():
        start = mask_code[0:6]
        md = mask_code[6:9]
        end = mask_code[9:15]
        y = padding + sqare_inner_width - 1

        #TopLeftCode
        index = 0
        for x in range(padding, padding + 6):
            if(start[index] == '0'):
                qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))
            else:
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))

            if(end[::-1][index] == '0'):
                qr.putpixel((y,x), ImageColor.getcolor('white', 'P'))
            else:
                qr.putpixel((y,x), ImageColor.getcolor('black', 'P'))

            index += 1

        x_coords = [padding+sqare_inner_width-2, padding+sqare_inner_width-1, padding+sqare_inner_width-1]
        y_coords = [padding+sqare_inner_width-1, padding+sqare_inner_width-1, padding+sqare_inner_width-2]

        for i in range(0,3):
            if md[i] == '0':
                qr.putpixel((x_coords[i], y_coords[i]), ImageColor.getcolor('white', 'P'))
            else:
                qr.putpixel((x_coords[i], y_coords[i]), ImageColor.getcolor('black', 'P'))
    
    #BottomLeftCode
        first = True
        start = mask_code[0:7]
        end = mask_code[7:15]
        x = padding + sqare_inner_width - 1

        index = 0
        for y in range(width - padding - sqare_inner_width + 2, width - padding+1):
            if first:
                qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))
                first = False
                if end[index] == '0':
                    qr.putpixel((y,x), ImageColor.getcolor('white', 'P'))
                else:
                    qr.putpixel((y,x), ImageColor.getcolor('black', 'P'))
            else:
                if start[::-1][index] == '0':
                    qr.putpixel((x,y), ImageColor.getcolor('white', 'P'))
                else:
                    qr.putpixel((x,y), ImageColor.getcolor('black', 'P'))

                if end[index+1] == '0':
                    qr.putpixel((y,x), ImageColor.getcolor('white', 'P'))
                else:
                    qr.putpixel((y,x), ImageColor.getcolor('black', 'P'))
                index +=1




    def draw_data():
        next = True
        jump = False
        up = True

        min_value = padding
        max_value = width-padding
        x_start = max_value
        y_start = max_value
        bg_color = (255, 0, 0)
        index = 0
        vert_sync_line_x = 10

        has_space = True

        while has_space:
            if qr.getpixel((x_start,y_start)) == bg_color:
                col = (x_start) // 2
                row = (y_start) // 2
                mask = apply_mask(col,row)
                try:
                    el = data[index]
                    if el =='1':
                        if mask:
                            color = 'white'
                        else:
                            color = 'black'
                    else:
                        if mask:
                            color = 'black'
                        else:
                            color = 'white'
                    qr.putpixel((x_start, y_start), ImageColor.getcolor(color, 'P'))
                except:
                     qr.putpixel((x_start, y_start), ImageColor.getcolor('white', 'P'))
                index += 1

            if has_space:
                if up:
                    if next:
                        x_start -=1
                        next = False
                        jump = True
                    elif jump:
                        if y_start - 1 < min_value:
                            if x_start < min_value:
                                has_space = False

                            if x_start - 1 == vert_sync_line_x:
                                x_start -= 1

                            x_start -= 2
                            y_start -= 1
                            up=False
                        else:
                            x_start += 1
                            y_start -= 1
                            next = True
                            jump = False
                
                if not up:
                    if next:
                        x_start -=1
                        next = False
                        jump = True
                    elif jump:
                        if y_start + 1 > max_value:
                            if x_start -1 < min_value:
                                has_space = False

                            if x_start - 1 == vert_sync_line_x:
                                x_start -= 2

                            up = True
                            x_start -=1
                        else:
                            x_start += 1
                            y_start += 1

                        next = True
                        jump = False





    draw_sqare(padding-1, padding - 1 + sqare_inner_width, padding-1, padding-1 + sqare_inner_width) #Top Left
    draw_sqare(padding-1, padding  - 1 + sqare_inner_width, width - padding - sqare_inner_width + 2, width - padding+2) #Bottom Left
    draw_sqare(width - padding - sqare_inner_width + 2, width - padding + 2, padding - 1, padding - 1 + sqare_inner_width) #Top Right
    

   

    if int(qr_version) > 3:
        draw_leveling_pattern(qr_width,qr_width)
        if int(qr_version) > 6:
            draw_version_code()

    draw_mask_and_level_code()
    draw_sync_lines()
    draw_data()
    qr.save('simplePixel.png') # or any image format

    

def convert_bytes_flow_to_bits_str(dataflow):
    res=''
    for byte in dataflow:
        res+="{0:b}".format(byte)
    return res

def apply_mask(x,y):
    return (x + y) / 2 == 0

