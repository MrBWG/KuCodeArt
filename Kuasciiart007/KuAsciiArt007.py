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
KUCHAR_LIST = list("moonriver")
kuchar_list_length = len(KUCHAR_LIST)
scaled_img_width = 0
scaled_img_height = 0
output_str = ""

font_size = 10
screen_width = 1000
screen_height = 1000
text_objects = list()

font_bg_r = 255
font_bg_g = 51
font_bg_b = 204
font_bg_trans = 255


rotate_angle = 360

temp_img_dir = "tmpdir"
temp_save_count = 1
temp_img_list = list()

#moonriver color layer: 0, 13, 51, 255

def read_image(image_path):
    img = Image.open(image_path)
    grey_image = img.convert("RGB")
    return grey_image
 
def img2ascii(grey_image, char_list=CHAR_LIST, scale=1.0, layer=1):
    scaled_img_width = int(grey_image.size[0] * scale) # scale
    scaled_img_height = int(grey_image.size[1] * scale)
    scaled_grey_img = grey_image.resize((scaled_img_width, scaled_img_height))
    char_list_length = len(char_list)
    ascii_data = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]   #pixel data
    color_data = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]   #color data
    img_data = list()

    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            # brightness: the larger, the brighter, and later position in given char list
            brightness = scaled_grey_img.getpixel((j, i))
            brightnessL = brightness[0] * 299/1000 + brightness[1] * 587/1000 + brightness[2] * 114/1000
            color_data[i][j] = brightness
            #print(brightnessL)
            if(layer ==1  and brightnessL > 10 and brightnessL <= 128):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_data[i][j] = char_list[pixel_index]
                #color_data[i][j] = (brightness[0]+70, brightness[1]+10, brightness[2]+50)
                #print(color_data[i][j])
            elif(layer == 2 and brightnessL > 128):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_data[i][j] = char_list[pixel_index]
                color_data[i][j] = (255, 255, 255)
            else:
                ascii_data[i][j] = ' '
    img_data.append(ascii_data)
    img_data.append(color_data)
    return img_data

def check_edge_char(ascii_img, i, j):
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    if((j-1 > 0 and ascii_img[i][j-1] == ' ' ) or (j+1 < scaled_img_width and ascii_img[i][j+1] == ' ' )
            or (i-1 > 0 and ascii_img[i-1][j] == ' ' ) or (i+1 < scaled_img_height and ascii_img[i+1][j] == ' ' )):
        #is edge char
        return True
    else:
        return False

def draw_mem_data(start_x, start_y, ascii_data, color_data, mem_image, mem_draw, clear=True):
    global font_size
    # use a truetype font
    mfont = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 12)
    #mem_draw.rectangle((0, 0, screen_width, screen_height), fill=(0,0,0), outline=(0,0,0), width=0)
    #mem_draw.rectangle((0, 0, screen_width, screen_height), fill=(0,0,0,0), outline=(0,0,0), width=0)
    scaled_img_height = len(ascii_data)
    scaled_img_width = len(ascii_data[0])
    for i in range(scaled_img_height):    #j:x   i:y
        for j in range(scaled_img_width):
            #ascii_img[i][j]
            if(ascii_data[i][j] != ' '):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_data[i][j] = CHAR_LIST[pixel_index]
                if(clear):
                    mem_draw.rectangle((start_x + j*font_size+5, start_y + i*font_size+5, start_x + j*font_size+font_size+6, start_y + i*font_size+font_size+6), fill=(0,0,0,255), outline=(0,0,0), width=0)
                mem_draw.text((start_x + font_size/2+j*font_size,start_y + font_size/2+i*font_size), ascii_data[i][j], font=mfont, fill=color_data[i][j])



def draw_merge_mem_data(merge_mem_image, mem_image, kusama_mem_image):
    global temp_save_count
    global rotate_angle
    #rotate bg image.
    rotate_image = mem_image.rotate(rotate_angle)
    r1_image = rotate_image.resize((screen_width,screen_height))
    r2_image = kusama_mem_image.resize((screen_width,screen_height))
    merge_mem_image.alpha_composite(r1_image, (0, 0), (0, 0))
    merge_mem_image.alpha_composite(r2_image, (0, 0), (0, 0))
    if(rotate_angle > 0):
        rotate_angle = rotate_angle - 6
    else:
        rotate_angle = 360
    if(temp_save_count <= 120):
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
    merge_tkimg = ImageTk.PhotoImage(image=merge_mem_image)
    canvas.itemconfig(merge_img_obj, image=merge_tkimg)




root = tkinter.Tk()
root.title('KuCodeArt-ASCII')
canvas = tkinter.Canvas(root, width=screen_width, height=screen_height, bd=0, highlightthickness=0, bg = 'black')
canvas.pack()

#bg image
grey_img = read_image("bifrost100s.png")
ascii_img = img2ascii(grey_img, CHAR_LIST, 1.0, 1)

# PIL create an empty image and draw object to draw on
# memory only, not visible
mem_image = Image.new("RGBA", (grey_img.width*font_size, grey_img.height*font_size), (0,0,0,0))
#kimg = ImageTk.PhotoImage(image=mem_image)
#img_obj = canvas.create_image(500,400, image=tkimg)
mem_draw = ImageDraw.Draw(mem_image)

#front image
kusama_img = read_image("bifrost300s.png")
kusama_ascii_img = img2ascii(kusama_img, KUCHAR_LIST, 1.0, 2)
# kusama image data
kusama_mem_image = Image.new("RGBA", (kusama_img.width*font_size, kusama_img.height*font_size), (0,0,0,0))
#kusama_tkimg = ImageTk.PhotoImage(image=kusama_mem_image)
#kusama_img_obj = canvas.create_image(500,750, image=kusama_tkimg)
kusama_mem_draw = ImageDraw.Draw(kusama_mem_image)

merge_mem_image = Image.new("RGBA", (screen_width, screen_height), (0,0,0))
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
    draw_mem_data(0,0, ascii_img[0], ascii_img[1], mem_image, mem_draw, True)
    draw_mem_data(0,0,kusama_ascii_img[0], kusama_ascii_img[1], kusama_mem_image, kusama_mem_draw, False)
    draw_merge_mem_data(merge_mem_image, mem_image, kusama_mem_image)
    draw_rec()
    # PIL image can be saved as .png .jpg .gif or .bmp file
    ############
    #canvas.itemconfig(img_obj, image=tkimg)

    if(loop_count == 150):
        creat_gif(temp_img_list, "Kucodeart007_5.gif")
    root.update_idletasks()
    root.update()
   
