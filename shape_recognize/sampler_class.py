from prettytable import PrettyTable

# Would be better to change it to a non-static class
#***************************** SAMPLER CLASS *********************************
class Sampler:
    number_of_tiles = 8

    low_blue = [115, 90, 0]             #format BGR!!
    high_blue = [195, 135, 20]

    low_black = [0, 0, 0]
    high_black = [60, 60, 60]

    low_white = [150, 180, 180]
    high_white = [256, 256, 256]

    low_green = [25, 70, 0]
    high_green = [80, 160, 70]

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
        if Sampler.matches(array, Sampler.low_blue, Sampler.high_blue):
            return 'bllue'                              #       pun intended
        if Sampler.matches(array, Sampler.low_black, Sampler.high_black):
            return 'black'
        if Sampler.matches(array, Sampler.low_white, Sampler.high_white):
            return 'white'
        if Sampler.matches(array, Sampler.low_green, Sampler.high_green):
            return 'green'

    @staticmethod
    def image_to_text_array(image, coord, number):         #This should be done much, much better
        result = [[]]
        a = 0
        b = 0
        table = PrettyTable()
        for element in coord.astype(int):
            result[b].append(Sampler.array_to_color(image[element[0][1]][element[0][0]]))
            a += 1
            if a == 8:
                table.add_row(result[b])
                a = 0
                b += 1
                result.append([])
        return table

    @staticmethod
    def matches(array, low, high):
        return array[0] in range(low[0], high[0]) and array[1] in range(low[1], high[1]) and array[2] in range(low[2], high[2])

# ************************************ /SAMPLER CLASS **********************************