# Autocreate Pull Request
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/autocreate-pr)
[![Latest](https://img.shields.io/github/release/heitorpolidoro/autocreate-pr.svg?label=latest)](https://github.com/heitorpolidoro/autocreate-pr/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/autocreate-pr)

[![CI/CD](https://github.com/heitorpolidoro/autocreate-pr/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/heitorpolidoro/autocreate-pr/actions/workflows/ci_cd.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_autocreate-pr&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_autocreate-pr)

![GitHub](https://img.shields.io/github/license/heitorpolidoro/autocreate-pr)

Action to create a pull request automatically with an option to set auto-merge.

### Usage
```yaml
name: Create Pull Request

on:
  create

jobs:
  create-PR:
    name: Create Pull Request
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Creating Pull Request
        uses: heitorpolidoro/autocreate-pr@v2.1.0
        with:
            draft: true|false # default: false
            automerge: true|false # default: false
        env:
          <user>: ${{ secrets.<USER_PERSONAL_ACCESS_TOKEN> }}
           # or          
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```
To allow a user to automatically create a pull request, define an `env` with the GitHub username passing in the user's personal access token, 
or pass the GITHUB_TOKEN env to allow to any user.
To enable auto-merge: [Automatically merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request)

