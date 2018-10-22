import os
import pathlib
import string

import requests
import tqdm
import bs4

from .user_agent import get_user_agent

base_url = "https://www.basketball-reference.com/players/%s/"
out_dir = "data/players"


def download_player_indices():
    """
    Download index of players
    """
    # TODO: Have some sensible way of updating user agent
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

    for c in tqdm.tqdm(string.ascii_lowercase):
        url = base_url % c
        with open(os.path.join(out_dir, "%s.html" % c), "w") as file:
            res = requests.get(
                url,
                headers={
                    "User-Agent": get_user_agent()
                }
            )
            file.write(res.content.decode("utf-8"))


def parse_player_indices():
    """
    Parse index of players
    """

    player_urls = []
    for c in tqdm.tqdm(string.ascii_lowercase):
        path = os.path.join(out_dir, "%s.html" % c)
        with open(path, "r") as file:
            try:
                raw = file.read()
                soup = bs4.BeautifulSoup(raw, "lxml")
                rows = soup.findAll("tbody")[0].findAll("tr")
                for row in rows:
                    link = row.findAll("a", href=True)[0]
                    player_urls.append(link["href"])

            # Because there's the letter X...
            except Exception as e:
                pass
    print(len(player_urls))

    with open(os.path.join(out_dir, "player_urls.txt"), "w") as file:
        file.write("\n".join(player_urls))


def download_player_pages():
    # TODO: respect robots.txt crawl-delay 3
    # TODO: save actual HTML pages
    pass


def parse_player_pages():
    # TODO: Remove thead tr
    # TODO: Refactor grabbing first link in first col of first table
    path = "tmp/player.html"
    with open(path, "r") as file:
        raw = file.read()
        soup = bs4.BeautifulSoup(raw, "lxml")

        # First table is the Per Game data
        rows = soup.findAll("tbody")[0].findAll("tr")
        for row in rows:
            link = row.findAll("a", href=True)[0]
            print(link["href"])


def parse_player_year():
    # TODO: Remove thead tr
    pass


__all__ = [
    "download_player_indices",
    "parse_player_indices",
    "download_player_pages",
    "parse_player_pages",
    "parse_player_year"
]
