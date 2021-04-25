from facebook_scraper import get_posts


def format_facebook(data):
    filtered = {key: data[key] for key in data.keys()
                & {'post_id', 'user_id', 'text', 'time', 'image', 'post_url'}}
    return filtered


def _wrapper(identifier, name):
    posts = map(format_facebook, get_posts(identifier, pages=4))
    return [dict(i, source_name=name, source_identifier=identifier) for i in posts]


# Get posts of "Routine of Nepal Banda"

def get_ronb():
    return _wrapper("213613352004799", "RONB")
