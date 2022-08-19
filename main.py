from PIL import Image, ImageDraw, ImageFont
import os

COLOR_LIST = ['#e03131','#e8590c','#f08c00','#66a80f','#2f9e44','#099268','#0c8599','#1971c2','#3b5bdb','#6741d9','#9c36b5','#c2255c','#343a40']
X_LIMIT = 900
X_DISTANCE = 17
Y_DISTANCE = 17
fold_path = "./tag"

def input_data():
    final_data = []
    while True:
        a = input()
        if a == 's':
            break
        else:
            final_data.append(a)
    return final_data

def get_size(text: str):
    canvas = Image.new('RGB', (2048, 2048))
    draw = ImageDraw.Draw(canvas)
    monospace = ImageFont.truetype("msyh.ttc", 30)
    draw.text((0, 0), text, font=monospace)
    bbox = canvas.getbbox()
    size = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    return size

def draw_tag(text, color: str, file_name = "no name"):
    if file_name == "no name":
        file_name = text
    size = get_size(text)
    canvas = Image.new('RGBA', (size[0]+34, 57))
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("msyh.ttc", 30, encoding="utf-8")
    draw.rounded_rectangle((0, 0, size[0]+33, 57), 14, fill=color)
    draw.text((15, 9), text, "grey", font)
    draw.text((16, 8), text, 'white', font)
    # canvas.show()
    canvas.save("%s/%s.png" % (fold_path, file_name))

def group_draw_tag(data_list: list):
    for i in range(len(data_list)):
        draw_tag(data_list[i], COLOR_LIST[i%len(COLOR_LIST)], str(i).rjust(2,'0'))

def read_picture():
    directory_name = fold_path
    tag_pic_list = []
    for picture_name in os.listdir(directory_name):
        file_name = directory_name + "/" + picture_name  # 读取文件夹地址+图片名称类型
        Temp = Image.open(file_name)
        tag_pic_list.append((Temp,Temp.size))
    return tag_pic_list

def cal_canvas_size(tag_list):
    X = X_LIMIT
    TEMP = 0
    count = 1
    Pic_X = []
    for i in tag_list:
        Pic_X.append(i[1][0])
    for i in Pic_X:
        TEMP += i
        if TEMP > X:
            count += 1
            TEMP = 0
        TEMP += X_DISTANCE
    Y = 57 * count + Y_DISTANCE * (count - 1)
    return Y

def clear_fold(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clear_fold(c_path)
        else:
            os.remove(c_path)

def draw_final_pic(tag_list):
    Y = cal_canvas_size(tag_list)
    canvas = Image.new("RGBA", (X_LIMIT, Y))
    x = 0
    y = 0
    for i in range(len(tag_list)):
        if x + tag_list[i][1][0] > X_LIMIT:
            x = 0
            y += 57 + Y_DISTANCE
        canvas.paste(tag_list[i][0], (x,y))
        x += tag_list[i][1][0] + X_DISTANCE
    canvas.save("now.png")

if __name__=='__main__':
    clear_fold(fold_path)
    data = input_data()
    group_draw_tag(data)
    tag_list = read_picture()
    draw_final_pic(tag_list)
