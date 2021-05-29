"""
Front end to read items from the database.
"""

import scrobblesglobal as glb
import json
import os


def get_all():
    "Returns all scrobbles."
    all_time_list = []

    years = glb.get_years(glb.tracks_path)

    for year in years:
        all_time_list, year_list = get_year(int(year), all_time_list)

    print("track count={}".format(len(all_time_list)))
    return all_time_list


def get_year(year, all_time_list=None):

    year_list = []

    for month in glb.months_as_string:
        all_time_list, year_list, month_list = get_month(year, month, all_time_list, year_list)

    return (all_time_list, year_list)


def get_month(year, month, all_time_list=None, this_year_list=None):

    month_list = []
    fqname = get_month_file_name(year, month)
    if os.path.exists(fqname):
        with open(fqname, "r") as fp:
            month_list = json.load(fp)

        if all_time_list is not None:
            all_time_list.extend(month_list)

        if this_year_list is not None:
            this_year_list.extend(month_list)

    return (all_time_list, this_year_list, month_list)


def get_upto_year(up_to_year):

    full_list = []

    years = os.listdir(glb.tracks_path)
    years.sort()
    years = [x for x in years if valid_year(x) and int(x) < up_to_year]

    for year in years:
        full_list, _ = get_year(int(year), full_list)

    return full_list


def get_upto_month(up_to_year, up_to_month):

    full_list = []

    fqdir = os.path.join(glb.tracks_path, str(up_to_year))
    months = os.listdir(fqdir)
    months.sort()
    print(months)

    for month_file in months:
        fqname = os.path.join(fqdir, month_file)
        with open(fqname, "r") as fp:
            full_list = json.load(fp)

    return full_list


def valid_year(year):

    if len(year) != 4:
        return False
    if year[0] != "2":
        return False

    return True


def get_month_file_name(year, month):
    fname = "-".join([str(year), month, glb.base_tracks_fname])
    fqpath = os.path.join(glb.tracks_path, str(year))
    fqname = os.path.join(fqpath, fname)
    return fqname


if __name__ == "__main__":

    track1 = ["date1", "artist1", "album1", "track1"]
    track2 = ["date2", "artist2", "album2", "track2"]
    track3 = ["date2", "artist1", "album1", "track3"]

    tracks = [track1, track2, track3]

    _ = get_upto_year(2021)

    _ = get_upto_month(2021, 6)
