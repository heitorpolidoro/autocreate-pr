# Autocreate Pull Request
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/autocreate-pr)

[![Latest](https://img.shields.io/github/release/heitorpolidoro/autocreate-pr.svg?label=latest)](https://github.com/heitorpolidoro/autocreate-pr/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/autocreate-pr)

[![CI/CD](https://github.com/heitorpolidoro/autocreate-pr/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/heitorpolidoro/autocreate-pr/actions/workflows/ci_cd.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_autocreate-pr&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_autocreate-pr)

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
  creating-pr:
    name: Create Pull Request
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Creating Pull Request
        uses: heitorpolidoro/autocreate-pr@v2
        with:
            automerge: true|false
        env:
          <user>: ${{ secrets.<USER_PERSONAL_ACCESS_TOKEN> }}
```
To enable a user to automatically creates a Pull Request set an `ENV` with the GitHub username passing the user Personal Access Token.
