
def intersperse(iterable, delimiter):
    # http://stackoverflow.com/a/5656097/613023
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x
