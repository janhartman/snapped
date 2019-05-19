import os
import pickle
import sys
import numpy as np
import face_recognition as fr
from PIL import Image

import swap

def snap(images, locations, encodings, target_im, swap_im):
    # Encoding of target face
    target_enc = fr.face_encodings(target_im)[0]
    print('Got encodings of target face')

    snapped = []

    for idx, im, locs, enc in zip(range(len(images)), images, locations, encodings):

        # Find if anyone matches the target
        tolerance = 0.6
        matches = fr.compare_faces(enc, target_enc, tolerance)
        print('Comparing to image', idx)

        for match, loc in zip(matches, locs):
            if match:
                print('Found match')

                top, right, bottom, left = loc
                extend = 90
                top = max(0, top - extend)
                bottom = min(im.shape[0], bottom + extend)
                left = max(0, left - extend)
                right = min(im.shape[1], right + extend)
                face = im[top:bottom, left:right]

                swapped_face = swap.swap(swap_im, face, warp_2d=True, correct_color=True)
                swapped = im.copy()
                swapped[top:bottom, left:right] = swapped_face

                snapped.append(swapped)
                
    return snapped

def unpickle(name):
    if os.path.isfile(f'{name}.pickle'):
        with open(f'{name}.pickle', 'rb') as f:
            return pickle.load(f)
    else:
        print(f'ERROR: no {name} found')

# Load images and embeddings
def load(load_saved=False):
    images = list(map(lambda i: fr.load_image_file(f'images/{i}'), os.listdir('images')))

    if load_saved:
        locations = unpickle('locations')
        encodings = unpickle('encodings')
        print('Loaded saved locations and encodings')
    else:
        locations = list(map(fr.face_locations, images))
        encodings = list(map(lambda x: fr.face_encodings(x[0], x[1]), zip(images, locations)))

        with open('locations.pickle', 'wb') as f:
            pickle.dump(locations, f)
        with open('encodings.pickle', 'wb') as f:
            pickle.dump(encodings, f)

        print('Computed face locations and encodings')

    return images, locations, encodings

if __name__ == '__main__':
    images, locations, encodings = load()

    # Images of target and new person
    if len(sys.argv) > 2:
        target_im = fr.load_image_file(sys.argv[1])
        swap_im = fr.load_image_file(sys.argv[2])
        swp = sys.argv[2]
    else:
        print('ERROR: provide command-line arguments for images')
        exit(1)

    snapped = snap(images, locations, encodings, target_im, swap_im)
    for i, s in enumerate(snapped):
        Image.fromarray(s).save(f'results/snapped_{i}.jpg')