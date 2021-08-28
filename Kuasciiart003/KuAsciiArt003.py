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
font_color_r = 5
font_color_g = 254
font_color_b = 5
font_color_trans = 255

font_bg_r = 204
font_bg_g = 0
font_bg_b = 204
font_bg_trans = 10

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

def print_ascii(ascii_img):
    output_str = ""
    for line in ascii_img:
        output_str += "".join(line) + "\n"
        sys.stdout.write(output_str)

def draw_ascii(ascii_img,tkcanvas):
    output_str = ""
    tfont = tkFont.Font(family='Times', size=font_size)
    #tfont.metrics(linespace=8,fixed=1)
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            #ascii_img[i][j]
            if(ascii_img[i][j] != ' '):
                tmp_obj = tkcanvas.create_text(font_size/2+j*font_size,font_size/2+i*font_size,text=ascii_img[i][j],font=tfont,fill=font_color)
            else:
                pixel_index = int(random.uniform(0,char_list_length))
                bg_chr = CHAR_LIST[pixel_index]
                tmp_obj = tkcanvas.create_text(font_size/2+j*font_size,font_size/2+i*font_size,text=bg_chr,font=tfont,fill=bg_color)
            text_objects.append(tmp_obj)

def update_ascii(tkcanvas):
    global temp_save_count
    for text in text_objects:
        pixel_index = int(random.uniform(0,char_list_length))
        tkcanvas.itemconfig(text, text=CHAR_LIST[pixel_index])


def draw_mem_data(ascii_img, mem_image, mem_draw):
    global font_size
    global temp_save_count
    # use a truetype font
    mfont = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 12)
    mem_draw.rectangle((0, 0, screen_width, screen_height), fill=(0,0,0), outline=(0,0,0), width=0)
    scaled_img_height = len(ascii_img)
    scaled_img_width = len(ascii_img[0])
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            #ascii_img[i][j]
            if(ascii_img[i][j] != ' '):
                pixel_index = int(random.uniform(0,char_list_length))
                ascii_img[i][j] = CHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), ascii_img[i][j], font=mfont, fill=(font_color_r, font_color_g, font_color_b, font_color_trans))
            else:
                pixel_index = int(random.uniform(0,char_list_length))
                bg_chr = CHAR_LIST[pixel_index]
                # do the PIL image/draw (in memory) drawings
                mem_draw.text((font_size/2+j*font_size,font_size/2+i*font_size), bg_chr, font=mfont, fill=(font_bg_r, font_bg_g, font_bg_b, font_bg_trans))
    # PIL image can be saved as .png .jpg .gif or .bmp file
    if(temp_save_count <= 30):
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
    imageio.mimsave(gif_name, frames, 'GIF', duration = 0.15)
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
    if(loop_count == 40):
        creat_gif(temp_img_list, "Kucodeart003.gif")
    root.update_idletasks()
    root.update()
   
