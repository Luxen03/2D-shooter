from PIL import Image
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import keyboard

worldMap = ((1,1,1,1,1,1,1,1),
            (0,0,0,0,0,0,0,1),
            (0,0,0,0,0,0,0,1),
            (0,0,0,0,0,0,0,1),
            (0,0,0,0,0,0,0,1)
            )
img = np.array(Image.new(mode="RGB", size=(len(worldMap[0]) * 10, len(worldMap) * 10)))
plt.ion()

playerX = 2
playerY = 2
rotation = -90

#clear
def clear():
    for screenX in range(len(img[0])):
        for screenY in range(len(img)):
            img[screenY, screenX] = (255, 255, 255)

def raycast(direction, origX, origY):
    dirX = sin(radians(direction))
    dirY = cos(radians(direction))

    pointX = origX
    pointY = origY

    distance = 0

    while pointX >= 0 and pointX < len(worldMap) and pointY >= 0 and pointY < len(worldMap[0]) and distance < 1:
        distance += 0.05
        pointX = dirX * distance + origX
        pointY = dirY * distance + origY
        img[min(int(pointX / len(worldMap) * len(img)), len(img) - 1),
            min(int(pointY / len(worldMap[0]) * len(img[0])), len(img[0]) - 1)] = (255, 0, 0)

while True:
    clear()
    if (keyboard.is_pressed('w')):
        playerX += sin(radians(rotation)) * 0.1
        playerY += cos(radians(rotation)) * 0.1
    elif (keyboard.is_pressed('s')):
        playerX -= sin(radians(rotation)) * 0.1
        playerY -= cos(radians(rotation)) * 0.1
    elif (keyboard.is_pressed('a')):
        playerX -= cos(radians(rotation)) * 0.1
        playerY += sin(radians(rotation)) * 0.1
    elif (keyboard.is_pressed('d')):
        playerX += cos(radians(rotation)) * 0.1
        playerY -= sin(radians(rotation)) * 0.1
    elif (keyboard.is_pressed('q')):
        rotation -= 3
    elif (keyboard.is_pressed('e')):
        rotation += 3
    img[min(int(playerX * 10), len(img) - 1), min(int(playerY * 10), len(img[0]) - 1)] = (0, 0, 255)
    raycast(rotation, playerX, playerY)
    plt.imshow(img)
    plt.show()
    plt.pause(0.001)
    plt.clf()
