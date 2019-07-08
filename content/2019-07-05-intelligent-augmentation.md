Title: Designing for Intelligent Augmentation
Tags: artificial intelligence, machine learning, design
Status: published
Summary: How can we better design systems that combine computational inference and human intelligence?

The first issue of the [Harvard Data Science Review](https://hdsr.mitpress.mit.edu/) was published last month.  I enjoyed [Michael Jordan's opinion piece](https://hdsr.mitpress.mit.edu/pub/wot7mkc1), in which he considers progress made (and, yes, hype!) in so-called artificial intelligence.  Particularly, I was excited about the phrase "Intelligent Augmentation"—the pursuit of systems that enhances our ability to reason about a subject, by providing additional analysis, data, and emphasis. Jordan writes:

> IA will also remain quite essential, because for the foreseeable future, computers will not be able to match humans in their ability to reason abstractly about real-world situations. We will need well-thought-out interactions of humans and computers to solve our most pressing problems. And we will want computers to trigger new levels of human creativity, not replace human creativity (whatever that might mean).

A week ago, I attended a family event where I got pulled into a surprisingly animated argument around Google Maps: is it accurate, is it helpful, and what are we losing by relying on it. The argument took all the predictable turns (yes, kids nowadays cannot use maps any more, and if Google decided to summon us all to the Mountainview HQ as an April Fool's joke, the results would be comically sad). But an interesting outcome was the question: "How can we better design systems to *help humans* make good decisions?"

![Lemmings walking off a cliff, which they do—but to migrate, not commit suicide](https://i.ytimg.com/vi/fmnTfkFN3KE/hqdefault.jpg)

E.g., Google Maps tells you where to drive—they maybe even give you one or two route options.  But the overarching goal is to get you to your destination in the shortest amount of time.  What if you felt like taking a scenic drive, or wanted to explore a bit?  In that case, a map that showed a compass and traffic for all nearby roads would be much more helpful. How many times do we drive past a national monument such as [Bodie](http://www.parks.ca.gov/?page_id=509), or a street festival on the next block over without realizing it? Maps could certainly alert us to these.

At the Berkeley Institute for Data Science, I build a lot of open source research software. I've learned that systems that work *with* humans are often both simpler to develop and ultimately more effective than fully automated systems. When we wrote [Inselect](https://naturalhistorymuseum.github.io/inselect/) with the Natural History Museum, it would have been very hard to do a 100% accurate segmentation of insect speciments (especially since many of the photos this would be applied to contained insects unseen during training).  But if you can provide reasonable accuracy, humans can easily adjust for minor discrepancies and still save a lot of time.

With this blog post, I encourage software designers to:

> Think about how to best empower your users, rather than to prescribe their behavior implicitly through design decisions.  Be mindful that users may have experience to contribute and a desire to execute their own plan; **augment** their ability to do so effectively.

Circling back to Jordan's article, I encourage you to read the various commentaries (for now, the easiest way to find them is to scroll down to the article on the [journal front-page](https://hdsr.mitpress.mit.edu/)).  I enjoyed, e.g., [David Donoho's](https://hdsr.mitpress.mit.edu/pub/rim3pvdw), where he discusses the requirements for "true intelligence" in AI, although I think he may have misinterpreted Jordan's intent with the term "augmented intelligence".

I'll end with a quote from Greg Cane's [commentary](https://hdsr.mitpress.mit.edu/pub/kyzf7fjv):

> For the humanist, intelligence augmentation must now and forever be our goal. Machine learning only matters insofar as it makes us fundamentally more intelligent and deepens our understanding.
