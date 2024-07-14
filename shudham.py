from PIL import Image
from skimage import color
import numpy as np
from sys import argv



def get_primary_colors_lab(filename, pn):
    img = Image.open(filename)
    (width, height) = img.size
    pixels = {}
    for i in range(width):
        for j in range(height):
            pixel = img.getpixel((i, j))
            (r, g, b) = pixel[:3]
            if (r, g, b) in pixels:
                pixels[(r, g, b)] += 1
            else :
                pixels[(r, g, b)] = 0

    sorted_dict = dict(sorted(pixels.items(), key=lambda kv: kv[1], reverse=True))
    primary_colors = []
    for n, i in enumerate(sorted_dict):
        if n < pn:
            primary_colors.append(i)
        else:
            break
    primary_colors_rgb = {i: np.array([i for i in i]) for i in primary_colors}
    return primary_colors_rgb


def relate_colors(colors, ifile, ofile):
    print('processing ', ifile)
    img = Image.open(ifile)
    new_img = Image.new(img.mode, img.size)
    pixels_new = new_img.load()
    (width, height) = img.size

    def closest_color_lab(lab_pixel, primary_colors_lab):
        distances = {name: np.linalg.norm(lab_pixel - lab) for name, lab in primary_colors_lab.items()}
        return min(distances, key=distances.get)
    def get_pixel_lab(rgb):
        rgb_pixel = np.array([rgb[0],rgb[1],rgb[2]])
        return color.rgb2lab(np.reshape(rgb_pixel, (1, 1, 3)))[0][0]


    def get_related(rgb, colors):
        rgb_lab = get_pixel_lab(rgb) 
        return closest_color_lab(rgb_lab, colors)


    for i in range(width):
        for j in range(height):
            pixel = img.getpixel((i, j))
            rgb = pixel[:3]
            prim_col = get_related(rgb, colors)
            pixels_new[i, j] =  prim_col
    print('done\nsaved to ', ofile) 
    new_img.show()
    new_img.save(ofile)

def main():
    help_msg = """Image Cleaner Tool

    Description: 
        You can remove blurry/mixed color pixels which are between two objects in an image and hence sharppening the image.
        This tool can be useful to sharpen logo/text/svg/png images which are simple yet are not sharp.
        The tool requires to know the number of primary colors(main colors) of the image inorder to process the sharpened image.

        The arguments must be in the same order as shown in Usage.

    Usage: 
        python shudham.py -p 3 <input_image> <outputimage>
    """
    NO_ARGS = 5
    if len(argv) == NO_ARGS:
        pcols = int(argv[2])
        ifile = argv[3]
        ofile = argv[4]

        primary_colors = get_primary_colors_lab(ifile, pcols) 
        primary_colors_lab = {name: color.rgb2lab(np.reshape(rgb, (1, 1, 3)))[0][0] for name, rgb in primary_colors.items()}
        relate_colors(primary_colors_lab, ifile, ofile)
    else:
        print(help_msg)

if __name__ == '__main__':
    main()