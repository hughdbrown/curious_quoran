#The Curious Quoran
==============

A cross-resource recommendation engine for Quora users, discovering hidden gems of interest on [Coursera](https://coursera.org), [iTunes Podcast](https://www.apple.com/itunes/podcasts/discover/) and [Project Gutenberg](https://www.gutenberg.org/).


#### Motivation & Inspiration

For many of us, [Quora](http://www.quora.com) is a beloved online repository of knowledge - a virtual meetingplace for hungry minds. True to its tagline, Quora often provides *"The best answer to any question"* on topics from Hinduism to horticulture, democratizing the knowledge, stories and intellectual resources of some of the most interesting and accomplished people in the world - public figures whose names you know ([Jimmy Wales!](http://www.quora.com/Jimmy-Wales) [Sheryl Sandberg!](http://www.quora.com/Sheryl-Sandberg)) among hundreds of thousands of others you may not.

Motivated by "gateway" questions of the form: "*How can I learn more about _____*", my goal is to augment the endogenous functionality of Quora's Stack Exchange-esque question and answer format by identifying latent user interests and recommending a curated set of resources from among the following: 

1. Project Gutenberg ebook repository (40,000 free downloadable ebooks)
2. Coursera (~800 free online courses)
3. iTunes podcasts (250,000+, available free via iTunes Podcast Store)

...thereby empowering autodidacts and curious individuals to continue their education at no cost.

#### Getting started

The first step was to obtain the data that feeds the engine: raw text from a user's Quora profile page, which has questions asked and answers upvoted. Scraping Quora was a bit tricky: the function I wrote takes needs your first and last name, username and password and uses the headless PhantomJS webdriver in Python's `selenium` library to navigate to the page and log in with your information. 

Stumbling block: Quora generates content with AJAX, so I needed to use the `selenium` webdriver to execute a bit of JavaScript to scroll to the bottom of the page, wait for new content to appear, then scroll further and repeat ad infinitum. The functions in `quora_scrape.py` return a full list of questions followed and asked from the user's *entire* history.

#### Data from Project Gutenberg's Bibliographic Records

I constructed features for Project Gutenberg ebooks by aggregating subject tags, titles and authors. I was lucky enough to stumble upon a PostGres SQL dump of the entire PG catalog (far less unwieldy than the original XML/RDF file) and ended up filtering to exclude works not in English. I was also the beneficiary of Gutenberg's bibliographic records, which are concise but informative (e.g. Shakespeare's *Othello* is tagged with the following: jealousy, interracial marriage, Muslims, Venice (Italy) and English Literature), and turned out to yield sufficiently verbose descriptions for sensible recommendations.

#### Podcast Data

Extracting semantically-rich descriptions for podcasts took a fair bit of work, but thanks to the FeedWrangler [API](https://feedwrangler.net/developers/podcasts_directory#show) I was able to get the top fifty most popular and scrape the episode feed urls to retrieve salient text for the most recent episodes. This worked surprisingly well, especially for very niche, domain-specific podcasts steeped in jargon, like Accidental Tech Podcast, NPR Planet Money or Freakonomics Radio.

#### Coursera Data

Coursera course features were the simplest - I collected concatenated course titles and descriptive text using the API.  

#### Extending the functionality

Once I had the pipeline in place, adding new resources (like curated writing from [Longform](http://longform.org) and changing the user profile or question page was a trivial matter.  

### Why is this more sophisticated than a search engine?

You might wonder why this is worth the trouble of aggregation and lexical analysis when it seems like a Google search could yield similar results, but as evidenced by the test "case studies," I found that in tapping into Quora discourse, this tool leverages a user history not easily conveyed by simply plugging a phrase into a search engine. 


#### Feature engineering: the secret sauce

Creativity in feature engineering is the crux of this project: once a document is transformed into vector space with TF-IDF weighting, I needed to "magnify" latent interests so that cosine similarity would yield optimal results. If a followed question was tagged with a topic that was previously followed (e.g. a question about sentiment analysis tagged with NLP, which was followed independently as a topic previously), that question was weighted more heavily, since the user demonstrated a deeper interest in that topic.

Worth mentioning is a quick but import fix for preventing overfitting to documents of a certain length: I needed to perform regularization (dividing by the L2 norm of TF-IDF vectors) to eliminate bias toward longer documents with more words. 

