# Autocreate Pull Request
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/autocreate-pr)

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
      - name: Checkout
        uses: actions/checkout@v3

      - name: Creating Pull Request
        uses: heitorpolidoro/autocreate-pr@v2
        env:
          <user>: ${{ secrets.<USER_PERSONAL_ACCESS_TOKEN> }}
```
To enable a user to automatically creates a Pull Request set an `ENV` with the GitHub username passing the user Personal Access Token.