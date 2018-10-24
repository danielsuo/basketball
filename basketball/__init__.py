import os
import pathlib
import random
import string
import time
import urllib
from datetime import date

import requests
import tqdm

import bs4
import pandas

from .user_agent import get_user_agent

base_url = "https://www.basketball-reference.com"
update_url = urllib.parse.urljoin(base_url, "boxscores/index.fcgi")
out_dir = "data/players"

# TODO: Write update scripts
# TODO: Investigate stat.nba.com advanced stats
# TODO: Parallelize downloading and parsing
# TODO: Make these functions not so incredibly terribad
# TODO: Aggregate stats together from different tables
# TODO: Stop being lazy and save intermediate files in a reasonable place
# TODO: Manage output directories better
# TODO: Create database and insert (e.g., tinydb)


def download_boxscores(
    year=date.today().year, month=date.today().month, day=date.today().day
):
    params = {"year": year, "month": month, "day": day}

    res = requests.get(update_url, params=params)

    data = res.content.decode("utf-8")
    soup = bs4.BeautifulSoup(data, "lxml")

    urls = []
    for link in soup.findAll("a", text="Box Score", href=True):
        urls.append(link["href"])

    urls = [os.path.join(base_url, url.lstrip(os.path.sep)) for url in urls]
    print(urls)

    download_urls(urls, out_dir="data/boxscores", sleep=False)


def parse_boxscores(
    year=date.today().year, month=date.today().month, day=date.today().day
):
    stamp = "{}{}{}".format(year, month, day)

    tables = []
    for path in os.listdir("data/boxscores"):
        if stamp not in path:
            continue
        with open(os.path.join("data/boxscores", path), "rb") as file:
            data = file.read().decode("utf-8")
            # soup = bs4.BeautifulSoup(data, "lxml")
            # soup.findAll
            # tables = pandas.read_html(data)
            tables.extend(pandas.read_html(data))

    return tables


def download_urls(urls, out_dir=out_dir, sleep=True):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for url in tqdm.tqdm(urls):
        path = urllib.parse.urlparse(url).path.lstrip(os.path.sep)
        path = path.replace("/", "-")
        with open(os.path.join(out_dir, path), "wb") as file:
            res = requests.get(url, headers={"User-Agent": get_user_agent()})
            try:
                file.write(res.content)
            except Exception as e:
                print("Failed at {} with {}".format(url))

        # Sleep for a random time
        if sleep:
            time.sleep(random.randint(3, 5))


def download_urls_from_list(url_list):
    with open(os.path.join(out_dir, url_list), "r") as file:
        urls = file.read().split()
        urls = [os.path.join(base_url, url.lstrip(os.path.sep)) for url in urls]
        download_urls(urls)


def parse_pages(pages, out_dir=out_dir):
    # TODO: Remove thead tr
    urls = []
    for page in tqdm.tqdm(pages):
        path = os.path.join(out_dir, page.replace("/", "-"))
        with open(path, "r") as file:
            try:
                raw = file.read()
                soup = bs4.BeautifulSoup(raw, "lxml")
                rows = soup.findAll("tbody")[0].findAll("tr")
                for row in rows:
                    link = row.findAll("a", href=True)[0]
                    link = link["href"].replace(base_url, "")
                    urls.append(link["href"])
            except Exception as e:
                pass

    return urls


def download_player_indices():
    """
    Download index of players
    """
    # TODO: Have some sensible way of updating user agent
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    urls = [os.path.join(base_url, "players", c) for c in string.ascii_lowercase]
    download_urls(urls, sleep=False)


def parse_player_indices():
    """
    Parse index of players
    """
    player_urls = parse_pages(list(string.ascii_lowercase))
    with open(os.path.join(out_dir, "player_urls.txt"), "w") as file:
        file.write("\n".join(player_urls))


def download_player_pages():
    download_urls_from_list("player_urls.txt")


def parse_player_pages():
    with open(os.path.join(out_dir, "player_urls.txt"), "r") as file:
        player_urls = file.read().split()
        pages = [os.path.basename(url) for url in player_urls]
        years = parse_pages(pages)

    with open(os.path.join(out_dir, "player_years.txt"), "w") as file:
        file.write("\n".join(years))

    print(len(years))


def download_player_years():
    download_urls_from_list("player_years.txt")


def parse_player_years():
    path = "tmp/year.html"
    with open(path, "r") as file:
        raw = file.read().split("\n")

        # Hack city, hack hack city
        raw = [line for line in raw if line != "<!--"]
        raw = [line for line in raw if line != "-->"]
        raw = "\n".join(raw)
        soup = bs4.BeautifulSoup(raw, "lxml")
        d = pandas.read_html(str(soup))
        print(d[0])
        print(len(d))
        # tables = soup.findAll("tbody")
        # print(type(tables[1]))
        # print(type(str(tables[1])))

        # for table in tables:
        # data = pandas.read_html(str(table))
        # print(data)


__all__ = [
    "download_urls",
    "download_urls_from_list",
    "parse_pages",
    "download_player_indices",
    "parse_player_indices",
    "download_player_pages",
    "parse_player_pages",
    "download_player_years",
    "parse_player_years",
    "download_boxscores",
    "parse_boxscores",
]
