import os
import json
import pprint
import re

fixup_path = os.path.join("h:\\", "dev", "scrobbles", "data", "filters")
small_words = ["a", "an", "and", "in", "for", "is", "it", "of", "on", "the", "that", "to"]


class Fixup:
    def __init__(self):

        self.artists = self.read_artist(fixup_path)
        self.albums = self.read_album(fixup_path)

        # This maps a variant album name, to a new album, it is a simple dictionary.
        self.variants = self.read_variants(fixup_path)

        # This maps an album name with a corrected artist.
        self.artists = self.read_artist(fixup_path)

        # This maps an album name with a corrected artist.
        self.artist_from_album = self.read_artist_from_album(fixup_path)
        fqpath = os.path.join(fixup_path, "fixup.json")
        with open(fqpath, "r") as fp:
            fixup_artist_from_album = json.load(fp)

        self.artist_from_album = {}
        for item in fixup_artist_from_album:
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

        new_artist = self.fixup_artist(new_artist)
        new_artist = self.fixup_artist_by_album(new_album, new_artist)

        return (new_artist, new_album)

    def read_album(self, ficup_path):
        # The fixup albums needs converting to a dictionary maping old album to new album.
        new_albums = {}
        fqname = os.path.join(fixup_path, "fixup_albums.json")
        with open(fqname, "r") as fp:
            fixup_album = json.load(fp)

        self.albums = {}
        for item in fixup_album:
            m_album = item["m_album"].lower()
            new_albums[m_album] = item["n_album"]

        return new_albums

    def read_artist(self, fixup_path):
        # The fixup artists needs converting to a dictionary mapping old to new artist.
        new_artists = {}
        fqpath = os.path.join(fixup_path, "fixup_artists.json")

        with open(fqpath, "r") as fp:
            fixup_artist = json.load(fp)

        self.artists = {}
        for item in fixup_artist:
            m_artist = item["m_artist"].lower()
            new_artists[m_artist] = item["n_artist"]

        return new_artists

    def read_variants(self, fixup_path):
        """
        This is a dictionary. Each key must be converted to lower case
        """
        fqname = os.path.join(fixup_path, "variant_albums.json")
        new_variants = {}
        with open(fqname, "r") as fp:
            variants = json.load(fp)

        for key, value in variants.items():
            new_variants[key.lower()] = value

        return new_variants

    def read_artist_from_album(self, fixup_path):

        new_artist_from_album = {}

        fqname = os.path.join(fixup_path, "fixup.json")

        with open(fqname, "r") as fp:
            fixup_artist_from_album = json.load(fp)

        for item in fixup_artist_from_album:
            m_album = item["m_album"].lower()
            new_artist_from_album[m_album] = item["n_artist"]

        return new_artist_from_album

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
                track = track_info["m_track"].lower()
                new_album = track_info["n_album"]
                new_track_info[track] = new_album
                break
            new_boxset[boxset_title.lower()] = new_track_info
            break

        return new_boxset

    def fixup_artist(self, artist):

        try:
            return self.artists[artist.lower()]
        except KeyError:
            return artist

        return artist

    def fixup_album(self, album):
        try:
            return self.albums[album.lower()]
        except KeyError:
            return album

        return album

    def fixup_variants(self, album):
        try:
            return self.variants[album.lower()]
        except KeyError:
            return album

        return album

    def fixup_artist_by_album(self, album, artist):
        try:
            return self.artist_from_album[album.lower()]
        except KeyError:
            return artist

        return artist

    def fixup_boxset(self, artist, album, track):

        try:
            album_by_track = self.boxset[album.lower()]
            try:
                return album_by_track[track.lower()]
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

        new_sentance.append(words[0].title())
        for word in words[1:]:
            word = word.lower()
            if word in small_words:
                new_sentance.append(word)
            else:
                new_sentance.append(word.capitalize())

        return " ".join(new_sentance)

    def titlecase(self, s):
        return re.sub(r"[A-Za-z']+('[A-Za-z']+)?", lambda mo: mo.group(0).capitalize(), s)


#   // {
#   //   "m_track": "Understanding What Black Is",
#   //   "n_track": "Understand What Black Is"
#   // },
