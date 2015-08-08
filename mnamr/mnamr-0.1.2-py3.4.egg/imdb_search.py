from requests.exceptions import HTTPError
import imdbpie

from .paginator import TitlePaginator

imdb = imdbpie.Imdb()

def search_for_imdb_title(unknown_movie):
    """
    Find the iMDB title for an unknown movie dir. The iMDB title returned is an imdbpie.objects.Title object.
    """
    parsed_title = unknown_movie.get_parsed_title()
    custom_title = None
    imdb_title = None

    print()
    print(" - Directory name:  %s" % unknown_movie.get_dirname())
    print("   Parsed title:    %s" % parsed_title)
    titles = TitlePaginator(imdb.search_for_title(parsed_title))
    print("   %s search results" % len(titles))

    while imdb_title is None:
        print()
        for i, title in titles.current_titles():
            print("   %s. (%s) %s" % (
                i + 1,
                title['year'],
                title['title'],
            ))

        print()
        print("   i) Enter iMDB ID")
        if custom_title is None:
            print("   s) Search for custom title")
        else:
            print("   r) Reset title to %s (current title: %s)" % (parsed_title, custom_title))
        print("   d) More details for a single search result")
        print("   p) Prev %s" % TitlePaginator.BULK_COUNT)
        print("   n) Next %s" % TitlePaginator.BULK_COUNT)
        print()

        choice = input("   Choose: ").lower()

        if choice == 'i':
            # Let user enter iMDB ID manually
            imdb_id = input("   Enter iMDB ID: ")
            try:
                imdb_title = imdb.get_title_by_id(imdb_id)

                # Found title, confirm
                print()
                print("   %s (%s)" % (imdb_title.title, imdb_title.year))
                print("   %s" % (imdb_title.poster_url))
                print("   http://www.imdb.com/title/%s/" % imdb_title.imdb_id)
                if input("   OK? (y/n) ").lower() != 'y':
                    imdb_title = None
            except HTTPError:
                print("   Couldn't find that, check http://www.imdb.com/title/%s/" % imdb_id)

        elif choice == 's':
            # Let user search for a custom title
            custom_title = input("   Enter movie title: ")
            titles = TitlePaginator(imdb.search_for_title(custom_title))
            print("   %s results for '%s'" % (len(titles), custom_title))

        elif choice == 'r':
            # Reset to default title
            custom_title = None
            titles = TitlePaginator(imdb.search_for_title(parsed_title))
            print("   %s results for '%s'" % (len(titles), parsed_title))

        elif choice == 'd':
            # Display details for the current bulk
            index = input("   Enter index: ")
            try:
                title_data = imdb.get_title_by_id(titles[int(index) - 1]['imdb_id'])
                print()
                print("   %s (%s) %s/10: %s" % (
                    title_data.title,
                    title_data.year,
                    title_data.rating,
                    title_data.tagline,
                ))
                print("   %s" % (title_data.plot_outline))
                print("   %s" % (', '.join([c.name for c in title_data.cast_summary])))
                print("   http://www.imdb.com/title/%s/" % (title_data.imdb_id))
            except IndexError:
                print("   There are only %s search results, can't pick index %s" % (len(titles), index))
            except ValueError:
                print("   Invalid index")

        elif choice == 'p':
            titles.back()

        elif choice == 'n':
            titles.forwards()

        else:
            # Not a recognized command, try to parse as a chosen search result index
            try:
                title_index = int(choice) - 1
                if title_index >= len(titles):
                    print("   There are only %s search results, can't pick index %s" % (len(titles), title_index))
                else:
                    imdb_title = imdb.get_title_by_id(titles[title_index]['imdb_id'])
            except ValueError:
                print("   Unknown command '%s'" % choice)
    return imdb_title
