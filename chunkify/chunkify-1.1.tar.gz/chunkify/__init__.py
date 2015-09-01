from itertools import islice


class ChunkingError(Exception):
    pass


def chunkify(things, this_chunk, chunks):
    if this_chunk > chunks:
        raise ChunkingError("this_chunk is greater than total chunks")

    size = len(things) / chunks
    big_chunks = len(things) % chunks
    start = size * (this_chunk-1)
    if big_chunks:
        start += (min(big_chunks, this_chunk)-1)
        if this_chunk <= big_chunks:
            size += 1
        elif this_chunk == big_chunks+1:
            start += 1
        else:
            start += this_chunk-big_chunks-1

    end = start + size
    try:
        return things[start:end]
    except TypeError:
        return islice(things, start, end)
