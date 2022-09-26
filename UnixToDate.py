from datetime import datetime

def convert_unix(unix):
    format = '%Y-%m-%d %H:%M'
    date = datetime.utcfromtimestamp(unix).strftime(format)
    return date