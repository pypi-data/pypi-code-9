from eulfedora.server import Repository
repo = Repository('https://libfedqa1.library.emory.edu:8443/fedora/')
print repo.get_next_pid()