# Setup Project
## install with poetry 
- [Poetry installation documentation](https://python-poetry.org/docs/#installation)
- open the terminal in the project directory
- execute `poetry install` to install the dependencies
- execute `poetry run python plexutils/main.py` to run the script


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
1. **Install pygettext:**
   `pygettext` is a tool included in the Python package, so no additional installation is required.
2. **Generate the messages.pot file:**
   Open Command Prompt (cmd) and navigate to your project directory containing your Python files. Run the following command to generate the `messages.pot` file:
   `pygettext -d plexutils -o messages.pot *.py`
3. **Move the messages.pot file to locale/xx_XX/LC_MESSAGES/:**
   Copy the `messages.pot` file to the corresponding directory for the desired language within the `locale` folder of your project. Replace `xx_XX` with the appropriate language code, e.g., `de_DE` for German.
4. **Rename the messages.pot file to plexutils.po:**
   After moving the `messages.pot` file to the appropriate directory, rename it to `plexutils.po`.
5. **Compile the .po file to a .mo file using msgfmt:**
   Open Command Prompt and navigate to the directory containing the `plexutils.po` file. Run the following command to use `msgfmt`:
   `msgfmt plexutils.po -o plexutils.mo`
6. **Change the language in the config.yaml file:**
   Open the `config.yaml` file in a text editor and update the language setting to your desired language, e.g., `language: de_DE`.
7. **Done!**
   Save all changes and restart your application to apply the new language setting.
