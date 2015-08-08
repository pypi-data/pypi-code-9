import argparse
import os

from .exceptions import UnparseableDirname
from .imdb_search import search_for_imdb_title
from .models import KnownMovieDir, UnknownMovieDir

def main():
    parser = argparse.ArgumentParser(description='Rename movie folders based on iMDB data.')
    parser.add_argument('dir', type=str, nargs='?', help='optional relative path from the current dir')
    args = parser.parse_args()
    current_dir = os.getcwd()
    if args.dir is not None:
        current_dir = os.path.join(current_dir, args.dir)
        if not os.path.exists(current_dir):
            print("Directory '%s' does not exist." % current_dir)
            exit()
    print("Looking for movie directories in %s..." % current_dir)

    movie_dirs = filter(os.path.isdir, [os.path.join(current_dir, f) for f in os.listdir(current_dir)])
    known_movies = []
    unknown_movies = []
    for dirname in movie_dirs:
        try:
            title, year, imdb_id = KnownMovieDir.parse_dirname(dirname)
            known_movies.append(KnownMovieDir(title, year, imdb_id))
        except UnparseableDirname:
            unknown_movies.append(UnknownMovieDir(dirname))

    print("%s known movies, %s unknown movies." % (len(known_movies), len(unknown_movies)))
    if len(unknown_movies) == 0:
        exit()

    print("Looking up and renaming unknown movie directories...")
    for unknown_movie in unknown_movies:
        imdb_title = search_for_imdb_title(unknown_movie)
        known_movie = KnownMovieDir(title=imdb_title.title, year=imdb_title.year, imdb_id=imdb_title.imdb_id)
        unknown_movie.rename_to(known_movie.get_dirname())
        print()
        print("   Renamed directory to: %s" % known_movie.get_dirname())
