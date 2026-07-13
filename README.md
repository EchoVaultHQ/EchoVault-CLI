# EchoVault CLI

A terminal (TUI) music player for your [EchoVault](https://github.com/ACS-lessgo/EchoVault) library, built with [Textual](https://github.com/Textualize/textual) and `pygame`.

-----

## Requirements

EchoVault CLI doesn't manage its own music library — it reads the same local database that the main [EchoVault](https://github.com/ACS-lessgo/EchoVault) desktop app builds when you add folders to your library. Install and run EchoVault at least once first, so `~/.config/EchoVault/sonicbox.db` exists and has tracks in it.

## Installation

```console
pip install EchoVault-CLI
```

Requires Python >= 3.8.

## Usage

Run the player from a terminal:

```console
echovault
```

Select a track in the list and use these keys to control playback:

| Key     | Action              |
|---------|----------------------|
| `space` | Play / Pause         |
| `n`     | Next track           |
| `p`     | Previous track       |
| `s`     | Toggle shuffle       |
| `r`     | Toggle repeat        |
| `+`     | Volume up            |
| `-`     | Volume down          |
| `q`     | Quit                 |

## CLI Preview

- ![EchoVault CLI theme 1](Screenshots/cli1.png)

- ![EchoVault CLI theme 2](Screenshots/cli2.png)

## Related Projects

- [EchoVault](https://github.com/ACS-lessgo/EchoVault) — the main desktop music player this CLI complements.

## License

`EchoVault-CLI` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
