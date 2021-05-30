"""
Refreshes tracks data.

Fixes up mytracks to apply the existing rules.  Used when the rules change.
Note that this DOESN'T read rawtracks.

It overwrites existing files.
"""
import os
import sys
import csv

import scrobblesfixup
import json
from optparse import OptionParser
import scrobbleswrite
import scrobblesglobal as glb

import pprint


def main():
    global options, fqpath

    fx = scrobblesfixup.Fixup()

    years = glb.get_years(glb.tracks_path)

    for year in years:
        for month in glb.months_as_string:
            tracks = read_tracks_month(glb.tracks_path, year, month)
            if tracks is not None:
                new_tracks = fixup_tracks(fx, tracks)
                scrobbleswrite.write_tracks(new_tracks, replace="yes")


def read_tracks_month(fqpath, year, month):
    """Reads either the specified file."""

    base_fname = "tracks.json"
    fname = "-".join([year, month, base_fname])
    fqname = os.path.join(fqpath, year, fname)
    # print("fqname={}".format(fqname))

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


if __name__ == "__main__":
    # print(sys.version)
    # print(sys, sys.executable)
    main()
