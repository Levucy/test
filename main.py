import requests
import pygame
import sys
import os
import math
from geopy.distance import distance


def main():
    global width, height, screen
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True

    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocodelist = []
    geocodelist1 = ['Салоники', 'Измир', 'Варна']
    ptcrd = []
    for i in range(len(geocodelist)):
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocodelist[i]}&format=json'
        # print(geocoder_request)
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # toponym1 = toponym["Point"]["pos"]
            # toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            # toponym_address0 = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coordinates = toponym["Point"]["pos"]
            # print(f'{toponym_coordinates}')

    plcrd = []
    for i in range(len(geocodelist1)):
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocodelist1[i]}&format=json'
        # print(geocoder_request)
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            point = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            plcrd.append(point["Point"]["pos"])
            print(f'{plcrd[i]}')

    length = length_calculator(plcrd)
    print(length)
    # print(f'{(distance1 + distance2) / 1000} км')
    print(plcrd)
    mediancrd = [(float(plcrd[0].split(' ')[0]) + float(plcrd[1].split(' ')[0]) + float(plcrd[2].split(' ')[0])) / 3,
                (float(plcrd[0].split(' ')[1]) + float(plcrd[1].split(' ')[1]) + float(plcrd[2].split(' ')[1])) / 3]
    print(mediancrd)
    mediancrd = str(mediancrd[0]) + ',' + str(mediancrd[1])

    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'  # '40d1649f-0493-4b70-98ba-98533de7710b'
    map_request = (f'{server_address}&pl={",".join(plcrd).replace(" ", ",")}'
                   f'&pt={mediancrd}&apikey={api_key}') # &ll={toponym_coordinates.replace(" ", ",")}&spn={"90,90"}
    print(map_request)
    response1 = requests.get(map_request)

    map_file = 'map.png'
    with open(map_file, "wb") as file:
        file.write(response1.content)
    mapp = load_image(map_file)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            screen.fill((0, 0, 0))
            screen.blit(mapp, (10, 10))
            font = pygame.font.Font(None, 50)
            text = font.render(length, True, (255, 255, 0))
            text_x = 100
            text_y = 500
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pygame.display.flip()
    pygame.quit()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def length_calculator(crd):
    dist = distance(crd[0], crd[1]).km
    dist0 = distance(crd[1], crd[2]).km
    return f'Расстояние: {round(dist + dist0, 2)} км'
    # side1 = abs(pt1lo - pt2lo) * math.cos(pt1la)
    # side2 = abs(pt1la - pt2la) * math.cos(pt1lo)
    # return math.sqrt(side1 ** 2 + side2 ** 2)


if __name__ == "__main__":
    main()