#Libraries here
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
#Might need to include PIL as well just to display the image too
from PIL import Image, ImageTk, ExifTags
from PIL.ExifTags import TAGS
import os

#Globals/Constants here
DEFAULT_BG_0 = "#FFFFFF"  # White mode
DEFAULT_BG_1 = "#2C3738"  # Dark mode

THUMBNAIL_SIZE = (100,100) #sample size, can experiment
DISPLAY_LIMIT = 20 #display up to this many images per page

remove_list = None

database = open("database.txt", 'r+') #unsure if needed

all_folders = []
all_photos = []

settings_file_path = "settings.txt"
settings = open(settings_file_path, "r+")
settings_data = settings.readlines() #unsure if needed HERE.

#Setting Background according to settings text file
bg_file = settings_data[1]
bg_file = bg_file.split("=")
bg_file[1] = bg_file[1][:7]

set_bg = "" 


#Truncating and lines then casting into ints
resolution = settings_data[0]
resolution = resolution.split("x")
resolution[0] = resolution[0][11:]
resolution[1] = resolution[1][:-1]

resolution[0] = int(resolution[0])
resolution[1] = int(resolution[1])

set_res_x = resolution[0]
set_res_y = resolution[1]

#Methods here

def replace_line(file_path, line_number, text):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines[line_number] = text

    with open(file_path, 'w') as file:
        file.writelines(lines)

def set_dark():
    front.config(background=DEFAULT_BG_1)
    replace_line(settings_file_path, 1, "bgcolor=" + DEFAULT_BG_1 + "\n")

def set_light():
    front.config(background=DEFAULT_BG_0)
    replace_line(settings_file_path, 1, "bgcolor=" + DEFAULT_BG_0 + "\n")

def set_custom():
    color = colorchooser.askcolor()
    if color[1]:
        front.config(background=color[1])
        replace_line(settings_file_path, 1, "bgcolor=" + color[1] + "\n")

def add_direc():
    folderpath = filedialog.askdirectory()
    # settings.seek(0,2)
    settings.write(folderpath + '\n')

def remove_direc():
    def remove():
        #global remove_list
        ind = int(remove_list.curselection()[0])
        ind += 7   
        replace_line('settings.txt', ind, "")
        remove_list.delete(remove_list.curselection())

    remove_window = Toplevel()
    remove_window.geometry("600x700+600+0")
    remove_window.minsize(600,700)

    global remove_list
    if remove_list is None:
        remove_list = Listbox(remove_window, width=75)

    list = []
    settings.seek(0,0)
    lines = settings.readlines()
    print(len(lines))
    for i in range(7, len(lines)): 
        list.append(lines[i])

    for x,item in enumerate(list):
        remove_list.insert(x,item)

    remove_list.pack()

    button_frame = Frame(remove_window)
    button_frame.pack(anchor="n")
    remove_button = Button(button_frame, text="Remove Directory", command=remove)
    remove_button.pack()

def search_focus(event):
    search_tags.focus_set()

def append_folders(folder):

    dir_list = os.listdir(folder)
    if len(dir_list) > 0:
        for dir_name in dir_list:
            full_path = os.path.join(folder, dir_name)
            if os.path.isdir(full_path):
                append_folders(full_path)

    if folder not in all_folders and os.path.isdir(folder):
        all_folders.append(folder)

def append_photos():
    # This adds all photos' paths from all specified folders and subfolders to app's memory
    settings.seek(0, 0)
    lines = settings.readlines()
    folders = []

    # Get the current script's directory
    script_directory = os.path.dirname(__file__)

    # Read from file at a certain point
    for i in range(7, len(lines)):
        folder_path = os.path.join(script_directory, lines[i].strip())
        folders.append(folder_path)

    # Let's go depth first: dig through all folders and open subsequent folders.
    for folder in folders:
        if not os.path.exists(folder):  # if the path doesn't exist. Unsure if this works
            continue
        append_folders(folder)

    for folder in all_folders:
        # I think you have to change to that directory first before getting photos? Could be very wrong
        os.chdir(folder)
        files = os.listdir(folder)
        # open all files in the folder
        for file in files:
            if os.path.isfile(file):
                full_path = os.path.join(folder, file).replace("\\", "/")
                if full_path not in all_photos:
                    all_photos.append(full_path)

def filter(photo: str, search_tags: str) -> bool:
        # if search_tags == None:
        if search_tags == "":
            return True
        # if not search_tags: return True 
        search_tags = search_tags.split(",")
        
        #open image, get existing EXIF data
        img = Image.open(photo)
        exif = img.getexif()
        
        #Search UserComment, split, and search.
        if exif is not None:
            if 37510 in exif:
                user_comment = exif[37510].split(',') if exif[37510] else []
                x = 0
                for stag in search_tags:
                    if stag in user_comment:
                        x += 1
                if x == len(search_tags):
                    return True
                return False

    
def display_page(page_number):
    if len(results) == 0:
        print("No matches found")
    else:
        for i in range(DISPLAY_LIMIT * page_number, min(DISPLAY_LIMIT * (page_number + 1), len(all_photos))):
            if i < len(results):
                show_image(i, results[i]) #will need to change this logic later

def search_results():
    global grid_labels  # Add this line to indicate that you're using the global variable

    append_photos()
    print(search_tags)

    if grid_labels is not None:
        for label in grid_labels:
            label.destroy()
        grid_labels = []  # Reset the global variable

    global results #forgot if need to be global.
    results = [] #this gets filled in by photos with correct tags
    if all_photos: 
        for photo in all_photos:
            if filter(photo, search_tags.get()) == True: #Need to get search tags first. won't work atm
                results.append(photo)

    page_count = int((len(results) / DISPLAY_LIMIT)) #How many pages of results exist.
    if (len(results) % DISPLAY_LIMIT) > 0:
        page_count += 1
    page_number = 0 #current page
    
    display_page(page_number)
    update_page_labels(page_number, page_count) #Maybe use this function within the function itself too?
 

#TODO: do not display buttons for pages beyond max, definitely happens when difference between current and max page is small enough
#TODO: add a focus event to the entry
def update_page_labels(page_number, page_count): 
    for widget in page_grid.winfo_children():
        widget.destroy()

    # Determine the range of pages to display labels for
    start_page = page_number #current page
    end_page = min(page_count, 5) #max # of pages
    
    def jump(i):
        for photo in gallery_grid.winfo_children():
            photo.destroy()
        display_page(i)
        update_page_labels(i,page_count)
        

    # def disable_page(button):
    #     if int(button.cget("text")) > page_count:
    #         button.config(state="disabled")

    def direct_jump(event):
        target_page = jump_entry.get()
        if target_page.isdigit():
            target_page = int(target_page) - 1
            if 0 <= target_page <= page_count - 1:
                jump(target_page)
            if target_page >= page_count:
                jump(page_count - 1)

    
#OG VERSION
#TODO: Make bindng work.
    if end_page <= 4: #If 5 or less pages
        for i in range(start_page,end_page):
            page = Button(page_grid,text=str(i+1), command=lambda i=i:jump(i))
            if i == start_page:
                page.config(state="disabled")
            page.grid(row=0,column=i)
            
    #Need to account for scrolling up pages due to not seeing the prev buttons later on.
    else: 
        p1 = Button(page_grid, text = "1",command=lambda i=0:jump(i))
        if start_page == 0:
            p1.config(state="disabled")
        p1.grid(row=0,column=0)

        #Button 2. Should take you 1 page back.
        #Always display 2 if at page 3 or below
        if start_page <= 2: #if at page 
            p2 = Button(page_grid, text = "2", command=lambda i=1:jump(i))
        else:    
            p2 = Button(page_grid, text = (start_page), command=lambda i=(start_page-1):jump(i))
        if start_page == 1:
            p2.config(state="disabled")
        p2.grid(row=0,column=1)
        #Button 3; if at page 3 or later, should be the current page
        if start_page <= 2:
            p3 = Button(page_grid, text = "3", command=lambda i=2:jump(i))
        else:
            p3 = Button(page_grid,text = start_page+1, state="disabled")
        p3.grid(row=0,column=2)
        if start_page >= 2:
            p3.config(state='disabled')
            
        #Page 4; if at page 3 or later, should be 1 + current page. 
        if start_page <= 2:
            p4 = Button(page_grid, text = "4", command=lambda i=3:jump(i))
        elif (page_count - start_page) == 1:
            p4 = Button(page_grid, text = page_count, command=lambda i = page_count:jump(i))
        else:
            p4 = Button(page_grid, text = start_page+2, command=lambda i=start_page+1: jump(i))
        if (start_page+1) == page_count:
            p4.config(text="",state='disabled')
        p4.grid(row=0,column=3)
        #Page 5.
        p5 = Button(page_grid, text = page_count, command=lambda i=page_count-1:jump(i))
        if start_page >= (page_count -2):
            p5.config(text='',state='disabled')
        # if start_page == (page_count) or (start_page - page_count) <= 2:
            # disable_page(p5)
        p5.grid(row=0,column=4)
        
        jump_entry = Entry(page_grid)
        jump_entry.grid(row=0,column=5)
        jump_entry.bind("<Return>",direct_jump)
        def tab_jump(event):
            jump_entry.focus_set()        
        jump_entry.bind("<Q>",tab_jump)
        jump_button = Button(page_grid, text = "Jump", command = direct_jump) #TODO: maybe squish bar a bit
        jump_button.grid(row=0,column=6)

tag_list = None

#TODO: make initial image fit on window 
#TODO: Implement a fullscreen, track monitor resoltuion(borderless preferred) and make image fit onto that.
#If image too big, then needs to be smaller
def view_img(img):

    print("Opening image:", img) 

    image = Image.open(img)
    image_viewer = Toplevel()
    image_viewer.minsize(1920, 1080)

    grid = Frame(image_viewer)
    add_text = Label(grid, text="Add Tags")
    add_text.grid(row=0, column=0, sticky="nw")

    tag_list = Frame(grid, bg="#1111CC")
    tag_list.grid(row=2, column=0, sticky="nw", columnspan=2, pady=(0, 1000))

    tag_subtitle = Label(tag_list, text="Tags. Click to remove")
    tag_subtitle.pack(anchor='nw', side='top')

    smaller_image_size = (int(image.width * 0.8), int(image.height * 0.8))
    smaller_image = image.resize(smaller_image_size, Image.LANCZOS)

    img_label = Label(grid)
    img_label.image = ImageTk.PhotoImage(smaller_image)
    img_label.config(image=img_label.image)
    img_label.grid(row=1, column=2, padx=20, pady=20, sticky="n", rowspan=3)    
    
#tag SHOULD refer to the button's text.
    def delete_tag(tag):
        exif = image.getexif()
        if exif is not None:
            if 37510 in exif:
                user_comment = exif[37510].split(',') if exif[37510] else []
                # user_comment = user_comment.split(',')
                for i in range(len(user_comment)):
                    if tag == user_comment[i]:
                        user_comment.pop(i)
                        user_comment = ','.join(user_comment) #I think?
                        
                #need to remove button next.
                        for child in tag_list.winfo_children():
                            if child.cget("text") == tag:
                                child.destroy()
                        exif[37510] = ','.join(user_comment)
                        image.save(img,exif = exif)

    def add_tag(tag):
        # Split the input tag into a list
        tags = tag.split(',')
        
        # Retrieve the existing EXIF data
        exif = image.getexif()
        
        # Check if EXIF data is present
        if exif is not None:
            # Check if UserComment tag exists
            if 37510 in exif:
                # Get the existing UserComment value
                user_comment = exif[37510].split(',') if exif[37510] else []
                
                # Iterate over new tags and append them if not present
                for atag in tags:
                    if atag not in user_comment:
                        user_comment.append(atag)
                
                # Join the list and assign it back to UserComment
                exif[37510] = ','.join(user_comment)
            else:
                # If UserComment doesn't exist, create a new list with the tags and join it
                exif[37510] = ','.join(tags)
            
            # Save the image with the updated EXIF data
            image.save(img, exif=exif)
            print(exif)
       

    def add_tag_to_list(event=None, tag=None):
        # nonlocal tag_list
        if tag is not None: #Loading Tags from Image
            exif = image.getexif()
            if exif is not None:
                if 37510 in exif:
                    itags = exif[37510].split(',') if exif[37510] else []
                    for itag in itags:
                        tag_button = Button(tag_list,text=itag,command=lambda t=itag:delete_tag(t))
                        tag_button.pack()
        else: #adding tag from entry bar
            add_tag(add_tag_entry.get())
            itags = (add_tag_entry.get()).split(',')
            for itag in itags:
                tag_button = Button(tag_list, text = itag,command=lambda t=itag:delete_tag(t))
                tag_button.pack()
            add_tag_entry.delete(0, END)     

    add_tag_entry = Entry(grid, font=("Arial", 20))
    add_tag_entry.grid(row=1, column=0, sticky="nw", pady=20)
    add_tag_entry.bind("<Return>", add_tag_to_list)
    add_tag_button = Button(grid, command=add_tag_to_list,text="Add Tag")
    add_tag_button.grid(row=1,column=1,sticky='n',pady=20)
    
    # Check if exiftags exist and if UserComment tag (which is used here) exists
    ini_exif = image.getexif()
    if ini_exif is not None:
        for tag,value in ini_exif.items():
            if tag == 37510:
                add_tag(value)
                #add buttons here?
                itags = value.split(',')
                length = len(itags)
                i = 0
                while i < length:
                    if itags[i] == '':
                        itags.pop(i)
                        length -= 1
                    else:
                        i += 1
                #save here?
                ini_exif[37510] = ','.join(itags)
                image.save(img,exif = ini_exif)
                for itag in itags:
                    tag_button = Button(tag_list, text=itag, command=lambda t=itag:delete_tag(t))
                    tag_button.pack()
    grid.pack()


def show_image(spot_number, img):
    row_no = int(spot_number / 5)
    col_no = spot_number % 5
    img_button = None  # Initialize img_button before the try block
    try:
        photo = Image.open(img)
        photo.thumbnail(THUMBNAIL_SIZE)
        print(photo.info)

        thumbnail_image = ImageTk.PhotoImage(photo)

        img_button = Button(gallery_grid, image=thumbnail_image, command=lambda i=img: view_img(i))
        img_button.thumbnail_image = thumbnail_image  # Keep reference to thumbnail
        img_button.grid(row=row_no, column=col_no)
        grid_labels.append(img_button)
    except Exception as e:
        print(f"Error loading or displaying image: {e}")
    
    if img_button:
        print("Image added to grid_labels:", img_button) 



def search_key(event):
    search_results()

#widgets = the stuff to hold
#windows = stuff holding the widgets

front = Tk() # First Window of the App; Simply has the search bars by tags and such
front.title("Personal Board")
front.geometry(f"{resolution[0]}x{resolution[1]}")
front.config(background=f"{bg_file[1]}")
front.minsize(1280,720) #Lock window size to this minimum for now because unsure the cases for smaller resolutions

bg_frame = Frame(front)
bg_frame.pack(anchor='ne') 
bg_pick = Label(bg_frame, text="Set Background Color").grid(row=0,column=0)
bg_light = Button(bg_frame, text="Light",command=set_light,bg="white",fg="black").grid(row=0,column=1)
bg_dark = Button(bg_frame, text="Dark", command=set_dark,bg="grey",fg="white").grid(row=0,column=2)
bg_custom = Button(bg_frame, text="Custom", command=set_custom).grid(row=0,column=3)

directory_frame = Frame(front)
directory_frame.pack(anchor='center')
add_button = Button(directory_frame, text="Add Directory",command=add_direc).pack(side=LEFT)
delete_button = Button(directory_frame, text="Remove Directory",command=remove_direc).pack(side=RIGHT)

search_frame = Frame(front)
search_frame.pack(anchor='center',pady=50)
search_label = Label(search_frame, font=("Arial",20),text="Search Images by Tag").pack()
search_tags = Entry(search_frame, font=("Arial",20))
front.bind("<grave>", search_focus)
search_tags.pack()
search_tags.bind("<Return>", search_key)
search_button = Button(search_frame, text="Search",font=("Arial",15),command=search_results)
search_button.pack()

#want results grid below this stuff
global grid_labels
grid_labels = []

gallery_grid = Frame(front)
gallery_grid.pack()

page_grid = Frame(front)
page_grid.pack()

front.mainloop()

#when app closes:
settings.close()
database.close()

