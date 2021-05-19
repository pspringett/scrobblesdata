import os
import sys
import csv

# import fixup
import json
from optparse import OptionParser
import scrobbleswrite

import pprint

# All of these shold end up under scrobbles\data eventually.
in_fqpath = os.path.join("h:\\", "dev", "phome", "scrobbles", "data")
# out_fqpath = os.path.join("h:\\", "dev", "scrobbles", "data", "tracks")
# fixup_fqpath = os.path.join("h:\\", "dev", "gomod", "scrobbles", "data")


def main():
    global options, fqpath

    _main_cmd_line()

    scrobbles = read_raw_tracks_by_year(in_fqpath, options.year)

    # fx = fixup.Fixup(fixup_fqpath)

    tracks = []
    for s in scrobbles:
        # print(s["Datetime"])
        f = {}

        f["Datetime"] = s["Datetime"]
        f["Title"] = s["Title"]
        f["Artist"] = s["Artist"]
        f["Album"] = s["Album"]
        # artist, album = fx.fixup_scrobble_info(s["Artist"], s["Album"], s["Title"])
        tracks.append(f)

    list.sort(tracks, key=lambda scrobble: scrobble["Datetime"])
    # pprint.pprint(tracks[:2], indent=4)

    new_tracks = []
    for track in tracks:
        new_tracks.append([track["Datetime"], track["Artist"], track["Album"], track["Title"]])

    # pprint.pprint(new_tracks[:2], indent=4)
    scrobbleswrite.write_raw_tracks(new_tracks)
    scrobbleswrite.write_tracks(new_tracks)


def read_raw_tracks_by_year(fqpath, year):
    """Reads either the specified file.

    This returns a list of dictionary entries with 'names' keys appended
    to the supplied list.
    """

    names = ["Datetime", "Artist", "Album", "Title"]

    fname = "{}scrobbles.txt".format(str(year))

    fqname = os.path.join(fqpath, fname)
    print("fqname={}".format(fqname))

    if os.path.exists(fqname):
        # with open(fqname) as fp:
        #     reader = csv.reader(fp)
        #     for row in reader:
        #         print(row)
        fp = open(fqname, "r", encoding="utf8")
        # fp = open(fqname, "r")
        l1 = list(csv.DictReader(fp, fieldnames=names, dialect="excel-tab"))

    else:
        raise IOError("File {} not found".format(fqname))

    fname = "{}manual.txt".format(str(year))
    fqname = os.path.join(fqpath, fname)

    if os.path.exists(fqname):
        print("fqname={}".format(fqname))
        l2 = list(csv.DictReader(open(fqname, "r"), fieldnames=names, dialect="excel-tab"))
        l1 = l1 + l2

    return l1


def write_tracks_by_year(fqpath, year, tracks):
    fname = "{}tracks.json".format(str(year))
    fqname = os.path.join(fqpath, fname)
    with open(fqname, "w") as fp:
        json.dump(tracks, fp, indent=4)


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

    epilog = "Converts old-style scrobbles as a CSV file, to a list on a year-by year basis"
    parser = OptionParser(usage, epilog=epilog)

    parser.add_option("-y", "--year", type="int", default=0)

    (options, args) = parser.parse_args()


if __name__ == "__main__":
    # print(sys.version)
    # print(sys, sys.executable)
    main()
