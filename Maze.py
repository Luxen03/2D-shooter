from PIL import Image
from pylab import *
import numpy as np
import cv2
import keyboard

worldMap = ((1, 1, 1, 1, 1, 1, 1, 1, 1),
            (1, 0, 0, 0, 1, 1, 0, 0, 1),
            (0, 0, 0, 1, 1, 0, 0, 0, 1),
            (0, 0, 0, 0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 1, 1, 1, 0, 1),
            (1, 0, 0, 0, 1, 1, 0, 0, 1),
            (0, 0, 0, 1, 1, 0, 0, 0, 1),
            (0, 0, 0, 0, 0, 0, 0, 0, 1),
            (0, 0, 0, 0, 1, 1, 1, 0, 1))

mode = 0
playerTransX = 2
playerTransY = 2
FOV = 60

img = np.array(Image.new(mode="RGB", size=(500, 500)))

def raycast(direction):
    xDir = sin(radians(direction % 360))
    yDir = cos(radians(direction % 360))
    xLen = len(worldMap[0])
    yLen = len(worldMap)

    distance = 0

    while distance < 12:
        distance += 0.01
        xPoint = xDir * distance + playerTransX
        yPoint = yDir * distance + playerTransY
        if (xPoint >= xLen or xPoint < 0 or yPoint >= yLen or yPoint < 0):
            return 100
        elif (worldMap[int(xPoint)][int(yPoint)] == 1):
            return distance
        if (mode == 1):
            img[int(yPoint / yLen * len(img)), int(xPoint / xLen * len(img[0]))] = (0, 0, 255)
    return 0

def render():
    if mode == 0:
        for xScreen in range(len(img[0])):
            distance = raycast((rotation - FOV / 2 + xScreen / len(img[0]) * FOV)) / 6 * 255
            for yScreen in range(len(img)):
                if (yScreen < len(img[0]) - distance / 255 * 400 and yScreen > distance / 255 * 400):
                    img[yScreen, xScreen] = (255 - distance, 255 - distance, 255 - distance)
                else:
                    img[yScreen, xScreen] = (0, 0, 0)
    elif mode == 1:
        xLen = len(worldMap[0])
        yLen = len(worldMap)
        for xScreen in range(len(img[0])):
            for yScreen in range(len(img)):
                xPoint = xScreen / len(img[0]) * len(worldMap[0])
                yPoint = yScreen / len(img) * len(worldMap)
                if (xPoint >= xLen or xPoint < 0 or yPoint >= yLen or yPoint < 0):
                    continue
                elif (worldMap[int(xPoint)][int(yPoint)] == 1):
                    img[yScreen, xScreen] = (255, 255, 255)
                else:
                    img[yScreen, xScreen] = (0, 0, 0)
        for xScreen in range(len(img[0])):
            distance = raycast((rotation - FOV / 2 + xScreen / len(img[0]) * FOV))
rotation = 0
while True:
    render()
    cv2.imshow("FIRST PERSON SHOOTER", img)
    cv2.waitKey(1)
    if (keyboard.read_key() == "a"):
        rotation -= 10
    elif (keyboard.read_key() == "d"):
        rotation += 10
    elif (keyboard.read_key() == "w"):
        playerTransX += sin(radians(rotation)) * 0.2
        playerTransY += cos(radians(rotation)) * 0.2
    elif (keyboard.read_key() == "s"):
        playerTransX -= sin(radians(rotation)) * 0.2
        playerTransY -= cos(radians(rotation)) * 0.2
