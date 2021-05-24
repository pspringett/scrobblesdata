import os
import sys
import csv

# import json
from optparse import OptionParser

# import scrobbleswrite
import scrobblesread
import charts
import datetime as dt

import pprint


def main():
    global options, fqpath

    _main_cmd_line()

    if options.artists:
        key = "artist"
    if options.albums:
        key = "album"
    if options.tracks:
        key = "track"

    tracks = scrobblesread.get_all()
    chart = charts.make_chart(tracks, key)
    charts.print_chart(chart)


def _main_cmd_line():
    """
    Interprets the command line parameters and stores them in global variables.
    In general these should not be changed by any part of this script.
    """
    global options, fqpath

    # -------------------------------------------------------------------------
    # Create the options parser.
    # -------------------------------------------------------------------------
    usage = "Usage: %prog [options]"

    epilog = "Shows summary scrobbles for the period selected. "
    epilog += "When no time parameter is selected it just displays counts for all time. "
    epilog += "fqpath is the path to the data files (inclduing exported_tracks.txt). "
    parser = OptionParser(usage, epilog=epilog)

    diff_help_text = "Use month (m), year (y) or all (a) to show the"
    diff_help_text += " difference over this period"

    parser.add_option("-y", "--year", type="int", default=0)
    parser.add_option("-m", "--month", type="int", default=0)
    parser.add_option("-d", "--day", type="int", default=0)
    parser.add_option("-a", "--artists", action="store_true", default=False)
    parser.add_option("-c", "--albums", action="store_true", default=False)
    parser.add_option("-t", "--tracks", action="store_true", default=False)
    parser.add_option("-s", "--summary", action="store_true", default=False)
    parser.add_option("-n", "--name", type="str", default=None)
    parser.add_option("-f", "--difference", type="str", default=None, help=diff_help_text)
    parser.add_option("-l", "--least", action="store_true", default=False)
    parser.add_option("-i", "--history", action="store_true", default=False)
    parser.add_option("-o", "--owned", action="store_true", default=False)
    (options, args) = parser.parse_args()

    # -------------------------------------------------------------------------
    # Optional parameters.
    # -------------------------------------------------------------------------
    today = dt.date.today()

    if options.month > 12:
        print("Invalid month")
        sys.exit(1)

    if options.day > 31:
        print("Invalid day")
        sys.exit(1)

    if options.difference is not None:
        d = options.difference
        if len(d) == 1:
            if (d != "m") and (d != "y") and (d != "a"):
                print("Invalid difference (f) option - %s" % diff_help_text)
                sys.exit(1)

        else:
            if (d != "month") and (d != "year") and (d != "all"):
                print("Invalid difference (f) option - %s" % diff_help_text)
                sys.exit(1)

        if options.day == 0:
            print("Cannot use difference (f) option without day option.")
            sys.exit(1)

        if options.difference == "m":
            options.difference = "month"
        if options.difference == "y":
            options.difference = "year"
        if options.difference == "a":
            options.difference = "all"

    if options.history:
        if options.name == None:
            print("--history (-h) options must also specify a name")
            sys.exit()

    if options.owned:
        return

    # -------------------------------------------------------------------------
    # Year, month day - Parameter  present.
    #   0    0    0    Display all time (no filter)
    #   0    0    1    This year, this month, specified day (day filter)
    #   0    1    0    This year specified month (month filter)
    #   0    1    1    This year, specified month, specified day (day filter)
    #   1    0    0    Specified year (year filter)
    #   1    0    1    Specified year, this month, specified day (not useful)
    #   1    1    0    Specified year, specified month (month filter)
    #   1    1    1    Specified year, specified month, specified day (day filter)
    #
    # This block fixes up any unspecified time period to todays year, or month
    # unless none are specified, which means all time.
    # -------------------------------------------------------------------------
    if options.year == 0:
        if options.month == 0:
            if options.day == 0:
                print("All time")
            else:
                print(
                    "This year (%d), this month (%d), specified day (%d)"
                    % (today.year, today.month, options.day)
                )
                options.year = today.year
                options.month = today.month
        else:
            if options.day == 0:
                print("This year (%d), specified month (%d)" % (today.year, options.month))
                options.year = today.year
            else:
                print(
                    "This year (%d), specified month (%d), specified day (%d)"
                    % (today.year, options.month, options.day)
                )
                options.year = today.year
    else:
        if options.month == 0:
            if options.day == 0:
                print("Specified year (%d)" % (options.year))
            else:
                print(
                    "Specified year (%d), this month (%d), specified day (%d)"
                    % (options.year, today.month, options.day)
                )
                print("Not a useful combination")
                sys.exit()

        else:
            if options.day == 0:
                print("Specified year (%d), specified month (%d)" % (options.year, options.month))
            else:
                print(
                    "Specified year (%d), specified month (%d) specified day (%d)"
                    % (options.year, options.month, options.day)
                )

    # If none of the artist, albums or tracks are specified, default to
    # artists.
    if not options.artists and not options.albums and not options.tracks:
        options.artists = True
    return


if __name__ == "__main__":
    # print(sys.version)
    # print(sys, sys.executable)
    main()
