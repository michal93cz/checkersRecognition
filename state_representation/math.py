class Math:
    @staticmethod
    def alter_chessboard_middles(image, points):            #0 => height, 1=> width
        if points[0][0][0] > len(image) / 2 and points[0][0][1] > len(image[0]) / 2:        #warunki sa odwrocone dyz zmieniono kolejnosc pojawiania sie koordynatow
            return points
        if points[0][0][0] < len(image) / 2 and points[0][0][1] > len(image[0]) / 2:
            return Math.rotate(points, 90)
        if points[0][0][0] < len(image) / 2 and points[0][0][1] < len(image[0]) / 2:
            return Math.rotate(points, 180)
        if points[0][0][0] > len(image) / 2 and points[0][0][1] < len(image[0]) / 2:
            return Math.rotate(points, 270)

    @staticmethod
    def rotate(points, deg):
        temp = points.copy()
        for i in range(0, 8):
            for k in range(0, 8):
                a = i * 8 + k
                b = {
                    90: (8 - k - 1) * 8 + i,
                    180: 64 - a - 1,
                    270: k * 8 + (8 - i - 1)
                }[deg]
                temp[a] = points[b]
        return temp