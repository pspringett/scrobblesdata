import os

from collections import namedtuple
from pprint import pprint
import dataclasses


@dataclasses.dataclass(order=True)
class TrackEntry:
    datetime: str
    artist: str
    album: str
    track: str


@dataclasses.dataclass(order=True)
class ChartEntry:
    key: str
    count: int
    previous_count: int
    gap: int


@dataclasses.dataclass(order=True)
class SummaryEntry:
    total_tracks: int
    unique_artists: int
    unique_albums: int
    unique_tracks: int


compilations = {
    "soundtrack",
    "the story of trojan records",
    "30 years of punk",
    "a very special christmas",
    "50 of the greatest original xmas hits",
    "a tribute to gram parsons",
    "uncut",
    "crazy heart soundtrack",
    "nme c81",
    "tower of song - the songs of leonard cohen",
    "blowin' in the wind: a reggae tribute to bob dylan",
    "i'm not there",
    "eurovision song contest lisbon 2018",
    "rockers - original soundtrack",
}


def make_chart(tracks, key_type):

    unsorted_chart = {}
    for track in tracks:
        # print("Track={}".format(track))
        entry = TrackEntry(track[0], track[1], track[2], track[3])

        if key_type == "album":
            if entry.album.lower() in compilations:
                entry.artist = "Various"

        key = get_key(key_type, entry.artist, entry.album, entry.track)
        # print("key={}".format(key))

        if key not in unsorted_chart:
            chart_entry = ChartEntry(key, 0, 0, 0)
            unsorted_chart[key] = chart_entry

        unsorted_chart[key].count += 1
        unsorted_chart[key].previous_count += 1

    # pprint(basic_chart, indent=4)
    chart = list(dict.values(unsorted_chart))
    # pprint(chart_list, indent=4)

    chart.sort(key=lambda x: x.count, reverse=True)

    # Determine how many gaps to leave beween lines.
    last_entry = chart[0]
    for entry in chart[1:]:

        if last_entry.count > entry.count + 1:
            last_entry.gap = last_entry.count - entry.count - 1

        last_entry = entry

    return chart


def print_chart(chart):
    for index, item in enumerate(chart):
        print("{:4}: ({:4}) - {}".format(index + 1, item.count, item.key))
        if item.count > 10 and item.count < 50:
            for line in range(item.gap):
                print("")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


def write_chart(fp, chart, title=None, summary=None, gaps=True):

    if title is not None:
        write_title(fp, title)

    if summary is not None:
        write_summary(fp, summary)

    for index, item in enumerate(chart):
        fp.write("{:4}: ({:4}) - {}\n".format(index + 1, item.count, item.key))
        if item.count > 10 and item.count < 50:
            for line in range(item.gap):
                fp.write("\n")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


def write_title(fp, title):
    fp.write("{}\n".format(title))


def write_summary(fp, summary):
    fp.write(
        "{:8} {:13} {:13} {:13}\n".format(
            "Total Tracks", "Unique Artists", "Unique albums", "Unique Tracks"
        )
    )
    fp.write(
        "{:8} {:13} {:13} {:13}\n".format(
            summary.total_tracks,
            summary.unique_artists,
            summary.unique_albums,
            summary.unique_tracks,
        )
    )


def make_summary(tracks):
    """
    GIven a list of track, generates sumamry information for it.
    """
    unique_artists = {}
    unique_albums = {}
    unique_tracks = {}

    summary = SummaryEntry(0, 0, 0, 0)

    summary.total_tracks = len(tracks)

    for track in tracks:
        entry = TrackEntry(track[0], track[1], track[2], track[3])

        if entry.artist not in unique_artists:
            unique_artists[entry.artist] = 0
            summary.unique_artists += 1
        if entry.album not in unique_albums:
            unique_albums[entry.album] = 0
            summary.unique_albums += 1
        if entry.track not in unique_tracks:
            unique_tracks[entry.track] = 0
            summary.unique_tracks += 1

    return summary


# But also use partial function to supply key once, once we know it.
def get_key(key, artist, album, track):
    if key == "artist":
        return artist

    if key == "album":
        return " - ".join([album, artist])

    if key == "track":
        return "{} - {} ({})".format(track, artist, album)

    return None


if __name__ == "__main__":

    track1 = ["date1", "artist1", "album1", "track1"]
    track2 = ["date2", "artist2", "album2", "track2"]
    track3 = ["date2", "artist1", "album1", "track3"]
    track4 = ["date2", "artist1", "album1", "track4"]
    track5 = ["date2", "artist1", "album1", "track5"]
    tracks = [track1, track2, track3, track4, track5]

    print("Check artist list")
    chart = make_chart(tracks, "artist")
    print_chart(chart)

    print("Check album list")
    chart = make_chart(tracks, "album")
    print_chart(chart)

    print("Check track list")
    chart = make_chart(tracks, "track")
    print_chart(chart)

    # get_key_partial = partial(get_key, "artist")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1"

    # get_key_partial = partial(get_key, "album")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1 - album1"

    # get_key_partial = partial(get_key, "track")
    # key = get_key_partial("artist1", "album1", "track1")
    # assert key == "artist1 - album1 - track1"
