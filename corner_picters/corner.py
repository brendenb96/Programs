#!/usr/bin/env python

import sys
from PIL import Image

SAMPLE_SIZE = 100
SAMPLE_RANGE = range(0,SAMPLE_SIZE)
REPLACE_PIXEL = (255,0,0)
BRIGHTNESS_THRESHOLD = 100

def main():

    imagePath = "recent_colour_average_buffer0.png"
    newImagePath = "out.png"
    im = Image.open(imagePath)
    pix = im.load()

    sample_count = (SAMPLE_SIZE * SAMPLE_SIZE) / 2

    photo_y_size, photo_x_size = im.size
    photo_x_size -= 1
    photo_y_size -= 1

    print "X Size: " + str(photo_x_size)
    print "Y Size: " + str(photo_y_size)

    # NW
    nw_sum = 0
    column_count = SAMPLE_SIZE
    for row in SAMPLE_RANGE:
        print_out = ""
        column_sample = range(0,column_count)
        for column in column_sample:
            pixel = pix[row, column]
            im.putpixel((row, column), REPLACE_PIXEL)
            nw_sum += sum(pixel)
        column_count -= 1

    nw_avg = nw_sum / sample_count
    print "NW AVG: %s" % nw_avg

    # ne
    ne_sum = 0
    column_count = SAMPLE_SIZE
    for row in SAMPLE_RANGE:
        print_out = ""
        column_sample = range(0,column_count)
        for column in column_sample:
            pixel = pix[row, (photo_x_size - column)]
            im.putpixel((row, (photo_x_size - column)), REPLACE_PIXEL)
            ne_sum += sum(pixel)
        column_count -= 1

    ne_avg = ne_sum / sample_count
    print "NE AVG: %s" % ne_avg

    # sw
    sw_sum = 0
    column_count = SAMPLE_SIZE
    for row in SAMPLE_RANGE:
        print_out = ""
        column_sample = range(0,column_count)
        for column in column_sample:
            pixel = pix[(photo_y_size - row), column]
            im.putpixel(((photo_y_size - row), column), REPLACE_PIXEL)
            sw_sum += sum(pixel)
        column_count -= 1

    sw_avg = sw_sum / sample_count
    print "SW AVG: %s" % sw_avg

    # se
    se_sum = 0
    column_count = SAMPLE_SIZE
    for row in SAMPLE_RANGE:
        print_out = ""
        column_sample = range(0,column_count)
        for column in column_sample:
            pixel = pix[(photo_y_size - row), (photo_x_size - column)]
            im.putpixel(((photo_y_size - row), (photo_x_size - column)), REPLACE_PIXEL)
            se_sum += sum(pixel)
        column_count -= 1

    se_avg = se_sum / sample_count
    print "SE AVG: %s" % se_avg

    total_avg = (nw_avg + sw_avg + ne_avg + se_avg)/4
    print "Total Avg: %s" % total_avg
    im.save(newImagePath)

    return 0

# Entry Point
#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
