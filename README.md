# Setup Project
## install with poetry 
- [Poetry installation documentation](https://python-poetry.org/docs/#installation)
- change to the project directory
- use `poetry install` to install the dependencies
- use `poetry run python plexutils/main.py` to run the script


## config.yaml
- rename the `example-config.yaml` to `config.yaml`
- language
  - example `language: de_DE` for german
  - supported languages:
    - `de_DE` german
    - `en_US` english
- movies-dir
  - example `movies-dir: /Users/felixrizzolli/PycharmProjects/PlexUtils/data/movies`
  - the path where your movies are located
- tvshows-dir
  - example `movies-dir: /Users/felixrizzolli/PycharmProjects/PlexUtils/data/tvshows`
  - the path where your tvshows are located
- tvdb-key and tvdb-pin
  - example `tvdb-key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
  - example `tvdb-pin: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  - you net to get them from [thetvdb.com](https://thetvdb.com/api-information)

# Features
## MovieFileUtils
1. validate movie filename syntax

## TVShowFileUtils
1. validate tvshow directory syntax
2. validate season directory syntax
3. validate episode filename syntax

## TVDBUtils
1. search in tvdb for new seasons of existing tvshows
2. search in tvdb for missing episodes of existing seasons of existing tvshows

# Contribute
## Add new language
1. install `xgettext`
2. create the `messages.pot` file
   1. (unix) `find . -iname "*.py" | xargs xgettext -o messages.pot`
3. rename the `messages.pot` file to `plexutils.po`
4. move `plexutils.po` to `locale/xx_XX/LC_MESSAGES/`
5. execute `msgfmt locale/xx_XX/LC_MESSAGES/plexutils.po -o locale/xx_XX/LC_MESSAGES/plexutils.mo`
6. change the language in the config.yaml
7. DONE!
