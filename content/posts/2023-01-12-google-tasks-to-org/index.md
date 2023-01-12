---
title: "Google Tasks to Org"
summary: Where we download a Google Tasks list in org-mode format.
tags: ['org-mode', 'productivity']
---

I [previously posted]({{< ref "2020-04-28-voice-capture-org-tasks-on-android.md" >}}) on how to
use Google Assistant to voice capture notes, which can subsequently be
downloaded into an org file.
This approach no longer works, since the service used there was deprecated.

While I could not replicate that entire pipeline, specifically
the voice part, I at least found a way to capture tasks on Android and
transfer them to org mode.

I chose Google Tasks since (a) [it has an
API](https://developers.google.com/tasks/reference/rest) (unlike Keep) and
(b) there is a [strong possibility](https://9to5google.com/2022/09/20/google-tasks-assistant-reminders/)
that we'll have voice capture for tasks in the near future 🤞.

## Implementation

First, install Google Tasks on your phone, add a new TODO list, and add a few tasks.

Next, we are going to set up an [Apps
Script](https://developers.google.com/apps-script) service that will
convert our tasks to org format, and expose the result via a URL.

1. Create a new Google Sheets spreadsheet, named whatever you like (say, `Google Tasks to Org`).
2. Click on `Extensions ➡ Apps Script`; the editor opens. Name the app (say, `tasks-to-org`).
3. In the sidebar, click `Services` and enable the Tasks API.
4. Paste the following into the editor:

```javascript
// Once this code is deployed as a web app, you can call it via curl:
//
// URL="..."
// TOKEN="..."
// curl -s -S -L -d "$TOKEN" "$URL?clear=1" >> output.org
//
// Remember to customize `token` and `taskList` below.

function doPost(e) {
  // A token (your password) can be anything; you can generate it using, e.g., Python:
  //
  //   python -c "import base64, os; print(base64.b64encode(os.urandom(50)).decode('ascii'))"
  //
  const token = "abcdefg12345";

  // The name of the task list in Google Tasks
  // This name is case sensitive
  const taskList = "org";

  var response = "Invalid token";
  const clear = (e.parameter['clear'] === '1');

  if (e.postData.contents === token) {
    response = tasksToOrg(taskList, clear);
  }

  return ContentService.createTextOutput(response);
}

function doGet(e) {
  return ContentService.createTextOutput("OK");
}

function taskToOrg(task) {
  // See https://developers.google.com/tasks/reference/rest/v1/tasks#Task

  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
  var entry = '* ';
  const status = (task.status == "completed" ? "DONE" : "TODO");
  var deadline = '';
  var notes = '';

  if (task.due) {
    const due = new Date(task.due);
    const year = due.getFullYear().toString();
    const month = (due.getMonth() + 1).toString().padStart(2, '0');
    const day = due.getDate().toString().padStart(2, '0');
    const wkday = days[due.getDay()];
    deadline = `\n  DEADLINE: <${year}-${month}-${day} ${wkday}>`;
  }

  if (task.notes) {
    notes = task.notes.split("\n");
    for (let i = 0; i < notes.length; i++) {
      notes[i] = "\n  " + notes[i];
    }
    notes = notes.join("");
  }

  return `* ${status} ${task.title}${deadline}${notes}`;
}

function tasksToOrg(taskListTitle, clear) {
  var org_file = [];

  const taskLists = Tasks.Tasklists.list({maxResults: 100, showDeleted: true, showCompleted: true, showHidden: true}).items;
  const taskList = taskLists.filter(tl => tl.title === taskListTitle)[0];
  const taskListId = taskList.id;

  const tasks = Tasks.Tasks.list(taskListId);

  for (let i = 0; i < tasks.items.length; i++) {
    const task = tasks.items[i];

    org_file.push(taskToOrg(task));
  }

  if (clear) {
    for (let i = 0; i < tasks.items.length; i++) {
      const task = tasks.items[i];
      Tasks.Tasks.remove(taskListId, task.id);
    }
  }

  return org_file.join("\n");
}
```

## Deployment

We want to expose this script at a public URL, so go to `Deploy ➡ New Deployment` (`Deploy` is in the upper-righthand corner).

Set `Execute as` to your email and `Who has access` to anyone.
It needs to run as yourself, to access *your* tasks, and we need anyone to have access, since you will be calling the URL anonymously from the terminal (not signed in from a browser).

Click deploy.

Google will ask you to authenticate the app, and warn you that the app
is not officially authenticated. Click away the warnings and proceed
(you trust yourself, don't you?).

Now, you should be presented with a URL which, when accessed, runs the app.

## Configuration

Set the variable `token` to any long, hard-to-guess string of your choice. You can generate one with Python:

```sh
python -c "import base64, os; print(base64.b64encode(os.urandom(50)).decode('ascii'))"
```

Set the variable `taskList` to the same name as the list in Google Tasks.

## Task list to org

We can now access our app via a `POST` request.  E.g., using `curl`:


```sh
curl -s -S -L -d "abcdefg12345 your token value" https://script.google.com/macros/s/abc123-app-id-generated-by-google/exec
```

This should yield something like:

```text
* TODO First task
* TODO A task for today
  DEADLINE: <2023-01-11 Wed>
* TODO Another task
  This time, the task has a description.
```

To clear the tasks after downloading, add a `clear=1` argument:

```sh
curl -s -S -L -d "abcdefg12345 your token value" https://script.google.com/macros/s/abc123-app-id-generated-by-google/exec?clear=1
```

Here's the general script I use:

```sh
#!/bin/bash

TASKS_TO_ORG_URL="https://script.google.com/macros/s/.../exec"
ORG_INBOX="${HOME}/org/tasks-inbox.org"
TOKEN="abcdefg12345"

curl -s -S -L -d "$TOKEN" "$TASKS_TO_ORG_URL?clear=1" >> $ORG_INBOX
```

In my daily org planner, I then put:

```text
- [ ] ([[shell:~/scripts/google-tasks-to-org.sh][fetch]]) [[file:~/org/tasks-inbox.org][Google Tasks]]
```
