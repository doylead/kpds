import json
from isodate import parse_duration
from datetime import datetime, timezone

def unpack_video_json(
        json_object, # The object to be "unpacked" - a raw JSON response
        cat1, # The first-level category, e.g. "Duration"
        cat2=None, # If categories are tiered, second tier
        cat3=None, # If categories are tiered, third tier
        part='snippet' # Which part of the YouTube API call we're scanning
        ):

    results = len(json_object['items'])

    ## Extract information, using tiers if necessary to access nested objects
    if cat3 is not None:
        l = [json_object['items'][i][part][cat1][cat2][cat3] for i in range(results)]
    elif cat2 is not None:
        l = [json_object['items'][i][part][cat1][cat2] for i in range(results)]
    else:
        l = [json_object['items'][i][part][cat1] for i in range(results)]

    ## Process if necessary
    # Convert duration to seconds
    if cat1 == 'duration':
        l = [int(parse_duration(l[i]).total_seconds()) for i in range(results)]

    # For some reason the API returns the caption value as a string reading either 
    # "true" or "false."  This returns python-native bolean instead
    if cat1 == 'caption':
        l = [json.loads(l[i]) for i in range(results)]

    # Converts timezone to UTC
    if cat1 == 'publishedAt':
        l = [datetime.strptime(l[i], "%Y-%m-%dT%H:%M:%S.%fZ") for i in range(results)]
        l = [l[i].astimezone(timezone.utc) for i in range(results)]

    return l

