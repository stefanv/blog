Title: Search headers in org-mode
Tags: emacs, org-mode
Status: published
Summary: Where we show a quick way of navigating org-mode files.

In org-mode, I often have the need to jump to a top-level heading
matching some word.

Since an org-mode buffer can be searched just like any other, I can
simply invoke forward search with `C-s`, but this will match *all*
occurrences of the text, instead of limiting the search to headings only.

This makes it hard to search for a phrase like "Travel", for which I
have a top-level heading, but also often occurs elsewhere in my notes.

I have a solution of the following form:

1. Launch a regular expression search
2. Pre-fill the text input with `^* ` so that only headings are
   matched.

First, define a custom search function.  It puts the keys `^* ` in the
"unread command events" list (i.e, a list of events waiting to be seen
by emacs), and then launches interactive forward regular expression search.

```elisp
(defun stefan/isearch-heading ()
  (interactive)
  (setq unread-command-events (listify-key-sequence "^* "))
  (isearch-mode t t nil t))
```

Next, we add a keybinding for org-mode:

```elisp
(defun org-mode-keys ()
  (interactive)
  (local-set-key (kbd "C-c g") 'stefan/isearch-heading)
)
(add-hook 'org-mode-hook 'org-mode-keys)
```

And that's it!  Pressing `C-c g` (for "go") in org-mode will
now present you with a search prompt.  Typing a heading name will take you
there directly, at which point you can choose to expand it with the
TAB key.
