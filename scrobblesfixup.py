import os
import json
import pprint
import re

fixup_path = os.path.join("h:\\", "dev", "scrobbles", "data", "filters")
small_words = ["a", "an", "and", "in", "for", "is", "it", "of", "on", "the", "that", "to"]

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
}


class Fixup:
    def __init__(self):

        self.read_artist()
        self.read_album()

        # This maps a variant album name, to a new album, it is a simple dictionary.
        fqpath = os.path.join(fixup_path, "variant_albums.json")
        with open(fqpath, "r") as fp:
            self.variants = json.load(fp)

        # This maps an album name with a corrected artist.
        fqpath = os.path.join(fixup_path, "fixup_artist.json")
        with open(fqpath, "r") as fp:
            fixup_artist = json.load(fp)

        # This maps an album name with a corrected artist.
        fqpath = os.path.join(fixup_path, "fixup.json")
        with open(fqpath, "r") as fp:
            fixup_artist = json.load(fp)

        self.artist_from_album = {}
        for item in fixup_artist[:2]:
            self.artist_from_album[item["m_album"]] = item["n_artist"]

        self.boxset = self.read_boxset(fixup_path)

    def fixup_tracks(self, tracks):
        new_tracks = []
        for t in tracks:

            datetime = t[0]
            artist = t[1]
            album = t[2]
            title = t[3]

            artist, album = self.fixup_scrobble_info(artist, album, title)
            new_tracks.append([datetime, artist, album, title])
        return new_tracks

    def fixup_scrobble_info(self, artist, album, track):

        new_album = self.titlecase(album)
        new_artist = self.proper(artist)

        new_album = self.fixup_boxset(new_artist, new_album, track)
        new_album = self.fixup_album(new_album)
        new_album = self.fixup_variants(new_album)

        new_artist = self.fixup_artist(artist)
        new_artist = self.fixup_artist_by_album(new_album, new_artist)

        return (new_artist, new_album)

    def read_artist(self):
        # The fixup artists needs converting to a dictionary mapping old to new artist.
        fqpath = os.path.join(fixup_path, "fixup_artists.json")
        with open(fqpath, "r") as fp:
            fixup_artist = json.load(fp)

        self.artists = {}
        for item in fixup_artist:
            self.artists[item["m_artist"]] = item["n_artist"]

    def fixup_artist(self, artist):

        try:
            return self.artists[artist]
        except KeyError:
            return artist

        return artist

    def read_album(self):
        # The fixup albums needs converting to a dictionary maping old album to new album.
        fqpath = os.path.join(fixup_path, "fixup_albums.json")
        with open(fqpath, "r") as fp:
            fixup_album = json.load(fp)

        self.albums = {}
        for item in fixup_album:
            self.albums[item["m_album"]] = item["n_album"]

    def fixup_album(self, album):
        try:
            return self.albums[album]
        except KeyError:
            return album

        return album

    def fixup_variants(self, album):
        try:
            return self.variants[album]
        except KeyError:
            return album

        return album

    def fixup_artist_by_album(self, album, artist):
        try:
            return self.artist_from_album[album]
        except KeyError:
            return artist

        return artist

    def read_boxset(self, fqpath):
        # This maps an album name which is a box-set, and based on the track maps it to an actual album.
        # It contains a dictionary based on the box set name, and then a dictionary, mapping track to album name.
        fqname = os.path.join(fqpath, "fixup_boxsets.json")
        with open(fqname, "r") as fp:
            raw_boxset = json.load(fp)

        new_boxset = {}
        for boxset_title, tracks in raw_boxset.items():

            new_track_info = {}
            for track_info in tracks:
                track = track_info["m_track"]
                new_album = track_info["n_album"]
                new_track_info[track] = new_album
                break
            new_boxset[boxset_title] = new_track_info
            break

        return new_boxset

    def fixup_boxset(self, artist, album, track):

        try:
            album_by_track = self.boxset[album]
            try:
                return album_by_track[track]
            except KeyError:
                return album
        except KeyError:
            return album

    def proper(self, sentance):
        """
        Capitalises all the non-small words in a string.
        """
        new_sentance = []

        words = sentance.split()

        for word in words:
            word = word.lower()
            if word in small_words:
                new_sentance.append(word)
            else:
                new_sentance.append(word.capitalize())

        return " ".join(new_sentance)

    def titlecase(self, s):
        return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
