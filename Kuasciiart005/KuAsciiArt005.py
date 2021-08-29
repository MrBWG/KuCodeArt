from PIL import Image,ImageDraw,ImageFont,ImageTk
import random
import os
import sys
import tkinter
import tkinter.font as tkFont
import time
import imageio

CHAR_LIST = list("expectchaos")
scaled_img_width = 0
scaled_img_height = 0
output_str = ""
char_list_length = len(CHAR_LIST)
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

light_line = 0
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
    pic_hori_end = 0
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            if(ascii_img[i][j] != ' ' and pic_vect_begin == 0):
                pic_hori_begin = i
                break
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            if(ascii_img[scaled_img_height-1-i][j] != ' ' and pic_vect_end == 0):
                pic_hori_end = scaled_img_height-i
                break
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
    pic_vect_end = 0
    for j in range(scaled_img_height):
        for i in range(scaled_img_width):
            if(ascii_img[i][j] != ' ' and pic_vect_begin == 0):
                pic_vect_begin = j
                break
    for j in range(scaled_img_height):
        for i in range(scaled_img_width):
            if(ascii_img[i][scaled_img_width-1-j] != ' ' and pic_vect_end == 0):
                pic_vect_end = scaled_img_width-j
                break
    pic_width = pic_vect_end - pic_vect_begin
    return pic_width

def draw_mem_data(ascii_img, mem_image, mem_draw):
    global font_size
    global temp_save_count
    global line1_hori_char_index
    global light_line
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
                if(j == pic_vect_begin + light_line or j == pic_vect_begin + light_line +1):   #draw ve
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size-1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size+1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_light_r, font_light_g, font_light_b, font_bg_trans))
                elif(check_edge_char(ascii_img, i, j)):   #encounter edge char.
                    ###
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size-1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size+1,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size+1), ascii_img[i][j], font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
                else:
                    mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_color_r, font_color_g, font_color_b, font_color_trans))
            else:
                pixel_index = int(random.uniform(0,char_list_length))
                bg_chr = CHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                #mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), bg_chr, font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
    if(light_line > 0):
        light_line = light_line -  4
    else:
        light_line = pic_vect_end
    # PIL image can be saved as .png .jpg .gif or .bmp file
    if(temp_save_count <= 46):
        #save one frame.save to ps then conver to png.
        temp_psfile_name = "temp_" + str(temp_save_count) + ".png"
        #getter(tkcanvas, temp_psfile_name)
        mem_image.save(temp_psfile_name)
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
    global canvas
    global mem_image
    #mem_draw.rectangle((100, 100, 500, 500), fill='red', outline='blue', width=2)
    #mem_draw.line([20, 20, 80, 80], fill='red',width=3)     #画线
    #mem_draw.ellipse((100,100, 200, 200), fill ='red',outline='blue')#画圆
    print("drawingdrawing")
    tkimg = ImageTk.PhotoImage(image=mem_image)
    canvas.itemconfig(img_obj, image=tkimg)
    canvas.update()




root = tkinter.Tk()
root.title('KuCodeArt-ASCII')
print("why why why")
#tk.wm_attributes('-topmost', 1)
canvas = tkinter.Canvas(root, width=screen_width, height=screen_height, bd=0, highlightthickness=0, bg = 'black')
canvas.pack()
grey_img = read_image("ku100.png")
ascii_img = img2ascii(grey_img)
pic_width = get_pic_width(ascii_img)
light_line = pic_vect_end
print(pic_vect_end)
# PIL create an empty image and draw object to draw on
# memory only, not visible
mem_image = Image.new("RGB", (screen_width, screen_height), (0,0,0))
tkimg = ImageTk.PhotoImage(image=mem_image)

img_obj = canvas.create_image(500,500, image=tkimg)
mem_draw = ImageDraw.Draw(mem_image)
##draw_mem_data(ascii_img, mem_image, mem_draw)
#draw_rec()

#draw_ascii(ascii_img, canvas)
#mem_image.show()


loop_count = 0
#tk.mainloop()

while 1:
    time.sleep(0.1)
    loop_count = loop_count + 1
    update_ascii(canvas)
    draw_mem_data(ascii_img, mem_image, mem_draw)
    draw_rec()
    # PIL image can be saved as .png .jpg .gif or .bmp file
    ############
    #canvas.itemconfig(img_obj, image=tkimg)
    if(loop_count == 60):
        creat_gif(temp_img_list, "Kucodeart005.gif")
    root.update_idletasks()
    root.update()
   
