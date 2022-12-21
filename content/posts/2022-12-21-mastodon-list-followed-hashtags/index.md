---
title: "Mastodon: How To List Followed Hashtags"
draft: false
tags: ['mastodon']
---

Mastodon recently introduced hashtags, but [does not
yet](https://github.com/mastodon/mastodon/issues/20763) have a user
interface for listing which hashtags you follow. Since there is an
[extensive API](https://docs.joinmastodon.org/api/), I thought it
would be straightforward to grab the list that way---and, it is, but
you need to perform the authorization dance correctly!

<!--more-->

## Query steps

1. To access the Mastodon API, you first register an application.
2. The application can make **public** queries, but to access personal information must first be granted access by the user.
3. Once the user authorizes the app, an oauth token can be obtained.
4. This token, in turn, allows personal API access.

## Implementation

Without further ado, some Python code which implements the above.
It caches secrets in `~/.config/mastodon-tags.yaml`.
I suspect tokens expire after a while, but the script doesn't yet take that into account.

```python
#!/usr/bin/env python

import requests
import yaml
import os
import webbrowser
import sys


SERVER = 'https://your.mastodon.server'
CONFIG = os.path.expandvars('$HOME/.config/mastodon-tags.yaml')


def get_config():
    if os.path.isfile(CONFIG):
        config = yaml.load(open(CONFIG, 'r'), Loader=yaml.SafeLoader) or {}
    else:
        config = {}
    return config


def update_config(update_dict):
    cfg = get_config()
    cfg = {**update_dict, **cfg}
    with open(CONFIG, 'w') as f:
        yaml.dump(cfg, f)
    return cfg


def post(url, **kwargs):
    data = requests.post(url, **kwargs).json()
    if 'error' in data:
        print(f'POST {url}')
        print()
        print(json['error'])
        sys.exit(1)
    return data


cfg = get_config()


if not 'client_id' in cfg:
    data = post(
        f'{SERVER}/api/v1/apps',
        json={
            'client_name': 'ls_hashtag',
            'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
            'scopes': 'read'
        }
    )
    cfg = update_config({
        'client_id': data['client_id'],
        'client_secret': data['client_secret']
    })


if not 'authorization_code' in cfg:
    oauth_url = f"{SERVER}/oauth/authorize?client_id={cfg['client_id']}&client_secret={cfg['client_secret']}&response_type=code&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
    webbrowser.open(oauth_url)

    auth_code = input("Enter token from browser window: ")
    cfg = update_config({
        'authorization_code': auth_code
    })


# Obtain OAuth access token
if not 'access_token' in cfg:
    data = post(
        f'{SERVER}/oauth/token',
        json={
            "grant_type": "authorization_code",
            "code": cfg['authorization_code'],
            "client_id": cfg['client_id'],
            "client_secret": cfg['client_secret'],
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob"
        }
    )
    cfg = update_config({
        'access_token': data['access_token']
    })

data = requests.get(
    f'{SERVER}/api/v1/followed_tags',
    headers={'Authorization': f"Bearer {cfg['access_token']}"}
).json()

N = max(len(tag['name']) for tag in data)
for hashtag in data:
    print(f'#{hashtag["name"]:{N}} {hashtag["url"]}')
```
