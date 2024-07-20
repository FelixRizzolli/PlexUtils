# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-07-20

### Added

- Added auto generated documentation with sphinx.
- Support for multiple plex libraries (#1).
- New settings menu to configure the plex libraries, the tvdb credentials and the language (#6).
- Added warnings to the MovieFileUtils menu if the required configuration is not set (#16).
- Added warnings to the TVShowFileUtils menu if the required configuration is not set (#17).
- Added warnings to the TVDBUtils menu if the required configuration is not set (#18).

## [1.0.1] - 2024-05-24

### Fixed

- Bugfix: the validation checks have been adapted to the plex naming conventions.

## [1.0.0] - 2024-05-19

### Added

- **MovieFileUtils** - validate movie filename syntax
- **TVShowFileUtils** - validate tvshow directory syntax
- **TVShowFileUtils** - validate season directory syntax
- **TVShowFileUtils** - validate episode filename syntax
- **TVDBUtils** - search in tvdb for new seasons of existing tvshows
- **TVDBUtils** - search in tvdb for missing episodes of existing seasons of existing tvshows

[Unreleased]: https://github.com/FelixRizzolli/PlexUtils/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/FelixRizzolli/PlexUtils/releases/tag/v1.0.0