"""
Reads mytracks and generates mycharts.  Overwriting files.
"""

import scrobblesglobal as glb
import scrobblesread
import scrobblescharts as charts
import os


def update_all():

    all_tracks = []

    years = os.listdir(glb.tracks_path)
    years.sort()
    years = [x for x in years if glb.valid_year(x)]

    for year in years:

        year_list = []
        for month in glb.months_as_string:
            print("....processing {}:{}".format(year, month))
            all_tracks, year_list, month_list = scrobblesread.get_month(
                year, month, all_tracks, year_list
            )

            if len(month_list) > 1:
                fqpath = os.path.join(glb.mycharts_path, year, month)
                write_charts(month_list, fqpath)

        fname = year
        fqname = os.path.join(glb.mycharts_path, year)
        write_charts(year_list, fqpath)

    fqpath = os.path.join(glb.mycharts_path)
    write_charts(all_tracks, fqpath)


def write_charts(tracks, fqpath):

    for key in glb.keys:

        fname = glb.chart_fnames[key]
        fqname = os.path.join(fqpath, fname)

        if not os.path.exists(fqpath):
            os.makedirs(fqpath)

        chart = charts.make_chart(tracks, key)

        with open(fqname, "w", encoding="utf8") as fp:
            charts.write_chart(fp, chart)


if __name__ == "__main__":

    update_all()
