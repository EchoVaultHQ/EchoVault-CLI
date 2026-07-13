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

## Deployment

Releases publish to PyPI automatically via GitHub Actions (`.github/workflows/publish.yml`) whenever a `v*` tag is pushed.

1. Bump the version in `src/echovault/__about__.py`:
   ```python
   __version__ = "X.Y.Z"
   ```
2. Commit the bump:
   ```console
   git add src/echovault/__about__.py
   git commit -m "Bump version to X.Y.Z"
   git push origin main
   ```
3. Tag and push the tag to trigger the release:
   ```console
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
4. Watch the run under the repo's **Actions** tab. On success, the new version appears on [PyPI](https://pypi.org/project/EchoVault-CLI/#history).

**Notes:**
- Publishing uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) — no API token is stored in the repo. The trusted publisher on PyPI must point at the current GitHub owner/repo/workflow (`Settings → Actions → Publishing` on the PyPI project page); update it there if the repo is ever renamed or transferred.
- Re-running a release requires a new tag or a re-pushed tag (delete + recreate) — pushing an unchanged existing tag will not retrigger the workflow.

## Related Projects

- [EchoVault](https://github.com/ACS-lessgo/EchoVault) — the main desktop music player this CLI complements.

## License

`EchoVault-CLI` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
