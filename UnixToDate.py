from datetime import datetime

def convert_unix(unix):
    format = '%d/%m/%Y'
    date = datetime.utcfromtimestamp(unix).strftime(format)
    return date