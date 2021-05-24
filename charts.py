import os

from collections import namedtuple
from pprint import pprint

TrackEntry = namedtuple("TrackEntry", "Datetime artist album track")


def make_chart(tracks, key):

    unsorted_chart = {}
    for track in tracks:
        # print("Track={}".format(track))
        entry = TrackEntry(track[0], track[1], track[2], track[3])

        key = " - ".join([entry.artist, entry.album])
        # print("key={}".format(key))

        if key not in unsorted_chart:
            unsorted_chart[key] = [key, 0, 0]

        unsorted_chart[key][1] += 1
        unsorted_chart[key][2] += 1

    # pprint(basic_chart, indent=4)
    chart = list(dict.values(unsorted_chart))
    # pprint(chart_list, indent=4)

    chart.sort(key=lambda x: x[1])

    return chart


def print_chart(chart):
    for index, item in enumerate(chart):
        print("{:4}: ({:4}) - {}".format(index + 1, item[1], item[0]))
        # 1: (1656) - David Bowie
        #   5: (232) - Scott 3 - Scott Walker
