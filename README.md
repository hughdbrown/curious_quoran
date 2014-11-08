#The Curious Quoran
==============

A cross-resource recommendation engine for Quora users, discovering hidden gems of interest on [Coursera](https://coursera.org), [Khan Academy](https://www.khanacademy.org/), [iTunes Podcast](https://www.apple.com/itunes/podcasts/discover/), LibGen and [Project Gutenberg](https://www.gutenberg.org/) ebook repositories.


#### Motivation & Inspiration


For many of us, [Quora](http://www.quora.com) is a beloved online repository of knowledge - a virtual meetingplace for hungry minds. True to its tagline, Quora often provides *"The best answer to any question"* on topics from Hinduism to horticulture, democratizing the knowledge, stories and intellectual resources of some of the most interesting and accomplished people in the world - public figures whose names you know ([Jimmy Wales!](http://www.quora.com/Jimmy-Wales) [Sheryl Sandberg!](http://www.quora.com/Sheryl-Sandberg)) and many others you may not.

My work is motivated by frequently asked Quora questions of the form: "*How / where can I learn more about ____*"; my goal is to augment the endogenous functionality of Quora's Stack Exchange-esque question and answer format by identifying latent user interests and recommending a curated set of resources among the following: 

1. Project Gutenberg ebook repository
2. Khan Academy lessons
3. Coursera courses
4. iTunes podcasts

...thereby empowering autodidacts and curious individuals to continue their education free of charge.


#### Getting started

The first step was to obtain the data that feeds the engine: the data from a user's Quora profile page, which has questions asked and answers upvoted. Scraping Quora was a bit tricky: the function I wrote takes needs your first and last name, username and password and uses the Chrome webdriver in Python's `selenium` library to navigate to the page and log in with your information. 

Stumbling block: Quora generates content with AJAX, so I needed to use `selenium`'s' webdriver to execute a bit of JavaScript to scroll to the bottom of the page. The functions in `quora_scrape.py` return a full list of questions followed and asked from the user's *entire* history! I consider this aggregate a snapshot of a Quoran's curiosities and will now use it for latent topic extraction and to generate top recommendations from external resources.


#### Getting data from Khan Academy  (<= how do I turn this into a link to another readme?)

Many of my targeted users want to deepen their understanding of a topic - overwhelmingly, Quora users seem to want explanations of various topics in layman's terms. I can't think of a better resource for this than Khan Academy, whose wonderful maxim empowers you to *"learn anything - for free, for everyone, forever"*. Fortunately, I'm the beneficiary of KA's *very* user-friendly and well-documented [API](http://api-explorer.khanacademy.org/).

Want to use the topictree API and grab a composite of slug, description, title and keywords.

#### Data from Project Gutenberg's Bibliographic Records

Use author, dates, loc class, subject tags, 

PG doesn't want to be scraped, but gives you [access to bibrecs](http://www.gutenberg.org/feeds/catalog.rdf.bz2) for the entire corpus of works in the repository. 

UPDATE: I found an incredibly useful PostGres dump with better metadata and richer descriptions than I could have hoped for. Much cleaner than parsing through the XML and trying to filter for English texts!

Collecting subject tags, title and author into a composite description yields what I hope will be a complete and verbose enough description to generate sensible recommendations. Gutenberg's raw catalog was an unwieldy RDF file with over 46,000 entries. I decided to dump the file into SQL and filter by works downloaded from the site at least 10,000 times. I got lucky here -- the BibRecs on PG are concise but informative (e.g. Shakespeare's *Othello* is tagged with the following: jealousy, interracial marriage, Muslims, Venice (Italy) and English Literature) 


Aside: the real challenge of this project is to recommend slight variations of the things users have asked about. Could add an extension for meetups in the city the user lives in. Given your Quora curiosities (quoriosities?): what should you do, read, hear, see? Need clever featurization for cross-platform resources 


Stanford topic modeling visualizer
Look, listen, read

#### Podcast Data

Getting semantically-rich descriptions for podcasts took a fair bit of work, but thanks to the FeedWrangler [API](https://feedwrangler.net/developers/podcasts_directory#show) I was able to get the top fifty most popular and scrape the episode feed urls to retrieve salient descriptions of the most recent episodes. This worked surprisingly well, especially for domain-specific podcasts rich in jargon-y summaries, like Accidental Tech Podcast, NPR Planet Money or Freakonomics Radio.


#### Extending functionality to recommend resources for individual question pages

TBD

Yet another curated reading list of short stories: http://recommendedreading.tumblr.com/rss

