#! /usr/bin/env python
#
# This program evaluates brightness of a given file

import sys
from PIL import Image
import argparse
import colored

# brightness globals
SAMPLE_SIZE = 100
SAMPLE_RANGE = range(0, SAMPLE_SIZE)
BRIGHT_THRESHOLD = 50

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to perform evaliation on",type=str)

    args = parser.parse_args()

    test_file = args.file

    print "Starting brightness evaluation..."
    print "Using file: %s" % test_file

    # load the image
    try:
        im = Image.open(test_file)
        pix = im.load()
    except Exception as e:
        print colored.stylize("Error loading image: %s" % str(e), colored.fg("red"))
        return 1

    # evaluate image pixels
    # samples corners instead of strips
    try:
        # init
        sample_count = (SAMPLE_SIZE * SAMPLE_SIZE) / 2
        photo_y_size, photo_x_size = im.size
        photo_x_size -= 1
        photo_y_size -= 1

        # NW sample spot
        nw_sum = 0
        column_count = SAMPLE_SIZE
        for row in SAMPLE_RANGE:
            print_out = ""
            column_sample = range(0, column_count)
            for column in column_sample:
                pixel = pix[row, column]
                nw_sum += sum(pixel)
            column_count -= 1
        nw_avg = nw_sum / sample_count

        # SW sample spot
        sw_sum = 0
        column_count = SAMPLE_SIZE
        for row in SAMPLE_RANGE:
            print_out = ""
            column_sample = range(0, column_count)
            for column in column_sample:
                pixel = pix[row, (photo_x_size - column)]
                sw_sum += sum(pixel)
            column_count -= 1
        sw_avg = sw_sum / sample_count

        # NE sample spot
        ne_sum = 0
        column_count = SAMPLE_SIZE
        for row in SAMPLE_RANGE:
            print_out = ""
            column_sample = range(0, column_count)
            for column in column_sample:
                pixel = pix[(photo_y_size - row), column]
                ne_sum += sum(pixel)
            column_count -= 1
        ne_avg = ne_sum / sample_count

        # SE sample spot
        se_sum = 0
        column_count = SAMPLE_SIZE
        for row in SAMPLE_RANGE:
            print_out = ""
            column_sample = range(0, column_count)
            for column in column_sample:
                pixel = pix[(photo_y_size - row), (photo_x_size - column)]
                se_sum += sum(pixel)
            column_count -= 1
        se_avg = se_sum / sample_count

        # set total average
        total_avg = (nw_avg + sw_avg + ne_avg + se_avg) / 4.0

        # determine state
        if (total_avg > BRIGHT_THRESHOLD):
            print colored.stylize("Bright light found!", colored.fg("red"))
            print colored.stylize("Value:\t\t%s" % total_avg, colored.fg("red"))
        else: 
            print colored.stylize("No bright light.", colored.fg("green"))
            print colored.stylize("Value:\t\t%s" % total_avg, colored.fg("green"))
        
        print colored.stylize("Threshold:\t%s" % BRIGHT_THRESHOLD, colored.fg("blue"))

        print " ____________________________ "
        print "|      /             \\      |"
        print "|{0:^5}/               \\{0:^5}|".format(nw_avg, ne_avg)
        print "|    /                 \\    |"
        print "|___/                   \\___|"
        print "|                           |"
        print "|                           |"
        print "|                           |"
        print "|___                     ___|"
        print "|   \\                   /   |"
        print "|    \\                 /    |"
        print "|{0:^5}\\               /{0:^5}|".format(sw_avg, se_avg)
        print "|______\\_____________/______|"

    except Exception as e:
        print colored.stylize("Error calculating brightness: %s" % str(e), colored.fg("red"))
        return 1

    print "\nDone."
    return 0


#---------------------------
if (__name__ == "__main__"):
    sys.exit(main())
#---------------------------
