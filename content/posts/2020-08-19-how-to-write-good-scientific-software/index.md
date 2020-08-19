---
title: "How to Write Good Scientific Software"
draft: false
description: Where I discuss social, mechanical, and scholarly disciplines required for writing good scientific software.
tags: ['science', 'software', 'coding']
---

*This is a lightly edited transcript of a talk I delivered at MLSS South Africa on 16 January 2019.*

In this post, I will define scientific software, describe how it is
different from other types of software, and discuss the social,
mechanical, and scholarly disciplines required for making it the best
it can be.

Upfront, I should note that these are all rough guidelines, but that
the context in which software is developed and used will affect the
extent to which they apply.  I make some generalizations to get my
point across.

## What is Scientific Software?

Scientific software is typically computational in nature, and aids us
in our understanding of the world, often by processing observational
measurements.  Because scientific software aims to uncover *truths*,
**accuracy** is of paramount importance.  Of course, accuracy is
important in many industrial applications too---you do not want a
parcel delivered to the wrong address, or an email sent to the wrong
recipient---but in science errors invariably invalidate the work.

Here, I consider a subset of scientific software: that which is
written to aid in reproducibility.  This software has to be
**reusable**[^varoquaux-strive-for-reusability]---particularly by those who did not write the software.
Even if reproducibility is not explicitly targeted, eventually most
scientific codes become associated with research outputs, such as
published papers.  At this point, ideally, the software should be open
for inspection, so that the science can be verified.  The vast
majority of research code has *not* historically fallen into this
category[^research-false], but I would argue that there are systematic changes underway
that will place more and more emphasis on openness.

[^varoquaux-strive-for-reusability]: Gaël Varoquaux, [Beyond
    Computational Reproducibility, Let Us Aim for Reusability](http://gael-varoquaux.info/programming/beyond-computational-reproducibility-let-us-aim-for-reusability.html),
    IEEE CIS TC Cognitive and Developmental Systems (volume 32, number 2, 2016).

[^research-false]: [Why Most Published Research Findings Are False, https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124)

## Purpose

We write software for different purposes, and that changes the amount
of rigor applied.  Just as you may make some initial calculations on
a napkin, code is sometimes used to improve your understanding of a
problem, without any intent of using that code in future scenarios.

Apart from this type of "scratch" code, in increasing levels of
maturity we have: experimental code for private use, experimental code
that will be published, and algorithmic or infrastructure code with an
eye towards reusability.

I would argue that the first type---experimental code that never
leaves the room---is to be avoided at all cost.  This code cannot be
verified, and is in some sense no better than a black box that takes
some arguments and spits out an answer.  Is it a good answer that
reflects an underlying truth?  There is no way for anyone on the
outside to tell.

Experimental code should be tracked, just as you would fastidiously
keep a lab notebook in a chemical laboratory.

Now, let us examine the mechanisms we can use to improve the quality of
our software.  I want to start with a higher-level concept: that of
the social environment in which you develop software, and then move on
to more specific technical mechanisms.

## Social Software

> One day, while I was a postdoc at Berkeley's Helen Wills
> Neuroscience Institute, I walked into my office to find the
> DiPy---that is, Diffusion Imaging in Python---team, busy finalizing
> their new API design after an entire day's work.
>
> I happened to be implementing identical functionality for my research, not realizing
> that their library covered similar ground.  So, curious---and excited about the
> prospect of being able to collaborate and leverage their
> work---I started asking them about their new design, with my own use
> case in mind.
>
> It soon became clear that the software would not yet be able to address
> my needs.  To the team's credit, despite some tired and
> exasperated looks, they worked with me for the rest of the weekend
> to refine their design until we had a general enough
> interface that addressed all of our needs.
>
> For the next two years, I worked very closely with this team,
> helping them build out the package.  That software---which serves a
> niche purpose in MRI---now has more than 450 citations.

The takeaway for me was that, here, an extra pair of eyes made a
difference to the general utility of that software, and because of the
newly discovered synergy the development team grew, which in turn led
to many further hours of productive collaboration.

There is a large and ever-growing volume of research that shows the
advantages of group work.  For example, about an April 2006 [article in
the Journal of Personality and Social Psychology](https://www.apa.org/news/press/releases/2006/04/group.aspx), author Patrick
Laughlin from the University of Illinois says:

> "We found that groups of size three, four, and five outperformed the
> best individuals and attribute this performance to the ability of
> people to work together to generate and adopt correct responses,
> reject erroneous responses, and effectively process information."

This emphasizes the quality of work a team can do.  Other similar
experiments compare, e.g., teams of students against their professors.

For a team to work well, however, it has to have certain qualities,
such as the right size and culture.

Jeff Sutherland, the co-inventor of SCRUM and co-author of the Agile
Manifesto, said at the Global Scrum Gathering 2017 that he believed
the optimal team size is 5.

But he also observe something remarkable[^sutherland-book]: that while
individual developers different in productivity with a ratio of as
much as 1:10, the difference can be orders of magnitude larger when it
comes to teams.

[^sutherland-book]: Jeff Sutherland, Doing Twice the Work in Half the Time, Chapter 3

In 2012, Google launched Project Aristotle to determine what makes a
good team successful.  [One of their key findings](https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html?smid=pl-share) was that group norms
are a key to success.  In other words, it makes a difference when team
members feel comfortable enough to take risks, make mistakes, and
voice their opinions.

There are also some further straightforward connections with teams and
better work:

- Two pairs of eyes are better than one---you can help one another find
  flaws in your work.  Having other people *look* at your code (we
  typically call this "reviewing the code"), makes it better.  For
  open source libraries such as NumPy or scikit-image, it is not
  atypical to see many tens of comments on any proposed patch.
- As illustrated in the story above, your software is likely to have
  wider application when it serves multiple people.
- One team member may have insights the others don't.  E.g., they may
  have some esoteric piece of knowledge, such as a better
  interpolation scheme, a more stable algorithm, a better type of
  regularization, or know a common failure mode of a certain neural network
  structure.  Or, they may simply have a creative insight in the right
  moment.  It is not so much about having the smartest or most
  well-read team-members, as it is about creating intellectual
  diversity within the team.

In summary: find good and varied collaborators; your software will be
better because of it.

## Technical Mechanisms for Higher Quality Software

We now turn to more straightforward technical mechanisms, techniques,
and disciplines for improving the quality of your software.

> While working on a large open source project, we had a collaborator
> who did not "believe" in testing.  That person also happened to be a
> very talented programmer; still, I made a point of writing a test for
> each piece of functionality they included.  Invariably, almost every
> single contribution performed incorrectly on some corner case of the
> data.
>
> I knew at this point already that almost all the code I wrote was
> flawed in some way, and that it only improved through iterative
> refinement.  But it was an eye-opener to see that the best
> programmers still made mistakes---and frequently.
>
> Just like when you drive a car, you have certain blind spots while
> programming.  And just like you check that blind spot on the road,
> there are techniques we can use to make software development safer.

Let me highlight a few of those mechanisms:

### Test your software

At a very minimum, your software has to be run, frequently.  This does
not guarantee correct results, but at least allows you to go back and
re-run earlier steps of an analysis, as needed.  You'd be surprised
how many researchers are stuck in a situation where they cannot
explore new ideas, because parts of their pipelines are stuck in an unrunnable
state. This is bad news: bad for your research, bad for reproducibility, and
bad for any papers that rely on these stagnant results.

Ideally, however, your code will be tested thoroughly.  While, or
immediately after, writing code, you will examine corner cases,
generate (by hand if needed) test data, and compare output against
pre-calculated results.  The formula is simple: if I execute `f(x)`,
do I get `y` as expected?

Testing is my primary concern around Jupyter notebooks for serious
science.  They *can* be tested, but it is hard, and the mechanisms are
not widely available.  They also encourage the use of global state,
instead of functions.  As such, I strongly discourage my students from
using them other than for scratch experiments, or as a by-product of
research to allow others to explore data and results.

To automate your tests, you may make use of continuous integration
systems such as Travis-CI, Azure Pipelines, et cetera.
(See, e.g.,
[PR #3584 from NumPy](https://github.com/scikit-image/scikit-image/pull/3584),
and its [test results on Travis-CI](https://travis-ci.org/scikit-image/scikit-image/builds/465090731).)

### Track your progress

Using a revision control system is a must, and I recommend Git.  This
lets you track the history of your software as it evolves, reduces the
need to keep hundreds of backup copies, and allows other developers to
take part in development.  See revision control as the equivalent of
your lab notebook, but for your software.  You'll never need to worry
about lost code again, and your stress levels the day before
publishing will thank you for it.

In "The Toyota Way: 14 Principles From The World's Greatest
Manufacturer", Jeffrey Liker describes their 5S program for *effective*
and *productive* workspaces.  Three of these are: Sort, Straighten, and
Shine.  That is, sort out unneeded items, have a place for everything,
and keep your workspace clean.  Git provides the software tools to do
this.

### Document your code

Your code may never see another pair of eyes, but even for your own
benefit: document your code.  I suggest identifying a documentation
template, such as [the one we use for the NumPy project](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).  Here, we
decide beforehand the types of things that should be documented, so
that each function has the same information.  [For example](https://github.com/numpy/numpy/blob/master/numpy/linalg/linalg.py#L328), you can
describe: the intent of the function, input parameters, return values,
usage examples, and notes and references.

### Keep it simple

> We all know that moment.  Huzzah!  Ten lines of code condensed
> into a one-liner.  It's a divine piece of art, beautifully compact.
>
> And, yet, so utterly incomprehensible to future you.
>
> I don't know where the following idea originated, but Robert Martin
> states it well in "Clean Code".  He writes: “Indeed, the ratio of
> time spent reading versus writing is well over 10 to 1. We are
> constantly reading old code as part of the effort to write new
> code. ...[Therefore,] making it easy to read makes it easier to
> write.”
>
> In addition, Martin Fowler wrote: "Any fool can write code that a
> computer can understand. Good programmers write code that humans can
> understand."

Making code *shorter* does not necessarily mean making it *simpler* to
understand.  Strive for clarity of expression, instead.

I'll also note here that object orientation is a great distraction to
new programmers, when functional design would suffice for the majority
of cases.

### Algorithm over optimization

> We all know the Donald Knuth quote: "Premature optimization is the
> root of all evil".
>
> I experienced this first-hand while writing a library to calculate
> discrete pulse transforms of images.  I spent weeks on this project,
> utilizing every trick in the book: I wrote a library in C, cached
> every intermediate calculation, and invented a new sparse
> data-structure.  I felt *good* about this code; it was clever and
> fast.
>
> One day, an old professor walked into my office. "Oh, by the way," he
> said, "I wrote an implementation of the discrete pulse transform this
> weekend."  I ran his code: it executed correctly, and was at least as
> fast as mine.  Confused, I examined his work more closely: 80 lines
> of pure Python.  No particular optimizations.  Just: the right idea,
> aided by the appropriate built-in data structures (priority queues,
> in this case).
>
> It turns out the professor was the one who invented the algorithm,
> and he knew a thing or two about it. This experience taught me a
> valuable lesson: get the *execution order* right.  You can write
> your code in assembler, and your $\mathcal{O}(N^2)$ algorithm still
> won't beat $\mathcal{O}(N)$ runtime on a large enough dataset.
> Worry about implementing *the correct algorithm*, instead of
> optimizing the wrong one.

### Automate everything

As far as possible, automate all processes: building of your software,
testing, producing figures for papers, the works.  When you automate a
process, you have one place to go to make a fix that affects all of
your work.  Otherwise, you will be very tempted to only fix the
outputs that urgently require attention.

The Japanese has the practice of Kaizen (改善), or "continual
improvement".  Small changes, applied many times over, can result in
great progress.

As an example of a fully automated publication, see [Elegant SciPy](https://github.com/elegant-scipy/elegant-scipy).

### Be consistent

There is no single best way to structure and format code.  Pick a
style you like, and stick to it.  Structure your entire code base the
same way, and ask that collaborators use the same standards.  In the
Python world, we have PEP8; but use whatever your community
recommends.

## Scholarly publication

Finally, your scientific code will likely be of better quality if it
gets made public.  Why?  Because if you know your code is going to be
published, you will take better care in its construction,
documentation, and testing.  No one wants to have others look at their
poor quality work!

There are several ways to make code public.  The easiest is to publish
it in a public git repository on, e.g., GitHub or GitLab.  This also
allows external developers to submit changes for your consideration.

If that is not an option, a copy of the software can be uploaded to a
public repository, where it will receive a Digital Object Identifier,
or DOI---essentially a snapshot, that shows the state of the software
at a specific point in time.

A third option is to simply upload the software to your website.  It's
the way we used to do it, but we now have better mechanisms.

Whichever medium you use, remember to add a license to your software.
Without a license, your software cannot be reused by others.  It is
*not* simply public domain without a license; quite the contrary.

## Conclusion

Scientific software has the potential to change our understanding of
the world.  Discoveries, however, depend on accurate results, which
are more likely to arise from high quality code.  We suggest you write
your code in teams---it is not only more fun, but likely to be more
widely usable.  At a minimum, ensure that your code is *tested* and
*documented*.  Aim for *reusability*.  Then, *publish* your work: it will
make science more transparent, and it will make your code better.

## Notes

A friend reviewing my talk pointed me
to
[this article](https://towardsdatascience.com/modernizing-academic-data-science-4213794a278e)
by
[Patrick Beukema](https://pbeukema.github.io/) that covers similar
ground.  Looks like we're in agreement!
