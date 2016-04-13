from PIL import Image
import numpy
import matplotlib.pyplot as plt
import glob
import scipy

def createBlankMap():
    im = Image.new("RGB", (400, 400), "white")
    im.save('base.jpg')


baseMap =   [
                ['w', 'bb', 'w', 'bb', 'w', 'bb', 'w', 'bb'],
                ['bb', 'w', 'bb', 'w', 'bb', 'w', 'bb', 'w'],
                ['w', 'bb', 'w', 'bb', 'w', 'bb', 'w', 'bb'],
                ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
                ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
                ['wb', 'w', 'wb', 'w', 'wb', 'w', 'wb', 'w'],
                ['w', 'wb', 'w', 'wb', 'w', 'wb', 'w', 'wb'],
                ['wb', 'w', 'wb', 'w', 'wb', 'w', 'wb', 'w']
            ]

anotherMap = [
                ['w', 'bb', 'w', 'bb', 'w', 'bb', 'w', 'bb'],
                ['bb', 'w', 'bb', 'w', 'bb', 'w', 'bb', 'w'],
                ['w', 'bb', 'w', 'wb', 'w', 'bb', 'w', 'bb'],
                ['b', 'w', 'b', 'w', 'bb', 'w', 'b', 'w'],
                ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'wb'],
                ['wb', 'w', 'b', 'w', 'wb', 'w', 'b', 'w'],
                ['w', 'wb', 'w', 'wb', 'w', 'wb', 'w', 'wb'],
                ['wb', 'w', 'wb', 'w', 'wb', 'w', 'wb', 'w']
            ]

createBlankMap()
base = Image.open('base.jpg')

for i in range(0, len(anotherMap[0])):
    for j in range(0, len(anotherMap)):
        base.paste(Image.open('tiles/' + anotherMap[j][i] + '.jpg'), (i * 50, j * 50))
base.save('processed2.jpg')
