---
title: "Voice capture org-mode tasks on Android"
draft: false
description: Where I show how to hook up org-mode and Google Assistant
tags: ['org-mode', 'productivity']
---

I often want to capture tasks on the go—in a hurry. When there's no time to fire up [organice](https://organice.200ok.ch/) or [Orgzly](http://www.orgzly.com/), being able to transcribe tasks comes in really handy.

In this post, I show how, on Android phones, you can hook up Google's Assistant with org-mode, so that you can *speak* notes and have them appear as TODO items in a buffer.

## Set up Google Assistant

First, we need to teach Google Assistant a new keyword, and tell it to store transcribed notes in an accessible location.  We do this via the free [If This Then That](https://ifttt.com/) service.  Add the "Log notes in a Google Drive spreadsheet" applet, and configure it as follows:

- *What do you want to say?* `Add a task to $`
- *What's another way to say it? (optional)* `new task $`
- *And another way? (optional)* `task $`
- *Drive folder path (optional)* `Google Assistant`

This would allow you to say `task <description>` and have Google Assistant log that to a spreadsheet in the `Google Assistant` folder of your drive.

Save the applet and try it out: launch Google Assistant and say "task test out capture system".  Then, locate and open the new spreadsheet in your Google drive.  The URL should be of the form:

```
https://docs.google.com/spreadsheets/d/8B...ZFk/edit#gid=0
```

Note down that long string after `/d/`—this is your spreadsheet ID.

## Set up org-mode conversion

Go to `Tools -> Script Editor`, and include the script provided at
https://github.com/stefanv/org-assistant.

You have to customize two variables: the spreadsheet ID, and a random "token" (a password to make it harder for other to abuse the service).

Now, [publish the script to the web](https://developers.google.com/apps-script/guides/web#deploying_a_script_as_a_web_app): `Publish -> Deploy as web app...`.  Set `Who has access to the app` to `Anyone, even anonymous` and note down the published URL.

## Use it!

I have the following script that downloads TODOs and append them to an org-file:

```bash
#!/bin/bash

ASSISTANT_TO_ORG_URL="url-to-the-web-app"
ORG_INBOX="${HOME}/org/assistant-inbox.org"
TOKEN='token-value'

curl -s -S -L -d "$TOKEN" "$ASSISTANT_TO_ORG_URL?clear=1" >> $ORG_INBOX
```

I then have the following in my daily org checklist:


```org
[[shell:~/scripts/assistant-tasks.sh][fetch tasks]] : [[file:~/org/assistant-inbox.org][tasks]]
```

The first link launches the script that fetches the latest tasks, and the second opens the tasks file.

## Conclusion

Having a quick, hands-free way to capture tasks has been tremendously helpful to me.  I hope you find it useful too!
