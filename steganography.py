# 
# Names: Ethan Koestler, Marissa Manata, Jack Hovland, Ryley Larson
# Date: 11/2021
# Purpose: Steganography encoding/decoding for images
# 

from PIL import Image
import numpy as np

encode_key = '$t3g0'

# get message from user, if msg is '' that means a msg hasn't been passed from the gui.py
def receiveMessage(msg=''):
    if msg == '':
        return input('Enter your secret message: ')
    else:
        return message


# get image from user to encode
def receiveImageToEncode():
    return input('Enter name of your image (INCLUDE EXTENSION): ')

# get image from user to decode
def receiveImageToDecode():
    return input('Enter name of your image (INCLUDE EXTENSION): ')

# returns the inputted message converted to binary
def messageToBin(message):
    if type(message) == str:
        return ''.join( [format(ord(i), '08b') for i in message])
    elif type(message) == bytes:
        return [ format(i, '08b') for i in message]
    elif type(message) == int:
        return [ format(message, '08b')]
    else:
        raise ValueError('Invalid input!')

# encodes the secret message into an inputted image
def encodeImage(encoded, image):
    im = Image.open(image, 'r')     # open image
    width, height = im.size
    array = np.array(list(im.getdata()))    # list of all pixel data from image

    # get number of total pixels based on if image is RGB or RGBA
    if im.mode == 'RGB':
        n = 3
    elif im.mode == 'RGBA':
        n = 4
    totalPixels = array.size//n
    requiredPixels = len(encoded)

    if requiredPixels > totalPixels:    # check if image is large enough to store secret message
        print('Please use a larger image')
    else:
        index = 0
        for p in range(totalPixels):
            for i in range(0, 3):
                if index < requiredPixels:
                    array[p][i] = int(bin(array[p][i])[2:9] + encoded[index], 2)    # add secret message bit to lsb
                    index += 1

        array = array.reshape(height, width, n)     # reshape array to image size
        encodedImage = Image.fromarray(array.astype('uint8'), im.mode)      # create new image (Pillow) from numpy array
        encodedFileName = 'EncodedImage.png' #input('Enter name for encoded file (INCLUDE EXTENSION): ')    # get file name
        encodedImage.save(encodedFileName)  # save new image
        print('encode successful')

def decodeImage(image):
    im = Image.open(image, 'r')     # open image
    array = np.array(list(im.getdata()))    # list of all pixel data from image

    # get number of total pixels based on if image is RGB or RGBA
    if im.mode == 'RGB':
        n = 3
    elif im.mode == 'RGBA':
        n = 4
    totalPixels = array.size//n

    # create secret message binary
    secretBits = ''
    for p in range(totalPixels):
        for i in range(0, 3):
            secretBits += (bin(array[p][i])[2:][-1])    # get secret message bit from lsb

    # separate into bytes of binary bit data
    secretBits = [secretBits[i:i+8] for i in range(0, len(secretBits), 8)]

    # create secret message from binary secretBit data
    message = ''
    for i in range(len(secretBits)):
        if message[-5:] == '$t3g0':
            break
        else:
            message += chr(int(secretBits[i], 2))
    if '$t3g0' in message:      # check for key to print message
        print('Hidden Message:', message[:-5])
    else:   # if no key, no message
        print('Hidden Message: No Hidden Message Found!')

    print('decode successful')
    return message[:-5]

if __name__ == '__main__':
    print('Beginning steganography ... ')
    print('Please select an option: ')
    print('1: Encode')
    print('2: Decode')
    option = input()                            # get option input from user
    if option == '1':
        message = receiveMessage() + encode_key   # add key to secret message
        encodedMessage = messageToBin(message)  # convert message to bin
        image = receiveImageToEncode()          # get image from user
        print('Encoding ... ')
        encodeImage(encodedMessage, image)      # encode image with secret message
        print('Encoded image saved.')
    elif option == '2':
        print('Enter image to decode: ')
        secretImage = receiveImageToDecode()    # get image from user
        print('Decoding ... ')
        decodeImage(secretImage)                # decode image
    else:
        print('Please choose either 1 or 2')    # incorrect option input
