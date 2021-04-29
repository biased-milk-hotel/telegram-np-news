def format_twitter(data):
    url = f"https://twitter.com/twitter/statuses/{data.id_str}"
    images = []
    for media in data.entities.get("media", [{}]):
        if media.get("type", None) == "photo":
            images.append(media["media_url"])

    return {
        "post_id": data.id,
        "user_id": data.user.id,
        "text": data.full_text,
        "time": data.created_at,
        "images": images,
        "post_url": url
    }


def _wrapper(api, identifier, name):

    tweets = api.user_timeline(
        screen_name="RONBupdates",
        count=10,
        include_rts=False,
        tweet_mode='extended'
    )
    cleaned_tweets = [x for x in map(format_twitter, tweets)]
    return [dict(i, source_name=name, source_identifier=identifier) for i in cleaned_tweets]


# Get tweets of "Routine of Nepal Banda"

def get_ronb(api):
    return _wrapper(api, "RONBupdates", "RONB")
