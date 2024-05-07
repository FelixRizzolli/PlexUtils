import os
import json

def generate_tvshow_files(data_dir: str, scripts_data_dir: str) -> None:
    tvshows_dir = os.path.join(data_dir, 'tvshows')

    # Open the JSON file
    with open(os.path.join(scripts_data_dir, 'tvshow_files.json'), 'r', encoding='utf-8') as f:
        # Load the JSON data into a Python dictionary
        tvshow_directories = json.load(f)['movie_files']

    # create data
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if not os.path.isdir(tvshows_dir):
        os.mkdir(tvshows_dir)

    # create tvshow directories
    for tvshow in tvshow_directories:
        tvshow_dirname: str = tvshow["dirname"]
        tvshow_dir: str = os.path.join(tvshows_dir, tvshow_dirname)
        if not os.path.isdir(tvshow_dir):
            os.mkdir(tvshow_dir)

        for season in tvshow["seasons"]:
            season_dirname: str = season["dirname"]
            season_dir: str = os.path.join(tvshow_dir, season_dirname)
            if not os.path.isdir(season_dir):
                os.mkdir(season_dir)

            for episode in season["episodes"]:
                episode_dir: str = os.path.join(season_dir, episode)
                with open(episode_dir, 'a', encoding='utf-8'):
                    pass
