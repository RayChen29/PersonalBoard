# from test_class import PersonalBoard
#Libraries here
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageTk, ExifTags
from PIL.ExifTags import TAGS
import os
import glob #not needed?
import base64
from win_unicode_console import enable
enable()

DEFAULT_BG_0 = "#FFFFFF"  # White mode
DEFAULT_BG_1 = "#2C3738"  # Dark mode
THUMBNAIL_SIZE = (100,100) #sample size, can experiment
DISPLAY_LIMIT = 20 #display up to this many images per page
#TODO: Maybe need to optimize loading speed for images.
#TODO Maybe turn the decoding process into a function?
class PersonalBoard:
    def __init__(self):
        #Tkinter stuff
        self.root = Tk()
        self.root.title("Personal Board")
        self.root.minsize(1280,720)
        self.root.bind("<Configure>", self.update_res)
        
        #read file, load background color, saved resolution,
        with open("settings.txt", "r") as settings:
            lines = settings.readlines()
            bg = lines[1].split("=")
            bg = bg[1][:7]
            self.root.configure(bg=bg)
            
            res = lines[0].split("x")
            res[0] = int(res[0][11:])
            res[1] = int(res[1][:-1])    
            self.root.geometry(f"{res[0]}x{res[1]}")

        self.bg_frame = Frame(self.root)
        self.bg_frame.pack(anchor='ne')
        self.bg_label = Label(self.bg_frame, text="Set Background Color").grid(row=0,column=0)
        self.bg_light = Button(self.bg_frame, text="Light",command=self.set_light,bg="white",fg="black").grid(row=0,column=1)
        self.bg_dark = Button(self.bg_frame, text="Dark", command=self.set_dark,bg="grey",fg="white").grid(row=0,column=2)
        self.bg_custom = Button(self.bg_frame, text="Custom", command=self.set_custom).grid(row=0,column=3)
        
        self.folder_frame = Frame(self.root)
        self.folder_frame.pack(anchor='center')
        self.add_button = Button(self.folder_frame, text="Add Folder",command=self.add_folder).pack(side=LEFT)
        self.delete_button = Button(self.folder_frame,text="Delete Folder",command=self.delete_folder).pack(side=RIGHT)
        
        self.search_frame = Frame(self.root)
        self.search_frame.pack(anchor='center',pady=50)
        self.search_label = Label(self.search_frame, font=("Arial",20),text="Search Images by Tag").pack()
        self.search_tags = Entry(self.search_frame, font=("Arial",20))
        self.root.bind("<grave>", self.search_focus)
        self.search_tags.pack()
        self.search_tags.bind("<Return>", self.search_key)
        self.search_button = Button(self.search_frame, text="Search", font=("Arial", 15), command=self.search_results)
        self.search_button.pack()        
        
        self.all_folders = []
        self.all_photos = []
        self.results = []
        self.grid_labels = []
        self.gallery_grid = Frame(self.root)
        self.gallery_grid.pack()
        self.page_grid = Frame(self.root)
        self.page_grid.pack()
        
        #Max Resolution of (main?) monitor screen
        self.screen_x = self.root.winfo_screenwidth()
        self.screen_y = self.root.winfo_screenheight()
        
        self.query = "" #maybe need to use later?
        self.root_path = os.getcwd()

        
    #NON-MEANINGFUL METHODS HERE
    def update_res(self, event):
        try:
            os.chdir(self.root_path)
            with open("settings.txt", "r+") as settings:
                xy = []
                xy.append(str(event.width))
                xy.append(str(event.height))
                res = 'x'.join(xy)
                lines = settings.readlines()
                lines[0] = "resolution=" + res + "\n"
                settings.seek(0)
                settings.writelines(lines)
                settings.truncate()
                settings.flush()
        except Exception as e:
            print(f"Error in update_res: {e}")
            
    def search_focus(self,event):
        self.search_tags.focus_set()
        
    def search_key(self,event):
        self.search_results()
    
    def set_light(self):
        self.root.config(background=DEFAULT_BG_0)
        self.edit_line(1,"bgcolor=" + DEFAULT_BG_0)
 
    def set_dark(self):
        self.root.config(background=DEFAULT_BG_1)
        self.edit_line(1,"bgcolor=" + DEFAULT_BG_1)        
    
    def set_custom(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.root.config(background=color[1])
            self.edit_line(line_no=1,text="bgcolor="+color[1]+"\n")
            
    #TODO: Maybe add a transparent custom background option

    #MEANINGFUL METHODS HERE
    def add_folder(self):
        #TODO: Find out how to correct encoding.
        os.chdir(self.root_path)
        with open("settings.txt", "r+", encoding="utf-8") as settings:
            lines = settings.readlines()
            folderpath = filedialog.askdirectory()
            #encode below
            for line in lines:
                if folderpath == line:
                    print("Uhhhh")
                    return
            #I'm assuming this "Hides" the path in the textfile.
            folderpath_fix = base64.b64encode(folderpath.encode('utf-8')).decode('utf-8') + '\n'
            settings.write(folderpath_fix)
            
    def delete_folder(self):
        #TODO: Figure a streamlined way to delete lines from file AS we delete from Listbox.
        def remove():
            ind = int(del_list.curselection()[0]) + 7
            self.edit_line(ind, "")  # Leaves a blank line, pref. to remove it, but eh.
            del_list.delete(del_list.curselection())
            #UNSURE if below 2 lines are needed here
            # Now, `decoded_path` contains the original UTF-8 folder path 
            print('decoded path = ', decoded_path)
 
        del_window = Toplevel()
        del_window.geometry("600x700+600+0")#This just happened to work.
        del_window.minsize(600,700)
        
        #TODO: maybe find way to delete residue lines from the textfile
        del_list = Listbox(del_window,width=75)
        with open("settings.txt","r+") as settings:
            lines = settings.readlines()
            for i in range(7,len(lines)):
                encoded_path = lines[i].strip()
                decoded_bytes = base64.b64decode(encoded_path.encode('utf-8'))
                decoded_path = decoded_bytes.decode('utf-8')
                del_list.insert(i - 7, decoded_path)            
        del_list.pack()
        button_frame=Frame(del_window)
        button_frame.pack(anchor='n')
        del_button = Button(button_frame,text="Remove Folder", command=remove)
        del_button.pack()
        
    def search_results(self):
        #get all subfolders first?
        # self.all_folders
        print("test")
        #Go to all (sub/)folders and append them to search locations
        self.results = [] #reset results upon launching
        tags = self.search_tags.get()
        
        def append_folders(folder):
            dir_list = os.listdir(folder)
            if len(dir_list) > 0:
                for dir in dir_list:
                    full_path = os.path.join(folder, dir)
                    if os.path.isdir(full_path):
                        append_folders(full_path)
            if folder not in self.all_folders and os.path.isdir(folder):
                self.all_folders.append(folder)
        os.chdir(self.root_path)
        with open("settings.txt", "r") as settings:
            lines = settings.readlines()
            for i in range(7,len(lines)):
                encoded_path = lines[i].strip()
                decoded_bytes = base64.b64decode(encoded_path.encode('utf-8'))
                decoded_path = decoded_bytes.decode('utf-8')
                if decoded_path not in self.all_folders:
                    self.all_folders.append(decoded_path)

        # Add subfolders to all_folders
        for folder in self.all_folders:
            if not os.path.exists(folder):
                continue
            append_folders(folder)
        #Check all folders and subfolders for all photo paths, append them to all_photos
        for folder in self.all_folders:
            os.chdir(folder)
            files = os.listdir(folder)
            #open all files in folder
            for file in files:
                if os.path.isfile(file):
                    full_path = os.path.join(folder,file).replace("\\","/") #here b/c of some quirk, unsure if needed
                    if full_path not in self.all_photos:
                        self.all_photos.append(full_path)
                # Populate self.results based on user's tags
        tags = self.search_tags.get()
        for photo in self.all_photos:
            if self.filter_photos(photo, tags) == True:
                self.results.append(photo)
                
        # self.display_page(0) #CPT
        self.show_results() 
        
    def filter_photos(self,photo: str, tags:str) -> bool:
        if tags == '': #if tag entry is empty, auto-pass
            return True
        #photo is the path, img is the opened file
        img = Image.open(photo)
        exif = img.getexif()
        #Search UserComment, split it, and search
        if exif is not None:
            if 37510 in exif:
                user_comment = exif[37510].split(',') if exif[37510] else []
                for stag in tags:
                    if stag not in user_comment:
                        return False
                return True
        return False #Assuming here that, if no exif is found, auto-return false
    
    def show_results(self):
        #Show result photos on grid
        print("Show Results")
        #do the tag work and the filter work below
        #grid label stuff. So far copied from og
        if self.grid_labels is not None:
            for label in self.grid_labels:
                label.destroy()
            self.grid_labels = [] #Reset labels
            
        page_count = int((len(self.results)/ DISPLAY_LIMIT))
        if (len(self.results) % DISPLAY_LIMIT) > 0:
            page_count += 1
        self.display_page(0)
        self.update_page_label(0,page_count)

#This block below might need help.
    def show_image(self,spot_no,img): #Maybe change to square root or something?
        row = int(spot_no / 5)
        col = spot_no % 5
        img_button = None #initialize this before tryblock?
        try:
            photo = Image.open(img)
            photo.thumbnail(THUMBNAIL_SIZE)
            print(photo.info)
            thumbnail_image = ImageTk.PhotoImage(photo)
            img_button = Button(self.gallery_grid, image=thumbnail_image, command=lambda i=img: self.view_img(i))
            # img_button = Button(self.gallery_grid, image=thumbnail_image, command=lambda i=img: self.view_img()
            img_button.thumbnail_image = thumbnail_image  # Keep reference to thumbnail
            img_button.grid(row=row, column=col)
            self.grid_labels.append(img_button)
        except Exception as e:
            print(f"Error loading or displaying image: {e}")
        if img_button:
            print("Image added to grid_labels:", img_button)           
        
    def display_page(self,page_no):
        if len(self.results) > 0:
            for i in range(DISPLAY_LIMIT * page_no, min(DISPLAY_LIMIT * (page_no + 1), len(self.all_photos))):
                if i < len(self.results):
                    self.show_image(i, self.results[i]) #will want to change this logic later. Forget why.     
                    
                    
    #UPL - Page Buttons Grid Labels
    def update_page_label(self,page_no,page_count): #page_no = current page
        for widget in self.page_grid.winfo_children(): 
            widget.destroy()
        # start_page
        end_page = min(page_count,5) #max # of pages

    # TODO: Maybe find way to condense jump and direct jump into one method?
        def jump(i): #Clears widgets upon loading page i 
            for photo in self.gallery_grid.winfo_children():
                photo.destroy()
            self.display_page(i)
            self.update_page_label(i,page_count)
        def direct_jump(event=None):
            target_page = jump_entry.get()
            if target_page.isdigit():
                target_page = int(target_page) - 1
                if 0 <= target_page <= page_count - 1:
                    jump(target_page)
                if target_page >= page_count:
                    jump(page_count - 1)
        if end_page <= 4: #If 5 or less pages
            for i in range(page_no,end_page):
                page = Button(self.page_grid,text=str(i+1), command=lambda i=i:jump(i))
                if i == page_no:
                    page.config(state="disabled")
                page.grid(row=0,column=i)
#Need to account for scrolling up pages due to not seeing the prev buttons later on.
        else: 
            p1 = Button(self.page_grid, text = "1",command=lambda i=0:jump(i))
            if page_no == 0:
                p1.config(state="disabled")
            p1.grid(row=0,column=0)

            #Button 2. Should take you 1 page back.
            #Always display 2 if at page 3 or below
            if page_no <= 2: #if at page 
                p2 = Button(self.page_grid, text = "2", command=lambda i=1:jump(i))
            else:    
                p2 = Button(self.page_grid, text = (page_no), command=lambda i=(page_no-1):jump(i))
            if page_no == 1:
                p2.config(state="disabled")
            p2.grid(row=0,column=1)
            #Button 3; if at page 3 or later, should be the current page
            if page_no <= 2:
                p3 = Button(self.page_grid, text = "3", command=lambda i=2:jump(i))
            else:
                p3 = Button(self.page_grid,text = page_no+1, state="disabled")
            p3.grid(row=0,column=2)
            if page_no >= 2:
                p3.config(state='disabled')
                
            #Page 4; if at page 3 or later, should be 1 + current page. 
            if page_no <= 2:
                p4 = Button(self.page_grid, text = "4", command=lambda i=3:jump(i))
            elif (page_count - page_no) == 1:
                p4 = Button(self.page_grid, text = page_count, command=lambda i = page_count:jump(i))
            else:
                p4 = Button(self.page_grid, text = page_no+2, command=lambda i=page_no+1: jump(i))
            if (page_no+1) == page_count:
                p4.config(text="",state='disabled')
            p4.grid(row=0,column=3)
            #Page 5.
            p5 = Button(self.page_grid, text = page_count, command=lambda i=page_count-1:jump(i))
            if page_no >= (page_count -2):
                p5.config(text='',state='disabled')
            # if start_page == (page_count) or (start_page - page_count) <= 2:
                # disable_page(p5)
            p5.grid(row=0,column=4)
            #TODO: Find way to get focus to  work on jump_entry
            jump_entry = Entry(self.page_grid)
            jump_entry.grid(row=0,column=5)
            jump_entry.bind("<Return>",direct_jump)
            def tab_jump(event):
                jump_entry.focus_set()        
            jump_entry.bind("<Q>",tab_jump)
            jump_button = Button(self.page_grid, text = "Jump", command = direct_jump) #TODO: maybe squish bar a bit
            jump_button.grid(row=0,column=6)           

        print("Test_DONE?")
#TODO: might need to squish further. most kinks worked out, but still room to improve.
#TODO: Make image smaller and scale w window size
#TODO: Fix tag support.
    def view_img(self,img):
        photo = Image.open(img)
        photo_viewer = Toplevel()

        # photo_viewer.minsize(1366, 768)
        photo_viewer.minsize(self.screen_x, self.screen_y)
        photo_viewer.maxsize(self.screen_x, self.screen_y)

        grid = Frame(photo_viewer)
        add_text = Label(grid, text="Add Tags")
        add_text.grid(row=0, column=0, sticky="nw")

        tag_list = Frame(grid, bg="#1111CC")
        tag_list.grid(row=2, column=0, sticky="nw", columnspan=2, pady=(0, 1000))
#TODO: Make text appear right below entry. Seems to get pushed over by other stuff if too big.
        tag_subtitle = Label(tag_list, text="Tags. Click to remove")
        tag_subtitle.pack(anchor='nw', side='top')
        
        #Chat, width and height scaling + accounting for widgets, + shrink factor
        shrink_factor = 1.2 #Higher number = smaller image, because shrinks more.
        available_width = self.screen_x - tag_list.winfo_reqwidth()
        width_scale = min(1.0,available_width / (photo.width*shrink_factor))
        height_scale = min(1.0,self.screen_y / (photo.height*shrink_factor))

#TODO: Squish photo to be displayable at window's size (pref at all times). 
#TODO: Far future?: Add zoom feature. Maybe

        smaller_photo_size = (
            int(photo.width * min(width_scale,height_scale)),
            int(photo.height * min(width_scale, height_scale))               
        )
        smaller_photo = photo.resize(smaller_photo_size, Image.LANCZOS)

        photo_label = Label(grid)
        photo_label.image = ImageTk.PhotoImage(smaller_photo)
        
        photo_label.config(image=photo_label.image)
        photo_label.grid(row=1, column=2, padx=20, pady=20, sticky="n", rowspan=3)
               
        def delete_tag(tag):
            exif = photo.getexif()
            if exif is not None:
                if 37510 in exif:
                    user_comment = exif[37510].split(',') if exif[37510] else []
                    for i in range(len(user_comment)):
                        if tag == user_comment[i]:
                            user_comment.pop(i)
                            user_comment = ','.join(user_comment)
                            
                    #need to remove button next.
                            for child in tag_list.winfo_children():
                                if child.cget("text") == tag:
                                    child.destroy()
                            exif[37510] = ','.join(user_comment)
                            photo.save(img,exif = exif)

        def add_tag(tag):
            # Split the input tag into a list
            tags = tag.split(' ')
            # Retrieve the existing EXIF data
            exif = photo.getexif()
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
                photo.save(img, exif=exif)
                print(exif)

        def add_tag_to_list(event=None, tag=None):
            # nonlocal tag_list
            if tag is not None: #Loading Tags from Image
                exif = photo.getexif()
                if exif is not None:
                    if 37510 in exif:
                        itags = exif[37510].split(',') if exif[37510] else []
                        for itag in itags:
                            tag_button = Button(tag_list,text=itag,command=lambda t=itag:delete_tag(t))
                            tag_button.pack()
            else: #adding tag from entry bar
                add_tag(add_tag_entry.get())
                itags = (add_tag_entry.get()).split(' ')
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
        ini_exif = photo.getexif()
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
                    photo.save(img,exif = ini_exif)
                    for itag in itags:
                        tag_button = Button(tag_list, text=itag, command=lambda t=itag:delete_tag(t))
                        tag_button.pack()
        grid.pack()        
    def edit_line(self, line_no,text): #replace line_no with text
        with open("settings.txt","r+") as settings:
            lines = settings.readlines()
            #cpt?
            # if line_no < len(lines):
            if 0 <= line_no < len(lines):
                if text is not None:
                    lines[line_no] = text + '\n'
                else:
                    del lines[line_no]
                settings.seek(0)
                settings.writelines(lines)
                settings.truncate()
    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = PersonalBoard()
    app.run()
