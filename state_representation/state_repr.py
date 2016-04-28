from PIL import Image

class Repr:
    @staticmethod
    def create_representation(map):
        image = Image.new("RGB", (400, 400), "white")
        for i in range(0, len(map)):
            for j in range(0, len(map[0])):
                image.paste(Image.open('../state_representation/tiles/' + map[j][i] + '.jpg'), (i * 50, j * 50))
        return image
