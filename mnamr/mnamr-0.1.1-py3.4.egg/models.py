import os
import re

from .exceptions import UnparseableDirname

class KnownMovieDir:
    """
    A known movie directory which follows the following naming convention:

        Title (Year) imdb:<iMDB-ID>

    The known
    """
    def __init__(self, title, year, imdb_id):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id

    def get_dirname(self):
        return '%s (%s) imdb:%s' % (self.title, self.year, self.imdb_id)

    @staticmethod
    def parse_dirname(dirname):
        """
        Try to parse the given dir name to a known movie dir. Returns a tuple of: (title, year, imdb id)
        """
        match = re.search(r'(.*?) \((\d{4})\) imdb:(tt\d{7})', dirname)
        if match is None:
            raise UnparseableDirname
        return match.group(1), match.group(2), match.group(3)

class UnknownMovieDir:
    """
    A movie dir with unknown contents. Contains methods for parsing the dir name into a searchable movie title.
    """

    def __init__(self, path):
        self.path = path
        self.title, self.year = self._parse_dirname()

    def _parse_dirname(self):
        """
        Tries to parse a typical downloaded movie dir name into a movie title and year
        """
        KEYWORDS = [
            'dvd image',
            'dvdrip',
            'dvdr',
            'brrip',
            'bluray',
            'divx',
            'xvid',
            'x264',
            'h264',
            'ac3',
            '720p',
            '720i',
            '1080p',
            '1080i',
        ]
        parsed_name = self.get_dirname()

        # Remove any known quality classifiers
        for word in KEYWORDS:
            parsed_name = re.sub(word, '', parsed_name, flags=re.IGNORECASE)

        # Replace dots with spaces
        parsed_name = re.sub(r'\.', ' ', parsed_name)

        # Remove trailing group name
        parsed_name = re.sub(r'-[a-z]+$', '', parsed_name, flags=re.IGNORECASE)

        # Try to find a year for the movie, and if found, remove it from the name
        year = None
        year_match = re.search(r'\d{4}', parsed_name)
        if year_match:
            year = year_match.group()
            parsed_name = re.sub(year, '', parsed_name)

        # Remove any empty bracket groups ([{ (with an optional space)
        parsed_name = re.sub(r'[\(\[\{]\ ?[\)\]\}]', '', parsed_name)

        # Remove *any* brackets, very rarely part of any movie name []
        parsed_name = re.sub(r'\[.*?\]', '', parsed_name)

        # Remove duplicate spaces
        parsed_name = ' '.join(parsed_name.split())

        return parsed_name.strip(), year

    def get_dirname(self):
        return os.path.basename(self.path)

    def get_parsed_title(self):
        if self.year is None:
            return self.title
        else:
            return '%s (%s)' % (self.title, self.year)

    def rename_to(self, new_name):
        new_path = os.path.join(os.path.dirname(self.path), new_name)
        if os.path.exists(new_path):
            print()
            print("Cannot rename: Directory '%s' already exists, do you have a duplicate of the same movie?" % new_path)
            print("Aborting.")
            exit()
        os.rename(self.path, new_path)
