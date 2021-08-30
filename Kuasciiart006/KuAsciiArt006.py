from PIL import Image,ImageDraw,ImageFont,ImageTk
import random
import os
import sys
import tkinter
import tkinter.font as tkFont
import time
import imageio

CHAR_LIST = list("expectchaos")
char_list_length = len(CHAR_LIST)
KUCHAR_LIST = list("expectchaos")
kuchar_list_length = len(KUCHAR_LIST)
scaled_img_width = 0
scaled_img_height = 0
output_str = ""

font_size = 10
screen_width = 1000
screen_height = 1000
text_objects = list()
font_color = "#33cc66"
bg_color = "#ccffcc"
font_color_r = 204
font_color_g = 0
font_color_b = 153
font_color_trans = 255

font_bg_r = 255
font_bg_g = 51
font_bg_b = 204
font_bg_trans = 10

font_light_r = 255
font_light_g = 102
font_light_b = 204
font_light_trans = 255

canary_light_line = 0
kusama_light_line = 0
pic_height = 0
pic_vect_begin = 0
pic_vect_end = 0
pic_width = 0
pic_hori_begin = 0
pic_hori_end = 0

temp_img_dir = "tmpdir"
temp_save_count = 1
temp_img_list = list()


def read_image(image_path):
    img = Image.open(image_path)
    grey_image = img.convert("L")
    return grey_image
 
def img2ascii(grey_image, char_list=CHAR_LIST, scale=1.0):
    scaled_img_width = int(grey_image.size[0] * scale) # scale
    scaled_img_height = int(grey_image.size[1] * scale)
    scaled_grey_img = grey_image.resize((scaled_img_width, scaled_img_height))
    char_list_length = len(char_list)
    ascii_img = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            # brightness: the larger, the brighter, and later position in given char list
            brightness = scaled_grey_img.getpixel((j, i))
            if(brightness > 5):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_img[i][j] = char_list[pixel_index]
            else:
                ascii_img[i][j] = ' '
    return ascii_img


def update_ascii(tkcanvas):
    global temp_save_count
    for text in text_objects:
        pixel_index = int(random.uniform(0,char_list_length))
        tkcanvas.itemconfig(text, text=CHAR_LIST[pixel_index])

def check_edge_char(ascii_img, i, j):
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    if((j-1 > 0 and ascii_img[i][j-1] == ' ' ) or (j+1 < scaled_img_width and ascii_img[i][j+1] == ' ' )
            or (i-1 > 0 and ascii_img[i-1][j] == ' ' ) or (i+1 < scaled_img_height and ascii_img[i+1][j] == ' ' )):
        #is edge char
        return True
    else:
        return False

def get_pic_height(ascii_img):
    global pic_hori_end
    global pic_hori_begin
    global pic_height
    pic_height = 0
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    pic_hori_begin = 0
    pic_hori_end = scaled_img_height
    pic_height = pic_hori_end - pic_hori_begin
    return pic_height

def get_pic_width(ascii_img):
    global pic_vect_end
    global pic_vect_begin
    global pic_width
    pic_width = 0
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    pic_vect_begin = 0
    pic_vect_end = scaled_img_width
    pic_width = pic_vect_end - pic_vect_begin
    return pic_width

def draw_canary_mem_data(start_x, start_y, ascii_img, mem_image, mem_draw):
    global font_size
    global canary_light_line
    # use a truetype font
    mfont = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 12)
    mfont_edge = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 14, index=1)
    mfont_light = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 14, index=1)
    mem_draw.rectangle((0, 0, screen_width, screen_height), fill=(0,0,0), outline=(0,0,0), width=0)
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    for i in range(scaled_img_height):    #j:x   i:y
        for j in range(scaled_img_width):
            #ascii_img[i][j]
            if(ascii_img[i][j] != ' '):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_img[i][j] = CHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                if(j == canary_light_line or j == canary_light_line +1):   #draw ve
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size-1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size+1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                elif(check_edge_char(ascii_img, i, j)):   #encounter edge char.
                    ###
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size-1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size+1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                else:
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_color_r, font_color_g, font_color_b, font_color_trans))
            else:
                pixel_index = int(random.uniform(0,char_list_length))
                bg_chr = CHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                #mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), bg_chr, font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
    if(canary_light_line > 4):
        canary_light_line = canary_light_line -  4
    else:
        canary_light_line = scaled_img_width-4

def draw_kusama_mem_data(start_x, start_y, ascii_img, mem_image, mem_draw):
    global font_size
    global kusama_light_line
    # use a truetype font
    mfont = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 12)
    mfont_edge = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 14, index=1)
    mfont_light = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 14, index=1)
    mem_draw.rectangle((0, 0, screen_width, screen_height), fill=(0,0,0), outline=(0,0,0), width=0)
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    for i in range(scaled_img_height):    #j:x   i:y
        for j in range(scaled_img_width):
            #ascii_img[i][j]
            if(ascii_img[i][j] != ' '):
                pixel_index = int(random.uniform(0,kuchar_list_length))
                ascii_img[i][j] = KUCHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                if(i == kusama_light_line or i == kusama_light_line -1):
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size-1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size+1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                elif(check_edge_char(ascii_img, i, j)):   #encounter edge char.
                    ###
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size-1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size+1,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                else:
                    mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_color_r, font_color_g, font_color_b, font_color_trans))
            else:
                pixel_index = int(random.uniform(0,kuchar_list_length))
                bg_chr = KUCHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                #mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), bg_chr, font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
    if(kusama_light_line < scaled_img_height-1):
        kusama_light_line = kusama_light_line +  2
    else:
        kusama_light_line = 1



def draw_merge_mem_data(merge_mem_image, mem_image, kusama_mem_image):
    global temp_save_count
    merge_mem_image.paste(mem_image, (80, 100))
    merge_mem_image.paste(kusama_mem_image, (0, 650))
    if(temp_save_count <= 51):
        #save one frame.save to ps then conver to png.
        temp_psfile_name = "temp_" + str(temp_save_count) + ".png"
        #getter(tkcanvas, temp_psfile_name)
        merge_mem_image.save(temp_psfile_name)
        temp_img_list.append(temp_psfile_name)
        temp_save_count = temp_save_count + 1


def creat_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.12)
    return


def draw_rec():
    global tkimg
    global mem_draw
    global mem_image
    global merge_tkimg
    global merge_mem_draw
    global merge_mem_image
    global canvas
    #mem_draw.rectangle((100, 100, 500, 500), fill='red', outline='blue', width=2)
    #mem_draw.line([20, 20, 80, 80], fill='red',width=3)     #画线
    #mem_draw.ellipse((100,100, 200, 200), fill ='red',outline='blue')#画圆
    print("drawingdrawing")
    #tkimg = ImageTk.PhotoImage(image=mem_image)
    #canvas.itemconfig(img_obj, image=tkimg)
    merge_tkimg = ImageTk.PhotoImage(image=merge_mem_image)
    canvas.itemconfig(merge_img_obj, image=merge_tkimg)
    #canvas.update()




root = tkinter.Tk()
root.title('KuCodeArt-ASCII')
print("why why why")
#tk.wm_attributes('-topmost', 1)
canvas = tkinter.Canvas(root, width=screen_width, height=screen_height, bd=0, highlightthickness=0, bg = 'black')
canvas.pack()

#canary image
grey_img = read_image("canary.png")
ascii_img = img2ascii(grey_img)
#pic_width = get_pic_width(ascii_img)
#light_line = pic_vect_end

# PIL create an empty image and draw object to draw on
# memory only, not visible
mem_image = Image.new("RGB", (grey_img.width*font_size, grey_img.height*font_size), (0,0,0))
#kimg = ImageTk.PhotoImage(image=mem_image)
#img_obj = canvas.create_image(500,400, image=tkimg)
mem_draw = ImageDraw.Draw(mem_image)

#kusama character image
kusama_img = read_image("kusama100.png")
kusama_ascii_img = img2ascii(kusama_img, KUCHAR_LIST)
# kusama image data
kusama_mem_image = Image.new("RGB", (kusama_img.width*font_size, kusama_img.height*font_size), (0,0,0))
#kusama_tkimg = ImageTk.PhotoImage(image=kusama_mem_image)
#kusama_img_obj = canvas.create_image(500,750, image=kusama_tkimg)
kusama_mem_draw = ImageDraw.Draw(kusama_mem_image)

merge_mem_image = Image.new("RGB", (screen_width, screen_height), (0,0,0))
merge_tkimg = ImageTk.PhotoImage(image=merge_mem_image)
merge_img_obj = canvas.create_image(500,500, image=merge_tkimg)
merge_mem_draw = ImageDraw.Draw(merge_mem_image)
#merge_image = Image.alpha_composite(mem_image, dest=(0, 0), source=(0, 0))
#merge_image = Image.alpha_composite(kusama_img, dest=(0, 0), source=(0, 0))
#draw_ascii(ascii_img, canvas)
#mem_image.show()


loop_count = 0
#tk.mainloop()

while 1:
    time.sleep(0.05)
    loop_count = loop_count + 1
    update_ascii(canvas)
    draw_canary_mem_data(0,0, ascii_img, mem_image, mem_draw)
    draw_kusama_mem_data(0,0,kusama_ascii_img, kusama_mem_image, kusama_mem_draw)
    #merge_mem_image.paste(mem_image, (100, 100))
    #merge_mem_image.paste(kusama_mem_image, (50, 700))
    draw_merge_mem_data(merge_mem_image, mem_image, kusama_mem_image)
    draw_rec()
    # PIL image can be saved as .png .jpg .gif or .bmp file
    ############
    #canvas.itemconfig(img_obj, image=tkimg)

    if(loop_count == 60):
        creat_gif(temp_img_list, "Kucodeart006.gif")
    root.update_idletasks()
    root.update()
   
