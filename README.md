# SNAPPED

## What
A tool for replacing a person's face in a collection of images with another person's face.

Point it at a collection of images, an image of the target person and an image of another person.
It will search all the images in the collection and replace all occurrences of target person's face with the other face you provided, 
thus snapping the target away with a snap of your fingers.

## Setup
```
apt install -y python3 python3-pip cmake git python3-opencv
pip3 install face-recognition numpy scipy dlib flask
# Credit to https://github.com/ageitgey/face_recognition and https://github.com/wuhuikai/FaceSwap
```

## Run
Place the images in the `images` directory.
```
# Command-line script:
python3 snap.py <target_image> <new_person_image>

# To run the server:
FLASK_APP=server.py flask run
# Server is accessible on localhost:5000
```

## Who
Authors:
- Jan Hartman
- Rok Kanduti
- Martin Kozmelj
- Luka Zlatečan

Winners of Best Software Hack award and overall 3rd place award at DragonHack 2019.