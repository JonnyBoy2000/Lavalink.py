def format_time(time):
    """ Formats the given time into HH:MM:SS. """
    hours, remainder = divmod(time / 1000, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return '%02dh %02dm %02ds' % (hours, minutes, seconds)
    if minutes:
        return '%02dm %02ds' % (minutes, seconds)
    if seconds:
        return '%02ds' % (seconds)
