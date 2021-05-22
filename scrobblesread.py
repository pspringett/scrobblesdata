"""
Front end to read items from the database.
"""

import scrobblesglobal as glb
import json
import os


def get_all():

    all_time_list = []

    for year in os.listdir(glb.tracks_path):
        if len(year) != 4:
            continue
        if year[0] != "2":
            continue

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


def get_month_file_name(year, month):
    fname = "-".join([str(year), month, glb.base_tracks_fname])
    fqpath = os.path.join(glb.tracks_path, str(year))
    fqname = os.path.join(fqpath, fname)
    return fqname
