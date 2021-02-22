import zipfile
from pytesseract import image_to_string
from PIL import Image
import cv2 as cv

face_cascade = cv.CascadeClassifier(r'D:\anaconda3\envs\opencv-project\opencv-project\haarcascade_frontalface_default.xml')

# opens the zip file and gets the name of the files aswell as the files themselves
# and extracts the items to a folder
with zipfile.ZipFile(r"D:\anaconda3\envs\new-opencv\src\small_img.zip", "r") as zp:
    image_name = {}
    images = {}
    i = 0
    for file in zp.namelist():
        image_name[i] = file
        images[i] = zp.open(file)
        i += 1 
    zp.extractall(r"D:\anaconda3\envs\new-opencv\src\images")

# creates a dictionary in which the key represents the number of the image it's analyzing
# using pytesseract library we can extract the words inside the image to strings
# store the strings inside the dictionary values 
text_in_image = {}
i = 0
for value in images.values():
    text_in_image[i]  = image_to_string(Image.open(value)).split()
    i += 1

# we search an input word and compare it agains the values inside of each dictionary
# if we find that input word inside the dictionary value list, we then return a True 
# if don't find the input word, we return a False
def searchWord(word):
    result = {}
    for list_number, text_list in text_in_image.items():
        if str(word) in text_list: 
            result[list_number] = True
        else: result[list_number] = False
    return result

# if we get the previous return value as True:
# using the opencv library we detect faces withing each image, we then crop those faces to a different image
# each image containing faces represents the results of one image that we extracted in the beginning
# if we get the previous return value as False:
# we print a line letting the user know that no word has been found inside the image, so no faces were cropped
def checkResults(result):
    for key, image in images.items():
        if result[key] == True:
            cv_image = cv.imread(r"D:\anaconda3\envs\new-opencv\src\images\{}".format(image_name[key]))
            gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            pil_image = Image.open(image)
            face_images = []
            for x, y, w, h in faces.tolist():
                cropped_image = pil_image.crop(box = (x, y, x + w, y + h))
                face_images.append(cropped_image)
            w, h = 0, 0
            for image in face_images:
                w = w + image.width
                if image.height > h: h = image.height
            contact_sheet = Image.new(face_images[0].mode, (w, h))
            x, y = 0, 0
            for image in face_images:
                contact_sheet.paste(image, (x, y))
                if x + image.width >= contact_sheet.width:
                    x = 0
                    y = y + image.height
                else:
                    x = x + image.width + 3
            contact_sheet.show()
        if result[key] == False:
            print("Word not found in the image {}".format(image_name[key]))

checkResults(searchWord("precincts"))