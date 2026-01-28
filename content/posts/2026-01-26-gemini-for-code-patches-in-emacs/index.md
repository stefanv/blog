---
title: "Using Gemini for Code Patches in Emacs"
draft: false
summary: How to configure Gemini for generating code patches in Emacs.
tags: ['emacs', 'LLMs']
---

To ensure that my skepticism of LLMs did not blind me to progress,
and to keep my finger on the pulse, I've been incorporating them into
my Emacs config, starting with
[gptel](https://github.com/karthink/gptel) and, more recently,
[macher](https://github.com/kmontag/macher). In December, I took
another look at Gemini, and noticed a *significant* improvement over
Flash 2.5 with the arrival of Flash 3 Preview.

In this post, I share the configuration I currently use, and
mention some open questions I still hope to address.

## Tools

`gptel` is a beautifully clean and simple interface for LLM chat.
Despite its simplicity, it actually has fairly advanced functionality,
which includes MCP integration, introspection of queries, multi-modal
input (such as images), and tool usage (extending LLMs with access to
elisp functions of your choosing).

`macher` runs on top of `gptel`. It provides a "pseudo-agentic"
workflow, in which you provide the LLM context about your current
project, such as the list of files. It also defines several tools that
the LLM can use, such as the ability to read files. You can use
`macher` to generate a patch, which you then review, apply the
parts you like, or ask `macher` for further improvements.

## Configuration

The `macher` installation simply follows the recommendations in its README:

```elisp
(use-package macher
  :custom
  ;; better folding and source block highlighting of the reasoning process
  (macher-action-buffer-ui 'org)

  :config
  (macher-install)
  (macher-enable))
```

And here is the basic `gptel` configuration, ensuring that `macher` is pre-loaded:

```elisp
(use-package gptel
  :commands (gptel gptel-mode)
  :config
  (require 'macher))
```

Now the model definition for Gemini, to access the latest 3.0 models:

```elisp
;; https://ai.google.dev/gemini-api/docs/models
(setq
  gptel-model 'gemini-3-flash-preview
  gptel-backend (gptel-make-gemini "Gemini"
                  :key "<Get your key at aistudio.google.com>"
                  :stream t
                  :models '(gemini-3-flash-preview
                            gemini-3-pro-preview
                            gemini-2.5-flash
                            gemini-2.5-pro)))
```

Note how you list the models you want to choose from, and then pick the default.

You will need an API key, which you can generate at
https://aistudio.google.com.  I'm pretty sure you also need to
activate billing to access `gemini-3-flash-preview`, but let me know
if you succeed without doing that. My total cost, after playing around
with it a bunch this week, was ~3 USD.

If your Emacs config lives in a public repository or on an untrusted
machine, you'll want to be careful in adding the token to it.  `gptel`
[automatically uses tokens listed in `~/.authinfo`](https://github.com/karthink/gptel?tab=readme-ov-file#optional-securing-api-keys-with-authinfo).
See [Mastering Emacs](https://www.masteringemacs.org/article/keeping-secrets-in-emacs-gnupg-auth-sources)
for more on
[auth-source](https://www.gnu.org/software/emacs/manual/html_mono/auth.html).

### Adding Google search

**EDIT: I've since noticed that, while adding the search tool this way works, it also messes up macher. So, don't try this yet until #750 is resolved.**

The above configuration works fine, but I noticed that some answers
were outdated.  Gemini supports "grounding" via Google Search. For
example, instead of telling you that TypeScript 5.3 is the newest
release (which it was, at the time of its training), it can use Google
Search to verify that, in fact, the latest version is 5.9.

[gptel#750](https://github.com/karthink/gptel/issues/750) tracks the
issue, but in the meantime you can manually adjust the query sent to
Google, and tell it to enable [Grounding with Google Search](https://ai.google.dev/gemini-api/docs/google-search):

```elisp
;; Enable Google Search capability for gemini
(cl-defmethod gptel--request-data :around ((backend gptel-gemini) prompts)
  "Add search ability to Gemini requests."
  (plist-put (cl-call-next-method) :tools (append '(:google_search ()))))
```

This is obviously just a temporary hack, until #750 can be resolved.

Grounding with Search may incur additional costs, as per the [Gemini API docs](https://ai.google.dev/gemini-api/docs/pricing):

> 5,000 prompts per month (free), then (Coming soon**) $14 / 1,000 search queries

## Usage

To generate a patch on your current project, you must do two things:

1. **Select project:** Tell `macher` which project you're working
   on. The easiest way to do this is to open a gptel buffer (which you
   can give any name you like, e.g. `gemini:add-tests`) and then `M-x
   cd` (change directory) into your project.

   I haven't checked, but I suspect this requires the project to be
   under version control.

2. **Activate macher:** As part of your query, mention `@macher`
   anywhere to enable it. E.g., `@macher add unit test
   scaffolding`. `C-c <enter>` executes the query.

   If you type `@macher` and it does not get highlighted with a little
   box surrounding the text, then `macher` isn't correctly
   installed. Try running `M-: (macher-install)` manually.

   You can add additional context to a query (e.g., a programming
   guidance document outside of the project) using `gptel-add` (this
   is standard `gptel` functionality).

While the query is executing, it displays a folded reasoning
block. You can type TAB to unfold it, and watch the various steps the
LLM takes. After a while, a patch will be generated in a separate
window.

You can apply the entire patch using `diff-apply-buffer`, or single
parts of the patch with `diff-apply-hunk`.

## Issues to resolve

With my configuration, `diff-apply-buffer` works fine as long as only
existing files are modified. When new files need to be created, it
misunderstands the file prefix in the patch, and fails to
auto-complete its name. I filed an issue to discuss that with the
macher author at
[macher#45](https://github.com/kmontag/macher/issues/45), and
hopefully can post an update soon.

## Conclusion

LLMs recently seem to have undergone a phase change in coding
ability.  Of course, even in this phase any code generated needs to be
very carefully reviewed and tested. [Andrej Karpathy's tweet earlier
today](https://x.com/karpathy/status/2015883857489522876) summarizes
where we stand quite well (I recommend reading the top comments too).

E.g., when talking about the new capability, he also warns:

> The nearest neighbor really is some kind of a junior engineer. Its
> ideas about what experiments to run [...] have been
> surprisingly bad, but its execution on ideas I've given it have been
> surprisingly good. — https://x.com/karpathy/status/2015888674739912910

> The mistakes have changed a lot - they are not simple syntax errors
> anymore, they are subtle conceptual errors that a slightly sloppy,
> hasty junior dev might do. The most common category is that the
> models make wrong assumptions on your behalf and just run along with
> them without checking. They also don't manage their confusion, they
> don't seek clarifications, they don't surface inconsistencies, they
> don't present tradeoffs, they don't push back when they should, and
> they are still a little too sycophantic. — https://x.com/karpathy/status/2015883857489522876

So, while we should tread with care, there are exciting avenues to explore. I've been developing open source computational libraries for a long time, and as [our ecosystem](https://scientific-python.org) grows I notice myself spending more and more time on maintenance, and less and less time on reading papers and developing new features. My hope is that LLMs will free our small communities—who have very limited time and resources—from repetitive, tiring maintenance tasks, so we may return to what we love to do: crafting intuitive APIs around innovative algorithms that, in turn, enable real-world science.
