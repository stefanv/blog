Title: Using org-mode with neomutt
Tags: org-mode, emacs, python, mutt
Status: published

[org-mode](https://orgmode.org) is, to me, is one of the most valuable
parts of the emacs ecosystem.  I use it to take notes, plan projects,
manage tasks, and write & publish documents.

Nowadays, a lot of work arrives via email, and so it is helpful to be
able to refer to messages directly from my notes or lists of
tasks.

The *simplest* option might be to store URLs pointing to an online
inbox such as [Fastmail](https://fastmail.com) or GMail, but I wanted
a solution that was both future proof (i.e., what if I moved my emails
to a different provider?) and worked with my terminal-based mail
client of choice, [neomutt](https://neomutt.org/).

I started with
a
[solution provided by Stefano Zacchiroli](https://upsilon.cc/~zack/blog/posts/2010/02/integrating_Mutt_with_Org-mode/),
and simplified it for my specific use-case.

## Overview

The solution has two parts: sending email links from neomutt to Emacs,
and later opening those links from Emacs by invoking neomutt.  The
first achieved via `org-protocol`, the latter via launching neomutt
and then simulating keypresses.

When launching neomutt, we have to tell it in which directory the
message lives.  We therefore use `notmuch` to find the message file
first, based on its Message-ID.  `maildir-utils` would be another way
of doing so.  **Please note that you have to have notmuch or
maildir-utils set up already for this scheme to work.**

I initially avoided the `org-protocol` package, because installation
looked complicated.  That, it turns out, is only the case if you care
about web browser integration, which we don't.

## Neomutt configuration

First, we have a Python script that can parse an e-mail and share the
Message-ID and Subject with emacs.  I call it `mutt-save-org-link.py`,
and make it executable using `chmod +x mutt-save-org-link.py`.

```python
#!/usr/bin/env python3

import sys
import email
import subprocess

# Parse the email from standard input
message_bytes = sys.stdin.buffer.read()
message = email.message_from_bytes(message_bytes)

# Grab the relevant message headers
message_id = message['message-id'][1:-1]
subject = message['subject']

# Ask emacsclient to save a link to the message
subprocess.Popen([
    'emacsclient',
    f'org-protocol://store-link?url=mutt:{message_id}&title={subject}'
])

```

We then configure neomutt (typically in `~/.muttrc`) to call the
script with a shortcut.  I chose Esc-L (the same as Alt-L).

```
macro index,pager \el "|~/scripts/mutt-save-org-link.py\n"
```

## Emacs configuration

Using `org-protocol`, we instruct emacsclient to intercept URLs with
the `org-protocol://` scheme, as used by our `mutt-save-org-link.py`
script.  We also tell org-mode how to handle special URLs of the form
`mutt:message-id+goes_here@mail.gmail.com`.  Neomutt needs to know
which Maildir folder to open, so we ask `notmuch` to tell us where the
message is located.

In my `~/.emacs` file I have:

```elisp
; Make sure org-protocol is loaded
; Now, org-protocol:// schemas are intercepted.
(require org-protocol)

; Call this function, which spawns neomutt, whenever org-mode
; tries to open a link of the form mutt:message-id+goes_here@mail.gmail.com
(defun stefanv/mutt-open-message (message-id)
  "In neomutt, open the email with the the given Message-ID"
  (interactive)
  (let*
      ((mail-file
        (replace-regexp-in-string
         "\n$" "" (shell-command-to-string
                   (format "notmuch search --output=files id:%s" message-id))))
       (mail-dir (replace-regexp-in-string "/\\(cur\\|new\\|tmp\\)/$" ""
                                           (file-name-directory mail-file)))
       (process-id (concat "neomutt-" message-id))
       (message-id-escaped (regexp-quote message-id))
       (mutt-keystrokes
        (format "l~i %s\n\n" (shell-quote-argument message-id-escaped)))
       (mutt-command (list "neomutt" "-R" "-f" mail-dir
                           "-e" (format "push '%s'" mutt-keystrokes))))

    (message "Launching neomutt for message %s" message-id)
    (call-process "setsid" nil nil
                   "-f" "gnome-terminal" "--window" "--"
                   "neomutt" "-R" "-f" mail-dir
                   "-e" (format "push '%s'" mutt-keystrokes))))

; Whenever org-mode sees a link starting with `mutt:...`, it
; calls our `mutt-open-message` function
(org-add-link-type "mutt" 'stefanv/mutt-open-message)
```

There are a few caveats: if you use `maildir-utils`, the search
command is `mu find -f l i:%s` instead of notmuch; and if you are not
on Linux, then `setsid` (which we use to launch a detached background
process) is not going to work, and you will want to use a different
terminal emulator.

## Wrap-up

That's it!  I've added the code
to
[https://github.com/stefanv/org-neomutt](https://github.com/stefanv/org-neomutt).
Please file issues and PRs there, or tell me about your use cases
in the comments below.
