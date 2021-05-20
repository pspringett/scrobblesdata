import os
import sys
import csv

import scrobblesfixup
import json
from optparse import OptionParser
import scrobbleswrite

import pprint

# All of these shold end up under scrobbles\data eventually.
fqpath = os.path.join("h:\\", "dev", "scrobbles", "data", "tracks")

months_as_string = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
]


def main():
    global options, fqpath

    _main_cmd_line()

    fx = scrobblesfixup.Fixup()

    if options.year == 0:
        if options.Month == 0:
            print("Fixup all scrobbles not supported")
            exit()
        else:
            print("Don't know which year you want")
            exit()
    else:
        if options.month == 0:
            print("Fixup all scrobbles for one year")
            for month in months_as_string:
                tracks = read_tracks_month(fqpath, str(options.year), month)
                if tracks is not None:
                    new_tracks = fixup_tracks(fx, tracks)
                    scrobbleswrite.write_tracks(new_tracks, replace="yes")

        else:
            print("Fixup scrobbles for year and month")
            tracks = read_tracks_month(fqpath, str(options.year), options.month2)
            if tracks is not None:
                new_tracks = fixup_tracks(fx, tracks)
                scrobbleswrite.write_tracks(new_tracks, replace="yes")


def read_tracks_month(fqpath, year, month):
    """Reads either the specified file."""

    base_fname = "tracks.json"
    fname = "-".join([year, month, base_fname])
    fqname = os.path.join(fqpath, year, fname)
    print("fqname={}".format(fqname))

    if os.path.exists(fqname):
        with open(fqname, "r", encoding="utf8") as fp:
            tracks = json.load(fp)
        return tracks

    else:
        print("File {} not found".format(fqname))
        return None


def fixup_tracks(fx, tracks):
    new_tracks = []
    for t in tracks:

        datetime = t[0]
        artist = t[1]
        album = t[2]
        title = t[3]

        artist, album = fx.fixup_scrobble_info(artist, album, title)
        new_tracks.append([datetime, artist, album, title])
    return new_tracks


def _main_cmd_line():
    """
    Interprets the command line parameters and stores them in global variables.
    In general these should not be changed by any part of this script.
    """
    global options

    # -------------------------------------------------------------------------
    # Create the options parser.
    # -------------------------------------------------------------------------
    usage = "Usage: %prog [options]"

    epilog = "Fixues up tracks based on the fixup/filtering functions."
    parser = OptionParser(usage, epilog=epilog)

    parser.add_option("-y", "--year", type="int", default=0)
    parser.add_option("-m", "--month", type="int", default=0)

    (options, args) = parser.parse_args()

    if options.month > 12:
        options.month = 12

    if options.month < 10:
        options.month2 = "0" + str(options.month)


if __name__ == "__main__":
    # print(sys.version)
    # print(sys, sys.executable)
    main()
