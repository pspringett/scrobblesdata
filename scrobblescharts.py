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


def make_chart(tracks, key_type):

    unsorted_chart = {}
    for track in tracks:
        # print("Track={}".format(track))
        entry = TrackEntry(track[0], track[1], track[2], track[3])

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
        for line in range(item.gap):
            print("")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


def write_chart(fp, chart, title):
    fp.write("{}\n".format(title))
    for index, item in enumerate(chart):
        fp.write("{:4}: ({:4}) - {}\n".format(index + 1, item.count, item.key))
        for line in range(item.gap):
            fp.write("\n")
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker


# But also use partial function to supply key once, once we know it.
def get_key(key, artist, album, track):
    if key == "artist":
        return artist

    if key == "album":
        return " - ".join([artist, album])

    if key == "track":
        return " - ".join([artist, album, track])

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
