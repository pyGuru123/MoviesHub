import json
from app.utils import fetch_posts, random_post, aeshash

def get_movie_url(name, url):
    try:
        fetch_posts()
        f = open("posts.json", "r")
        json_data = json.load(f)
        json_data = json.loads(json_data)
        content = json_data["feed"]["entry"]

        random_post_link = random_post(content)
        shorten_link = aeshash(random_post_link, name, url)

        return shorten_link
            
    except Exception as e:
        print(e)