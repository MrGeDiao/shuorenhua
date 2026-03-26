# English Banned Phrases

> Sources: humanizer, stop-slop, avoid-ai-writing, beautiful_prose.

## Tier 1: Replace by default

These words appear 5–20x more often in AI text than human text. Replace by default, but allow exceptions per misfire protection rules (see `severity.md`).

### Throat-clearing openers
- Here's the thing
- The uncomfortable truth is
- Can we talk about
- Let's be honest
- I'll be frank
- It's worth noting that
- At its core
- At the end of the day
- In today's world
- In a world where
- What this means is
- It's important to note

### Emphasis crutches
- Full stop.
- Let that sink in.
- Make no mistake.
- Mark my words.
- I promise.
- Read that again.
- Period.

### Business jargon
- leverage → use
- navigate → handle, deal with
- unpack → explain
- lean into → accept, try
- deep dive → detailed look
- game-changer → important change
- circle back → revisit
- synergy → cooperation
- ecosystem → system, community
- streamline → simplify
- empower → let, enable
- actionable → practical
- learnings → lessons
- thought leader → expert
- best practices → good practices
- holistic → complete, whole

Keep literal technical uses in graph, network, routing, or pathfinding contexts. Example: `The system navigates the network topology using Dijkstra's algorithm.`

### Inflated verbs (use simpler alternatives)
- utilize → use
- commence → start
- endeavor → try
- ascertain → find out
- facilitate → help
- cultivate → build, grow
- elucidate → explain
- ameliorate → improve
- galvanize → motivate
- bolster → support
- spearhead → lead
- catalyze → trigger
- reimagine → rethink

### Significance inflation
- testament to → shows
- serves as → is
- stands as → is
- showcases → shows
- underscores → shows
- highlights → shows
- pivotal → important
- groundbreaking → new
- cutting-edge → new, latest
- watershed moment → turning point
- indelible mark → lasting effect
- paradigm shift → major change

### Copula avoidance (just use "is/are/has")
- serves as a → is a
- stands as a → is a
- represents a → is a
- functions as a → is a
- boasts a → has a
- features a → has a
- presents a → has a

### Filler phrases
- In order to → To
- Due to the fact that → Because
- At this point in time → Now
- It is important to note that → (delete)
- The system has the ability to → The system can
- It goes without saying → (delete)

### Sycophantic / meta
- Great question!
- You're absolutely right!
- Certainly!
- Of course!
- I hope this helps!
- Let me know if you'd like me to expand
- In this essay we will explore
- As we'll see
- Here is a/an

## Tier 2: Flag when 2+ appear in same paragraph

Legitimate individually, clustering signals AI.

- harness, navigate, foster, elevate, unleash
- resonate, revolutionize, underpin, nuanced, crucial
- multifaceted, myriad, plethora, encompass
- transformative, cornerstone, paramount, poised
- burgeoning, nascent, quintessential, overarching

## Tier 3: Flag at high density only

Common words, only problematic at high density. Thresholds: 3+ in short text (<200 words), 5+ in medium text (200–1000 words), >0.5% in long text (>1000 words). See `severity.md` for details.

- significant, innovative, effective, dynamic
- scalable, compelling, unprecedented, exceptional
- remarkable, sophisticated, instrumental
- comprehensive, robust, seamless

## Adverbs (-ly words)

Most -ly adverbs are filler. Delete or rephrase:

- really, just, literally, genuinely, honestly
- deeply, truly, fundamentally, essentially
- incredibly, remarkably, significantly
- interestingly, importantly, notably
- ultimately, arguably, undeniably
