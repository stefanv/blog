---
title: "Pomodoros with org-timer"
draft: false
summary: How to use org-mode as a pomodoro timer, and then show the pomodoro status on waybar.
tags: ['emacs', 'elisp', 'productivity']
---

*A New Year! Create the `2025.org` journal file, channel all that post-break energy, and get ready to be Super Productive™! 💪 Oh, what's this... [a post on how to track Pomodoros using org mode](https://charlbotha.com/til/Show-Emacs-org-timer-countdown-in-macOS-menubar). 👀 Of course, I didn't bite. Of course not.*

Productivity people sure spend a lot of time writing a lot about little; and the **Pomodoro technique** is no exception. It can be summarized as:

> Set a timer, get to work, take a break. Repeat, take a break.

There's way too much productivity literature out there, and much of it comes down to: *find a way to get your butt in the seat and start [writing/typing/reading/editing/...]*. The new wave of productivity literature, or ["anti-productivity" literature](https://www.oliverburkeman.com/), tells us to face the facts: you're never going to finish your TODO list, so give up already, be in the present, and focus on what's most important (or, whatever, just [be present](https://www.wakingup.com/)).

Sometimes, I get in the flow easily, and don't need any tricks. But other times, especially with those slightly-mundane-tasks-that-still-need-to-get-done, I need a little nudge not get started and not get distracted (by something more interesting which, in this case, may well be everything).

For me, the Pomodoro method is helpful for that purpose. And, **because distraction abounds**, it's helpful to **have the timer as well as the topic** you're supposed to be focused on **displayed somewhere visible**.

When I saw Charl's post, I was delighted because:

1. It relies on `org-mode`, which I already use;
1. it does everything I used `org-pomodoro` for, but more simply;
1. it provides an easy path towards integration with [waybar](https://github.com/Alexays/Waybar) (he uses xbar for macOS, but same idea); and,
1. as observed by Charl, it does not interfere with other org clocks.

So, what follows here is a slight modification of [Charl's method](https://charlbotha.com/til/Show-Emacs-org-timer-countdown-in-macOS-menubar), which in turn combines previous approaches by
[David Wilson (System Crafters)](https://systemcrafters.net/emacs-shorts/pomodoro-timer/) and [Xiang Ji](https://xiangji.me/2020/12/27/displaying-orgmode-clock-in-menu-bar/).

## Emacs configuration: basic

```lisp
(require 'org-timer)

;; If you want sound when the pomodoro is over
(setq org-clock-sound (expand-file-name "~/sounds/bell.wav"))

;; And if you'd like to have a keyboard shortcut for starting a Pomodoro
(defun org-timer-start-pomodoro ()
  (interactive)
  (setq current-prefix-arg 25)
  (call-interactively 'org-timer-set-timer))
(global-set-key (kbd "C-c P") 'org-timer-start-pomodoro)
```

Now, when you press `C-c P`, a new pomodoro timer is started (you'll see it in the mode line). You can also start it with `org-timer-set-timer`. After 25 minutes, when the Pomodoro is done, a system notification is displayed. Tada!

## Display pomodoro status on waybar

To display org-timer's status on waybar, we'll query emacs (via emacsclient[^emacsclient]) for its current value.

[^emacsclient]: Since Emacs 29, the emacsclient server is started automatically! 🙌

Here's the function, `org-timer-waybar-repr`, which generates the status text:

```lisp
(defun org-timer-minutes-to-string ()
  "Remaining org-timer minutes, rounded to nearest minute, as string."
  (let* ((time-string (org-timer-value-string))
         (parts (split-string time-string ":"))
         (hours (string-to-number (nth 0 parts)))
         (minutes (string-to-number (nth 1 parts)))
         (seconds (string-to-number (nth 2 parts)))
         (total-minutes (+ (* hours 60) minutes (/ seconds 60.0))))
    (number-to-string (round total-minutes))))

(defun org-timer-waybar-repr ()
  "Format org-timer status for waybar"
  (if (or
        (not (boundp 'org-timer-countdown-timer))
        (not org-timer-countdown-timer))
  "🤗"
  (concat
    "🍅 " (org-timer-minutes-to-string)
    "  🎯 " (org-link-display-format
              (substring-no-properties org-timer-countdown-timer-title)))))
```

Next, we need a script, say `org-timer-remaining`, to access this text:

```sh
#/bin/sh
emacsclient --eval '(org-timer-waybar-repr)' | sed 's/"//g'
```

(That `sed` bit is to strip the surrounding quotes from the resulting string.)

To display it in waybar, we need to tell waybar to call the script at a regular interval. In `~/.config/waybar/config`:

```json
{
  ...,
  "modules-left": [..., "custom/org_timer"],
  ...,
  "custom/org_timer": {
     "exec": "~/scripts/org-timer-remaining",
     "interval": 30,
     "signal": 8
  }
}
```

Now, after starting a timer, you should see something like:

![Waybar displaying org-timer status](waybar-org-timer.png)

One little trick 🪄: do you notice the `"signal": 8` above? You don't need it, but it's a mechanism provided by `waybar` for externally refreshing a widget. In this case, if we send a specific kill signal, the org-timer display will reload:

```sh
pkill -RTMIN+8 waybar
```

You can therefore add the following to your emacs configuration to refresh `waybar` the moment a pomodoro is created:

```lisp
(add-hook 'org-timer-set-hook
  (lambda ()
    (start-process "waybar-timer-trigger" nil "pkill" "-RTMIN+8" "waybar")))
```

## Things that didn't work

I'd have liked a tomato-themed notification for when my pomodoro expired. I can use `notify-send` to make that happen:

```lisp
(defun pomo-notify (MSG &optional TIMEOUT)
  """Display pomodoro notification with notify-send"""
  (apply
    'start-process
    "notify-send" nil "notify-send"
    `(,@(when TIMEOUT (list (format "--expire-time=%d" (* 1000 TIMEOUT))))
       ,MSG)))

(add-hook 'org-timer-done-hook (lambda () (pomo-notify "🍅 org-timer done!")))
```

However, now I have *two* notifications popping up: mine, and the org-timer one.
I tried to silence the org-timer notification using [advice](https://www.gnu.org/software/emacs/manual/html_node/elisp/Advising-Functions.html):

```lisp
(defun suppress-org-notify (orig-fun &rest args)
  (cl-letf (
             ((symbol-function 'org-show-notification) (lambda (&rest _) (ignore)))
           )
    (apply orig-fun args)))
(advice-add 'org-timer--run-countdown-timer :around #'suppress-org-notify)
```

Alas, my advice fell on deaf ears. Do you perhaps know how to make it work? Let me know!

## The end

En dit is dit. Geniet die tamaties!
