# Setup Project

## install with poetry 

- [Poetry installation documentation](https://python-poetry.org/docs/#installation)
- open the terminal in the project directory
- execute `poetry install` to install the dependencies
- execute `poetry run compile-messages` to install other languages
- execute `poetry run generate-test-data` to generate the test data for the unittests
- execute `poetry run plexutils` to run the script


## config.yaml

To create a config.yaml file you can simply copy or rename the `example-config.yaml` file 
to `config.yaml` and adjust the settings to your needs.

### Language

#### Example

```yaml
language: de_DE
```

#### Supported languages

- `de_DE` german (germany)
- `de_AT` german (tyrol)
- `en_US` english

### Plex Libraries

#### Example

```yaml
libraries:
  - name: Movies
    type: movie
    lang:
      dub: de_DE
      sub: de_DE
    path: /.../movies
  - name: TV Shows
    type: tvshow
    lang:
      dub: de_DE
      sub: de_DE
    path: /.../tvshows
```

#### Description

Under the `libraries` key you can define your plex libraries. Each library has the following keys:

- `name` (required): The name of the library
- `type` (required): The type of the library. Possible values are `movie` and `tvshow`
- `path` (required): The path to the library
- `lang` (optional): The language settings for the library. Each library has the following keys:
  - `dub` (optional): The default is `en_US`. The language of the dubbing
  - `sub` (optional): The language of the subtitles

### TVDB Credentials

To get the TVDB credentials you need to create an account on 
[thetvdb.com](https://thetvdb.com/api-information) and create a new API key and pin.

#### Example

```yaml
tvdb:
  api_key: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  api_pin: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Description

Under the `tvdb` key you can define your TVDB credentials:

- `api_key` (required): The API key
- `api_pin` (required): The API pin

# Documentation

## Update the documentation

- open the terminal in the project directory
- execute `poetry run generate-docs` to generate the documentation with sphinx

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

### Unix

1. install `xgettext`
2. create the `messages.pot` file
   1. (unix) `find . -iname "*.py" | xargs xgettext -o messages.pot`
3. rename the `messages.pot` file to `plexutils.po`
4. move `plexutils.po` to `locale/xx_XX/LC_MESSAGES/`
5. execute `msgfmt locale/xx_XX/LC_MESSAGES/plexutils.po -o locale/xx_XX/LC_MESSAGES/plexutils.mo`
6. change the language in the config.yaml
7. DONE!

### Windows

1. install babel if not installed (`pip install Babel`)
2. create `babel.cfg` with `[python: **.py]` as its content
3. open Command Prompt (cmd) and navigate to your project directory. Run:
   ```
   pybabel extract -F babel.cfg -o messages.pot .
   ```
4. run the following command, replacing `xx_XX` with your language code (e.g., `de_DE` for German):
   ```
   pybabel init -i messages.pot -d locale -l xx_XX
   ```
5. open the generated .po file in `locale/xx_XX/LC_MESSAGES/` directory with a text editor and translate the messages into your desired language
6. rename the `messages.pot` file to `plexutils.po`
7. compile the .po file to a .mo file:
   Execute:
   ```
   pybabel compile -d locale
   ```
8. Open `config.yaml` in a text editor and update the language setting (e.g., `language: de_DE`)
9. DONE!
