from prettytable import PrettyTable
import copy

# Would be better to change it to a non-static class
#***************************** SAMPLER CLASS *********************************
class Sampler:
    number_of_tiles = 8

    # low_blue = [105, 60, 0]             #format BGR!!
    # high_blue = [205, 155, 60]
    #
    # low_black = [0, 0, 0]
    # high_black = [70, 70, 70]
    #
    # low_white = [130, 130, 130]
    # high_white = [256, 256, 256]
    #
    # low_green = [5, 50, 0]
    # high_green = [80, 160, 70]

    debug = 1

    @staticmethod
    def check_colors(img, coord):
        temp = coord.astype(int)
        #print(array_to_color([190, 190, 190]))
        # for val in temp:
        #     print(array_to_color(img[val[0][1]][val[0][0]]))
            # print('x: ', val[0][1], '   ', 'y: ', val[0][0])
            # print(img[val[0][1]][val[0][0]][0])
            # print(img[val[0][1]][val[0][0]][1])                     #1 - width, 0 - height; COLOR FORMAT !!BGR!!
        return Sampler.image_to_text_array(img, coord, Sampler.number_of_tiles)

    @staticmethod
    def array_to_color(array):                          #WIOCHA ale nie rozgryzlem jak to zrobic slownikiem
        if Sampler.diff_bgr(array) < 40 and array[0] < 110:
            return 'black'
        if Sampler.diff_bgr(array) < 40 and array[0] > 130:
            return 'white'
        if Sampler.diff_bgr(array) > 80 and array[0] > array[1] > array[2]:
            return 'blue'
        if array[0] < array[1] > array[2]:
            return 'green'
        # if Sampler.matches(array, Sampler.low_blue, Sampler.high_blue):
        #     return 'blue'
        # if Sampler.matches(array, Sampler.low_black, Sampler.high_black):
        #     return 'black'
        # if Sampler.matches(array, Sampler.low_white, Sampler.high_white):
        #     return 'white'
        # if Sampler.matches(array, Sampler.low_green, Sampler.high_green):
        #     return 'green'

    @staticmethod
    def image_to_text_array(image, coord, number):         #This should be done much, much better
        result = [[]]
        a = 0
        b = 0
        table = PrettyTable()
        pos = []
        color = []
        clear_row = ['','','','','','','','']
        for element in reversed(coord.astype(int)):
            result[b].append(Sampler.array_to_color(image[element[0][1]][element[0][0]]))
            a += 1
            pos.append(str(element[0][1]) + ' ' + str(element[0][0]))
            color.append(str(image[element[0][1]][element[0][0]]))
            if a == number:
                table.add_row(result[b])
                table.add_row(pos)
                table.add_row(color)
                table.add_row(clear_row)
                color = []
                pos = []
                a = 0
                b += 1
                if b != number:
                    result.append([])
        if Sampler.debug == 1:
            print(table)
        return result

    @staticmethod
    def matches(array, low, high):
        return array[0] in range(low[0], high[0]) and array[1] in range(low[1], high[1]) and array[2] in range(low[2], high[2])

    @staticmethod
    def diff_bgr(array):
        array = array.astype(int)
        result = max([abs(array[2] - array[1]), abs(array[2] - array[0]), abs(array[1] - array[0])])
        return result

    @staticmethod
    def strarr_to_intarr(array):
        int_array = copy.deepcopy(array)
        arr = []
        verse = []
        for row in int_array:
            for element in row:
                square = {
                    'white': 0,
                    'blue': 1,
                    'green': 2,
                    'black': None
                }[element]
                if square is not None:
                    verse.append(square)
            arr.append(verse)
            verse = []
        return arr


# ************************************ /SAMPLER CLASS **********************************