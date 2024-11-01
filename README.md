# scorigami-sync

A simple CLI written in Python designed for syncing data from third party sports APIs to a remote server, as specified in [scorigami](https://github.com/razfrumkin/scorigami). This administrative tool is intended for private use of fetching and transferring sports data, ensuring that any remote server remains up to date with the latest sports information.

## Leagues

- **NBA**: [nba_api](https://github.com/swar/nba_api) to fetch NBA data.

## Examples

Fetch data from the latest NBA season:

```bash
python3 src/main.py nba fetch games latest
```

Sync data from a specific NBA season to the remote server:

```bash
python3 src/main.py nba sync <base-url> <password> games specific 2015-16
```

Sync data from all the NBA seasons to the remote server:

```bash
python3 src/main.py nba sync <base-url> <password> games all
```
