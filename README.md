Written in Python, using Tkinter and Pillow.
This IS a work in progress, hopefully can add more features later.
For your (images') safety, probably backup your images before trying this out. I am not responsible for any loss incurred otherwise.

PersonalBoard uses your images' ExifData, specifically the UserComment tag (37510) . If you use this, I advise against using PersonalBoard.


This is an application that is designed to work as a local imageboard. 
That is, importing your directories and their photos, and adding user tags to them so that they can later be searched for specifically.

USING PERSONALBOARD
Start it up by executing 'personal-board.py'

BREAKDOWN
Add Directory: Add your folders to have its images scanned.
Only need to include the root folder; all subfolders will be scanned as well

Remove Directory: 
Select folders to be excluded from being scanned (until you add them again)

Search Images by Tags
Search for your tags by a single space (You can use ENTER/RETURN here)
Or leave the searchbar blank for all of your photos.
Tags are clustered in the UserComment tag and separated by commas
If you have 5+ pages of photos, the jumpbar lets you skip to the specified page (You can use ENTER/RETURN here)
Click on a photo you want to add tags to or view.

Viewing Image
You can add one or multiple tags by splitting them with a single space(You can use ENTER/RETURN here)
You can click on a tag's button to remove it.

List of Personal TODOS: 
Refactoring
Cleaning up code
Logic fixing
Adding key events to focus on the appropriate entry fields
Resizing the viewed image from fullscreen to a size that is more viewable
Adding a fullscreen option for viewing the image
Allow adding tags to multiple images at once from the gallery


