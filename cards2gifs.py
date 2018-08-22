#!/usr/bin/env python3

import json
from plistlib import readPlist
import os, shutil
import re
from PIL import Image, ImageFont, ImageDraw


def anims_list(source, path):
    """
    Read source+'.plist' file to find unique animation keys.

    :param str source: file name without '.plist' extension.
    :return: list of strings for animations.
    """
    anims = []
    plist = readPlist(os.path.join(path, source+'.plist'))

    for frame in plist.frames.keys():
        frame_split = frame[len(source):].split('_')
        if frame_split[-2] in anims:
            continue
        anims.append(frame_split[-2])
    return anims


def create_anim_gif(source, anim, path, rename):
    """
    Create a gif image from the source+'.png' file for the specified animation.  Output gif file
    will be saved to same directory in format source+'_'+anim+'.gif' such that if source provided
    is 'neutral_koi' and anim is 'idle' the file 'neutral_koi_idle.gif' will be created.

    :param str source: source png file without '.png' extension.
    :param str anim: animation to create gif image for.
    :return: None
    """

    anim2 = anim
    if (anim2 == ''):
        anim2 = "actionbar"
    gif_name = '{}'.format(os.path.join(path,'{0}_{1}.gif'.format(rename, anim2)))
    if (os.path.isfile(os.path.join(path, gif_name))):
        print(gif_name + " already exists, skipping")
        return
    plist = readPlist(os.path.join(path, source+'.plist'))

    if anim == '':
        key_fingerprint = re.compile('{0}_[0-9][0-9][0-9]\.png'.format(source))
    else:
        key_fingerprint = re.compile('{0}_{1}_[0-9][0-9][0-9]\.png'.format(source, anim))

    frames = {}
    for frame in plist.frames.keys():
        if re.search(key_fingerprint, frame):
            f = frame.replace('.png', '')
            f = re.compile('_').split(f)[-1]
            frames[int(f)] = plist.frames[frame]

    pil_frames = []
    cpt = 0

    img = Image.open(os.path.join(path, source+'.png'))

    # Crop animation frames according to plist coordinates
    for f in frames:
        coords = [int(c) for c in frames[f].frame.replace('{', '').replace('}', '').split(',')]
        coords[2] += coords[0]
        coords[3] += coords[1]
        cropped_img = img.crop((coords))

        # Save frames to png format
        name = os.path.join(path,'{0}_{1}_{2}.png'.format(source, anim2, cpt))
        cropped_img.save(name)
        pil_frames.append(name)
        cpt += 1

    # Create list of png frames
    with open('image_list.txt', 'w') as file:
        for item in pil_frames:
            file.write("%s\n" % item)

    # Use ImageMagick to create the gif
    os.system('convert -dispose background @image_list.txt "{}"'.format(gif_name))
    # print(gif_name)

    # remove temp files
    for item in pil_frames:
        os.remove(item)
    # os.remove('image_list.txt')


def create_anims(source, path, rename):
    """
    Given a source name, identify the animations and create each animated gif from source png.

    :param str source: source for png and plist without the '.png' or '.plist' extension.
    :return: None
    """

    anims = anims_list(source, path)

    for anim in anims:
        create_anim_gif(source, anim, path, rename)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create gifs from Duelyst png and plist files. :P')
    parser.add_argument('source', type=str,
                        help='path to the units png and plist directory.')
    args = parser.parse_args()

    with open('cards.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for p in data:
            if p['id'] < 1000000:
                name = re.sub(' ', '_', p['name'])
                name = re.sub("'", "\'", name)
                name = re.sub(" Of ", " of ", name)
                name = re.sub(" The ", " the ", name)
                try:
                    slug = p['slug']
                    shutil.copy2(os.path.join(args.source, "{}.png".format(slug)), ".")
                    shutil.copy2(os.path.join(args.source, "{}.plist".format(slug)), ".")
                    create_anims(slug, "", name)

                except KeyError:
                    pass
                except FileNotFoundError:
                    # print("FileNotFoundError: " + name)
                    pass
                except Exception as ex:
                    print("Error: {0} - {1}".format(name, ex))
                    pass
