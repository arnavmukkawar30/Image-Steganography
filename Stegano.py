# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
from cryptography.fernet import Fernet

#importing modules for python Image Steganography project
from tkinter import *
from tkinter.filedialog import * 
from PIL import ImageTk,Image
# from stegano import exifHeader as stg
from tkinter import messagebox


def encrypt_aes(msg):
    def pad(entry):
        padded = entry + (44 - len(entry) % 16 - 1) * 'a'
        padded = padded + '='
        return (padded)

    key = pad("VitPune")

    msg = msg.encode()
    f = Fernet(key)
    ciphertext = f.encrypt(msg)
    return ciphertext

def decrypt_aes(ct):

    def pad(entry):
        padded = entry + (44 - len(entry) % 16 - 1) * 'a'
        padded = padded + '='
        return (padded)

    key = pad(input("Enter the encryption PASSWORD:\n"))
    if key==pad("VitPune"):
        ciphertext=ct.encode('UTF-8')

        f = Fernet(key)
        cleartext = f.decrypt(ciphertext)

        cleartext = cleartext.decode()
        return cleartext
    else:
        print("wrong key!!!")
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


# Encode data into image
def enc():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, encrypt_aes(data).decode())

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


# Decode the data in the image
def dec():

    #
    Screen.destroy()
    DecScreen = Tk()
    DecScreen.title("Decode- TechVidvan")
    DecScreen.geometry("500x500+300+300")
    DecScreen.config(bg="pink")

    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


# Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        enc()

    elif (a == 2):
        a=dec()
        b=decrypt_aes(a)
        print("Decoded Word :  " + b)
    else:
        raise Exception("Enter correct input")


# Driver Code
if __name__ == '__main__':
    # Calling main function
    #main()
    # Initializing the screen for python Image Steganography project
    Screen = Tk()
    Screen.title("Image Steganography ")
    Screen.geometry("500x500+300+300")
    Screen.config(bg="blue")
    # creating buttons
    EncodeButton = Button(text="Encode", command=enc())
    EncodeButton.place(relx=0.3, rely=0.4)

    DecodeButton = Button(text="Decode", command=dec())
    DecodeButton.place(relx=0.6, rely=0.4)

    mainloop()

