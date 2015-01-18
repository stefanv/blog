---
layout: post
title: "Emacs package management"
date: 2012-09-25 17:14
comments: true
categories: [emacs, python, scipy]
published: true
---

I recently tried to install MuMaMo as one of the dependencies for Takafumi
Arakaki's [Emacs-based IPython notebook][ein].  The instructions on the MuMaMo
webpage were as clear as mud and aimed primarily at Windows users.  Enters
[apt-get for Emacs][el-get]!

My Emacs setup is shared across multiple machines: a synchronized ``elisp``
folder, containing ``*.el`` files, along with my ``.emacs`` configuration.
``el-get`` allows you to share your package installation folder in a similar
fashion.  Here are some relevant configuration snippets:

```common-lisp

; Everything gets installed into ~/elisp, a folder
; I sync across all my machines

(setq el-get-dir "~/elisp/el-get")
(setq el-get-install-dir "~/elisp/el-get/el-get")
(add-to-list 'load-path el-get-install-dir)

; If el-get is missing, install it automatically

(unless (require 'el-get nil t)
  (url-retrieve
   "https://raw.github.com/dimitri/el-get/master/el-get-install.el"
   (lambda (s)
     (goto-char (point-max))
     (eval-print-last-sexp))))

; Install these packages, and call the specified configuration snippets
; after each load
(setq el-get-sources
      '(

        (:name ethan-wspace
         :after (progn
                  (global-ethan-wspace-mode 1)
                  (set-face-background 'ethan-wspace-face "gray95")))

        (:name column-marker
         :after (add-hook 'font-lock-mode-hook
                          (lambda () (interactive) (column-marker-1 80))))

; Also install these packages, no configuration required
(setq my-packages
      (append
       '(el-get maxframe markdown-mode ein python)
       (mapcar 'el-get-source-name el-get-sources)
       )
)

; Check packages and install any that are missing
(el-get 'sync my-packages)
```

There are two ways to specify packages to be installed: either include them in
the ``my-packages`` list, or add them to ``el-get-sources``, which in addition
allows further customization upon successful loading of the package.

[What's in your stack?][swc-stack] Here's my list of Emacs packages:

    Org Mode, Ethan's wspace, Tab Bar, Column Marker, Max Frame, EIN, Python,
    JS2

Do you know of any other useful packages?  Let me know!

<!-- References -->

[ein]: https://github.com/tkf/emacs-ipython-notebook
[el-get]: https://github.com/dimitri/el-get
[swc-stack]: http://software-carpentry.org/2012/09/whats-in-your-stack/
