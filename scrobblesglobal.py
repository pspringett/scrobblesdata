import os

timestamp_format = "%Y-%m-%d %H:%M:%S"

timestamp_path = os.path.join("h:\\", "dev", "scrobbles", "data")
raw_tracks_path = os.path.join("h:\\", "dev", "scrobbles", "data", "rawtracks")
tracks_path = os.path.join("h:\\", "dev", "scrobbles", "data", "tracks")
mycharts_path = os.path.join("h:\\", "dev", "scrobbles", "data", "mycharts")

base_tracks_fname = "tracks.json"

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

keys = ["artist", "album", "track"]

chart_fnames = {"artist": "artists.txt", "album": "albums.txt", "track": "tracks.txt"}


def valid_year(year):

    if len(year) != 4:
        return False
    if year[0] != "2":
        return False

    return True
