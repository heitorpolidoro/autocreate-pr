# Autocreate Pull Request


[![Latest](https://img.shields.io/github/release/heitorpolidoro/autocreate-pr.svg?label=latest)](https://github.com/heitorpolidoro/autocreate-pr/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/autocreate-pr)
![GitHub](https://img.shields.io/github/license/heitorpolidoro/autocreate-pr)

Action to create a pull request automatically.

### Usage
```yaml
name: Create Pull Request

on:
  push:
    branches-ignore:
      - master

jobs:
  creating-PR:
    name: Create Pull Request
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Creating Pull Request
        uses: heitorpolidoro/autocreate-pr@v1
        env:
          <user>: ${{ secrets.<USER_PERSONAL_ACCESS_TOKEN> }}
```
To enable a user to automatically creates a Pull Request set an `ENV` with the GitHub username passing the user Personal Access Token