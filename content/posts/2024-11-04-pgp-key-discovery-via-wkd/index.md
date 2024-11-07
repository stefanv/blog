---
title: "PGP key discovery via Web Key Directory (WKD)"
draft: false
summary: |
  How Web Key Directory works for discovering PGP keys associated with a given email address,
  and how to set up your own.
tags: ['pgp', 'security', 'web-of-trust']
---

PGP (GPG) keys, while sometimes tricky to use, are also *super* useful: for encrypting files, for signing emails and software releases, and for [storing](https://www.passwordstore.org/) and [sharing passwords](https://github.com/scientific-python/vault-template).

In this post, we consider the situation where you have someone's email address, and want to send them a secure email or encrypted file.

(a) How do you find the PGP key associated with that email address?
(b) Can you say, with some confidence, that the key belongs to that person?
(c) How do you make your own key available to others.

## Finding a PGP key by email

PGP keys are distributed via key servers.
You can browse to, e.g., https://keys.openpgp.org or https://keyserver.ubuntu.com/, and search for your recipient's email.
GPG also knows how to receive keys from key servers.

How do you know *which key server* to use?
For that, you use the Web Key Directory (WKD): it's like a telephone book, that maps email addresses to their associated PGP keys.

Mail clients that support WKD include Protonmail, Thunderbird, and many others.
And GPG can use it too:

```sh
$ gpg --auto-key-locate local,wkd --locate-keys nameof@myfriend.org
gpg: key 34DC9100A65AA3BE: public key "nameof@myfriend.org <nameof@myfriend.org>" imported
```

Here `--auto-key-locate local,wkd` instructs GPG to find the key locally, or via the WKD—but to *not* query key servers otherwise.

## Does the key belong to your intended recipient?

Somewhat bizarrely, key servers used not to do much verification, and anyone could upload keys to them.
This is because *verifying* keys was meant to happen via the so-called "web of trust": if someone you know indicated that they trust a key (by signing it with theirs), then perhaps you could trust that key as well.
It seems like a good idea, but often you end up dealing with people outside of your network, rendering the web of trust useless.

Fortunately, modern key servers like https://keys.openpgp.org (which runs the cutely named [hagrid](https://gitlab.com/keys.openpgp.org/hagrid)—keeper of keys) are *verifying* key servers: they check, by emailing key uploaders, that they own the email address matching their uploaded key.
Unverified keys are stripped of their user IDs, ensuring that they can't be accidentally used.

The process isn't entirely watertight: if someone else has access to your email, then they could upload a compromised key.
But by then you have big problems already—how many service passwords can be obtained using "I forgot my password"?!

## Trust and WKD

We'd trust a telephone book if owners always *chose* to have their numbers published.
*Yep, that's Amy's number: she put it in the phone book herself.*
Similarly, for WKD, all entries are approved by the domain owner.

How does the WKD know where to find your key? Let's ask:

```sh
$ gpg-wks-client print-wkd-url spam@mentat.za.net
https://openpgpkey.mentat.za.net/.well-known/openpgpkey/mentat.za.net/hu/55caf3anhb75xpzx9m6hgw6589ozf1b9?l=spam
```

Here, the string `55caf...` is the word `spam`, of which the SHA-1 digest is encoded with z-base-32:

```python
import hashlib
import zbase32  # pip install z-base-32

username = 'spam'
sha1 = hashlib.sha1()

sha1.update(username.lower().encode('ascii'))
print(zbase32.encode(sha1.digest()))
```

```text
55caf3anhb75xpzx9m6hgw6589ozf1b9
```

Great, so for a given email address, we have a fixed URL to query.
At that location, we'll find the associated PGP key in binary format.
**And**, we know that **the domain owner explicitly provided its location** (either by hosting the key at the given URL, or by reconfiguring their DNS records to point `openpgpkey.theirdomain.org` to another keyserver).

## Hosting WKD

There are two options for hosting WKD:

(1) Point your DNS to a verifying key server, such as https://keys.openpgp.net.
    This process is [covered in detail by friend Charl over at vxlabs](https://vxlabs.com/2024/10/24/openpgp-wkd-for-easy-pgp-key-discovery/).

(2) Host a static website at https://openpgpkey.yourdomain.org.
    This approach has the slight advantage that it lets you publish external
    signatures of your key (i.e., when your friends and colleagues sign
    your keys)—which get stripped by keys.openpgp.org.
    But [newer versions of GPG will ignore those anyway](https://inversegravity.net/2019/web-of-trust-dead/).

The site should have the following structure:

```text
.well-known/
.well-known/openpgpkey
.well-known/openpgpkey/mydomain.org
.well-known/openpgpkey/mydomain.org/policy
.well-known/openpgpkey/mydomain.org/submission-address
.well-known/openpgpkey/mydomain.org/hu/55caf3anhb75xpzx9m6hgw6589ozf1b9
```

The files `policy` and `submission-address` can be empty, according to the [WKD RFC](https://datatracker.ietf.org/doc/draft-koch-openpgp-webkey-service/).

For each email address, calculate its ID (use the Python script above or `gpg-wks-client print-wkd-url`), and add its binary key.
Using GPG, you'd generate the key using:

```sh
gpg --export [KEY-ID-IN-HEX] > .well-known/openpgpkey/mydomain.org/hu/55caf3anhb75xpzx9m6hgw6589ozf1b9
```

For a full example, see [my WKD site for openpgpkey.mentat.za.net](https://github.com/stefanv/openpgpkey.mentat.za.net).
You can verify that it works by looking me up: my first name at mentat.za.net.

I opted for this route because I like publishing a key which my friends and colleagues have co-signed.
Besides, having your key signed, and signing someone else's key, makes for some fun in this age of remote isolation!

## Takeaways

1. Publish your key via WKD—this makes it clear to others which key you want them to have.
2. Do not use unverified PGP key servers (use https://keys.openpgp.org).
3. Setting up WKD for your domain is as easy as hosting a static site, or adding a CNAME entry to your DNS.

Go ahead, make your PGP keys discoverable using WKD!
