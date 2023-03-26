# Taken from: https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python

def hms_to_seconds(timestr: str) -> float:
    """Get seconds from time.

    :param timestr: hh:mm:ss.xxx string or mm:s.xxx or simply s.xxx where xxx is the fraction of seconds
    :returns: time in float seconds
    """
    seconds = 0.
    for part in timestr.split(':'):
        seconds = seconds*60. + float(part)
    return seconds
