# HOW TO START USING
~~Start it up by executing 'personal-board.py'~~
1. Download 'personal-board.exe' and 'settings.txt (keep them in the same folder together)
     1a. Download 'Sample Folder' if you'd like to experiment with other pictures before your own.
2. Run 'personal-board.exe'

# PERSONAL BOARD Tutorial / Demo

Add Folder: Add your folders to have its images scanned.
Only need to include the root folder; all subfolders will be scanned as well.

Remove Folder: 
Select folders to be excluded from being scanned (until you add them again)

Search Images by Tags
Search for your tags by a single space (You can use ENTER/RETURN here)
Or leave the searchbar blank to search all photos within specified folders to search through.
Tags are clustered in the UserComment tag and separated by commas
If you have 5+ pages of photos, the jumpbar lets you skip to the specified page (You can use ENTER/RETURN here)
Click on a photo you want to add tags to or view.

Viewing Image
Click on a picture you want to see the full size of.
You can add one or multiple tags by splitting them with a single space(You can use ENTER/RETURN here)
You can click on a tag's button to remove it.
Press ESC to close the window, or click the X.

## TUTORIAL/FEATURES in GIF format

## Adding a Folder & Displaying its images
![Image](https://github.com/user-attachments/assets/01a3a3e5-e700-4272-a1ce-b2ecc9081cd3)

##  Tagging an image and filtering search by tag
![Image](https://github.com/user-attachments/assets/92e0e897-cd28-448b-acdc-8143c1114a73)

## Deleting a tag from an image + what it does
![Image](https://github.com/user-attachments/assets/fcf4ea2f-d49a-4436-bd18-2e89129edc77)

## Tagging multiple images simulataneously
![Image](https://github.com/user-attachments/assets/3b1dc750-489f-4bf2-be6b-400f9ab25763)


# List of Personal TODOS / Known Issues: 
Deleting more than 1 tag at once is being wonky
  Tags being split into individual letters
Removing folders to search through doesn't work until next run of the program
During/After tagging multiple images simulatenously, previously touched/affected images gain tags even when unintended
If viewing a second page of images or further then searching a query with only 1 page of results, have to manually click back to first page.

Refactoring
Cleaning up code
Logic fixing
Adding key events to focus on the appropriate entry fields
Adding a fullscreen option for viewing the image
Adding zoom functionality on gallery mode.
~~Allow adding tags to multiple images at once from the gallery~~ Done
Loading optimization, especially for higher image counts.


QUICK HEADS UP
After moving onto Base64 Encoding for file paths, I can't automatically include the sample pictures folder into settings.txt
The old version is under the V1 branch.

# Revision History
7/30/25 - Created Executable & Added Sample Pictures
-Simply download 'personal-board.exe' and 'settings.txt', then run personal-board.exe

2/15/24 - Quality of Life Regarding Image Tagging
-You can now add/remove tags from multiple images on the front page rather than going through each individual image

2/5/24 - Refactoring and etc.
-In settings.txt, file paths run on Base64 to support UTF-8 / foreign folder names 
-Everything was put into a class and ran as a class object to help avoid globals
-Photo-viewing now takes your monitor's resolution into account to determine how it will be displayed
  Before, if the photo's dimensions were too big, you'd only be able to see one corner of it.

12/24/23 - First released.

##Technical Breakdown 

Written in Python, using Tkinter and Pillow.
This IS a work in progress, hopefully can add more features later.
For your (images') safety, probably backup your images before trying this out. I am not responsible for any loss incurred otherwise.

PersonalBoard uses your images' ExifData, specifically the UserComment tag (37510) . If you use this for other purposes, I advise against using PersonalBoard.


This is an application that is designed to work as a local imageboard. 
That is, importing your directories and their photos, and adding user tags to them so that they can later be searched for specifically.




