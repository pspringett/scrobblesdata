import os
from datetime import datetime
import json
from pathlib import Path


timestamp_format = "%Y-%m-%d %H:%M:%S"

timestamp_path = os.path.join("h:\\", "dev", "scrobbles", "data")
raw_tracks_path = os.path.join("h:\\", "dev", "scrobbles", "data", "rawtracks")
tracks_path = os.path.join("h:\\", "dev", "scrobbles", "data", "tracks")

# Tracks is a list of tracks where
# Track[0] is the timestamp: 2021-05-17 19:53:24
# Track[1] is the artist
# Track[2] is the album
# Track[3] is the track
# Tricksiness here is that we append to the the correct year file, so handle spltting over years.
# Want to be clverer than this, and mroe important for the write tarcks.
# for tracks to write:
#   if fname is different
#       if file is open, clsoe it
#       open the new file
#   write track


def write_raw_tracks(tracks):
    def write_raw_tracks_to_file(fp, tracks):
        for fields in tracks:
            fp.write(("\t".join(fields) + "\n"))

    raw_years = {}

    for track in tracks:
        # print(track)
        start_time = track[0]
        dt = datetime.fromisoformat(start_time)
        print(dt.year)

        if dt.year not in raw_years:
            raw_years[dt.year] = []
        raw_years[dt.year].append(track)

    for year, tracks in raw_years.items():

        fname = str(year) + "scrobbles.csv"
        fqname = os.path.join(raw_tracks_path, fname)

        if os.path.exists(fqname):
            print("Append raw tracks to filename={}".format(fname))
            with open(fqname, "a") as fp:
                write_raw_tracks_to_file(fp, tracks)

        else:
            print("write raw tracks to filename={}".format(fname))
            with open(fqname, "w") as fp:
                write_raw_tracks_to_file(fp, tracks)

    return


def write_tracks(tracks):
    print("Write tracks")

    fname = "tracks.json"

    # create a nested dictionary, ndexed by year, then month.
    tracks_by_year = {}
    for track in tracks:
        start_time = track[0]
        dt = datetime.fromisoformat(start_time)
        month = f"{dt:%m}"
        print(dt.year)
        print(month)

        if dt.year not in tracks_by_year:
            tracks_by_year[dt.year] = {}
            tracks_by_year[dt.year][month] = []

        if month not in tracks_by_year[dt.year]:
            tracks_by_year[dt.year][month] = []

        tracks_by_year[dt.year][month].append(track)

    # Walk the dictionary, writing out the files in the correct directories.
    for year, months in tracks_by_year.items():

        for month, tracks in months.items():

            directory = "-".join([str(year), month])
            fqpath = os.path.join(tracks_path, str(year), directory)
            fqname = os.path.join(fqpath, fname)
            print("track file = {}".format(fqname))
            Path(fqpath).mkdir(parents=True, exist_ok=True)

            if os.path.exists(fqname):
                print("Append raw tracks to filename={}".format(fname))
                with open(fqname, "a") as fp:
                    json.dump(tracks, fp, indent=4)
            else:
                print("write raw tracks to filename={}".format(fname))
                with open(fqname, "w") as fp:
                    json.dump(tracks, fp, indent=4)

    return


def write_timestamp():

    now = datetime.now()

    dt_string = now.strftime(timestamp_format)
    print("write timestamp =", dt_string)

    fqname = os.path.join(timestamp_path, "timestamp.json")
    with open(fqname, "w") as fp:
        json.dump(dt_string, fp)
    return


def read_timestamp():

    fqname = os.path.join(timestamp_path, "timestamp.json")
    with open(fqname, "r") as fp:
        dt_string = json.load(fp)
    print("read timestamp =", dt_string)

    d = datetime.strptime(dt_string, timestamp_format)

    return d
