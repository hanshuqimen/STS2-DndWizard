# Contributing

Issues and pull requests are welcome. Include the target game, BaseLib and mod versions when reporting bugs, together with reproduction steps and relevant errors.

Keep changes focused. Edit generate_content.py for card data/localization and regenerate content instead of editing generated card classes. Include English and Chinese text for new content and an original illustration for each new playable card.

Run the offline rule and content checks described in docs/BUILD.md. Full mod builds require your own game and BaseLib installation. Do not commit game binaries, extracted game assets, private logs, credentials or local backups.

Clearly distinguish offline verification from in-game testing. A passing CI does not mean gameplay or balance has been tested.
