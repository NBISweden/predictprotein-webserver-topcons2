import time
def timeit(method):# {{{
    """Decorator to time a method
inspired by https://www.zopyx.com/andreas-jung/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('Runtime for %r:  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed
# }}}
