#!/usr/bin/env python

import requests
from urllib.parse import urlsplit

def main(url):
    comic_id = url.split("/")[-1]
    res_toc = requests.get(f"https://comic.pixiv.net/api/app/episodes/{comic_id}/read", headers={
        "X-Requested-With": "pixivcomic",
        "X-Client-Time": "2020-07-09T14:50:07-05:00",
        "X-Client-Hash": "dac19c3c6a4e2b7740600e8b5db11908",
        "Host": "comic.pixiv.net",
    })
    assert res_toc.ok
    data = res_toc.json()["data"]["reading_episode"]
    print(f"Downloading {data['work_title']} {data['title']}")
    images = [page["url"] for page in data["pages"]]
    for url_image in images:
        res_im = requests.get(url_image, headers={
            "Referer": url,
        })
        assert res_im.ok
        filename = urlsplit(url_image).path.split("/")[-1]
        print(f"[ OK ] {filename}")
        with open(filename, "wb") as f:
            f.write(res_im.content)

if __name__ == "__main__":
    import sys
    try:
        main(sys.argv[1])
    except IndexError:
        print(f"Usage: {sys.argv[0]} https://comic.pixiv.net/viewer/stories/12345", file=sys.stderr)
