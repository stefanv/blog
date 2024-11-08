---
title: "Adobe's new free font: Source Code Pro"
slug: consolas-vs-source-code-pro
date: 2012-09-26
tags: ['coding', 'emacs', 'linux']
status: published
---


Adobe yesterday
[released its free and open source Type family, Source Code Pro][scp-release],
which includes an eye-pleasing monospace font  ideally suited for coding.
In the past, and at the recommendation of [Fernando Perez][fperez], I've
used the beautiful (but non-free) [Consolas by Microsoft][consolas]; now,
which is best?

To install on Linux:

 1. [Grab the font][scp-download].
 2. Copy the files to ``~/.fonts``.
 3. Run ``fc-cache -f -v``.

The font should now be available for selection in apps such as Firefox, Gnome
Terminal, etc.  To make it the default font in Emacs::

```emacs-lisp
    (set-default-font "Source Code Pro")
```

Here's a comparison of Consolas (left) and Source Code Pro (right):

{{< figure src="consolas_vs_source_code_pro.png" title="Comparison: Consolas vs Source Code Pro" >}}

Comments also on [Google+][].

[Google+]: https://plus.google.com/104831275312843762750/posts/Ju6Ns8Dtuik
[fperez]: http://blog.fperez.org/
[consolas]: http://www.microsoft.com/en-us/download/details.aspx?id=17879
[scp-release]: http://blogs.adobe.com/typblography/2012/09/source-code-pro.html
[scp-download]: https://github.com/adobe-fonts/source-sans-pro/releases/tag/variable-fonts
