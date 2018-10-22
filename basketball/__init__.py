import os
import pathlib
import string

import requests
import tqdm

base_url = "https://www.basketball-reference.com/players/%s/"

# Download player indices
def download_player_indices():
    out_dir = "data/players"
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)

    for c in tqdm.tqdm(string.ascii_lowercase):
        url = base_url % c
        with open(os.path.join(out_dir, "%s.html" % c), "w") as file:
            file.write(requests.get(url).content.decode("utf-8"))


