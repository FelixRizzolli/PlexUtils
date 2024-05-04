import os

from test_data import test_movie_files


current_script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(current_script_dir, '../../data')
movies_dir = os.path.join(data_dir, 'movies')


def delete_directory(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            delete_directory(item_path)
    os.rmdir(dir_path)


def create_movie_files():
    movie_files = test_movie_files

    # clear data
    if os.path.isdir(movies_dir):
        delete_directory(movies_dir)

    # create data
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    if not os.path.isdir(movies_dir):
        os.mkdir(movies_dir)

    for movie_file in movie_files:
        open(os.path.join(movies_dir, movie_file), 'a').close()
