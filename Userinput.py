import argparse
import os
import Constants as cs

parser = argparse.ArgumentParser()
parser.add_argument("--tickrate", help='Set the game speed between 5 and 20. Default = 10', type=int)
parser.add_argument("--filename", help='Pass your .txt file. Note: File has to be in the same folder as the gamefile')
parser.add_argument("--spawnrange", help='Set food spawnrate. 0 - food can spawn next to the wall, 1 - food will spawn 1 or more block further from the wall ', type=int)
parser.add_argument("--background", help='Pass your background image in .jpg or .png format')
args = parser.parse_args()
tickrate = args.tickrate
filename = args.filename
spawnrange = args.spawnrange
background = args.background


def get_tickrate():
    if tickrate is None:
        return cs.default_tickrate
    else:
        if tickrate in range(5, 21):
            return tickrate
        else:
            raise ValueError('Invalid number. Expected intiger between 5 and 20')


def get_spawnrange():
    default_spawnrange = 0
    if spawnrange is None:
        return default_spawnrange
    else:
        if spawnrange in range(0, 2):
            return spawnrange
        else:
            raise ValueError('Expected int: 0 or 1')


def get_users_map():
    if os.path.isdir(cs.default_filename):  # jeśli dostanie folder plików, to go usuwa, o ile ma uprawnienia
        os.rmdir(cs.default_filename)
    if not os.path.exists(cs.default_filename):
        with open(cs.default_filename, '+w') as f:
            f.close()
    if filename is None:
        return cs.default_filename
    else:
        if os.path.isfile(filename):
            return filename
        else:
            raise TypeError('.txt format required')


def get_background():
    default_background = cs.background_name
    if background is None:
        return default_background
    else:
        if '.jpg' in background or '.png' in background:  # tu warunek na zdjęcie
            return background
        else:
            raise Exception('Invalid file')


def get_wall_cords_from_file(filepath):
    positions = []
    dictionary = {
        0: 100, 1: 120, 2: 140, 3: 160,
        4: 180, 5: 200, 6: 220, 7: 240,
        8: 260, 9: 280, 10: 300, 11: 320,
        12: 340, 13: 360, 14: 380, 15: 400,
        16: 420, 17: 440, 18: 460, 19: 480
    }
    with open(filepath) as users_map:
        for line in users_map:
            positions.append(line.rstrip('\n').split())
        for lista in positions:
            for i in range(0, len(lista)):
                lista[i] = int(lista[i])
                if lista[i] > 19 or lista[i] < 0:
                    raise ValueError('You entered intigers which are not in interval <0,19>')
            for i, item in enumerate(lista):
                lista[i] = dictionary.get(item, item)
        for i in range(0, len(positions)):
            for lista in positions:
                if len(lista) > 2 or len(lista) == 1:
                    raise ValueError('Invalid arguments. Correct input: x y then newline')
                if not lista:
                    positions.remove(lista)
    return positions
