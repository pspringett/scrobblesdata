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
def write_raw_tracks(tracks):
    def write_raw_tracks_to_file(fp, tracks):
        for fields in tracks:
            # print(fields)
            fp.write(("\t".join(fields) + "\n"))

    base_fname = "scrobbles.csv"

    # create a nested dictionary, indexed by year, then month.
    tracks_by_month = parse_tracks_to_write(tracks)

    # Walk the dictionary, writing out the files in the correct directories.
    for year, months in tracks_by_month.items():

        for month, tracks in months.items():

            # directory = "-".join([str(year), month])
            fname = "-".join([str(year), month, base_fname])
            fqpath = os.path.join(raw_tracks_path, str(year))
            fqname = os.path.join(fqpath, fname)
            # print("track file = {}".format(fqname))
            Path(fqpath).mkdir(parents=True, exist_ok=True)

            if os.path.exists(fqname):
                print("Append raw tracks to {}".format(fqname))
                # print(tracks)
                with open(fqname, "a", encoding="utf8") as fp:
                    write_raw_tracks_to_file(fp, tracks)
            else:
                print("write raw tracks to {}".format(fqname))
                with open(fqname, "w", encoding="utf8") as fp:
                    write_raw_tracks_to_file(fp, tracks)
    return


def write_tracks(tracks):
    def write_tracks_to_file(fp, tracks):
        json.dump(tracks, fp, indent=4)

    base_fname = "tracks.json"

    # create a nested dictionary, indexed by year, then month.
    tracks_by_month = parse_tracks_to_write(tracks)

    # Walk the dictionary, writing out the files in the correct directories.
    for year, months in tracks_by_month.items():

        for month, tracks in months.items():

            fname = "-".join([str(year), month, base_fname])
            fqpath = os.path.join(tracks_path, str(year))
            fqname = os.path.join(fqpath, fname)
            # print("track file = {}".format(fqname))
            Path(fqpath).mkdir(parents=True, exist_ok=True)

            if os.path.exists(fqname):
                print("Append tracks to {}".format(fqname))
                with open(fqname, "r") as fp:
                    new_tracks = json.load(fp)
                new_tracks.extend(tracks)
                new_tracks.sort(key=lambda x: x[0], reverse=False)
                with open(fqname, "w") as fp:
                    json.dump(new_tracks, fp, indent=4)
            else:
                print("write tracks to {}".format(fqname))
                with open(fqname, "w") as fp:
                    json.dump(tracks, fp, indent=4)

    return


def parse_tracks_to_write(tracks):
    tracks_by_month = {}
    for track in tracks:
        start_time = track[0]
        dt = datetime.fromisoformat(start_time)
        month = f"{dt:%m}"
        # print(dt.year)
        # print(month)

        if dt.year not in tracks_by_month:
            tracks_by_month[dt.year] = {}
            tracks_by_month[dt.year][month] = []

        if month not in tracks_by_month[dt.year]:
            tracks_by_month[dt.year][month] = []

        tracks_by_month[dt.year][month].append(track)
    return tracks_by_month


def write_tracks_by_month(tracks_by_month, tracks_path, fname, write_tracks_func):

    for year, months in tracks_by_month.items():

        for month, tracks in months.items():

            directory = "-".join([str(year), month])
            fqpath = os.path.join(tracks_path, str(year), directory)
            fqname = os.path.join(fqpath, fname)
            print("write tracks to filename={}".format(fqname))
            Path(fqpath).mkdir(parents=True, exist_ok=True)

            if os.path.exists(fqname):
                print("Append tracks to filename={}".format(fqname))
                with open(fqname, "a") as fp:
                    write_tracks_func(fp, tracks)
            else:
                print("write tracks to filename={}".format(fqname))
                with open(fqname, "w") as fp:
                    write_tracks_func(fp, tracks)


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
