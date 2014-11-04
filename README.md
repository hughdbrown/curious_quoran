#The Curious Quoran
==============

A cross-resource recommendation engine for Quora users, discovering hidden gems of interest on Coursera, Khan Academy, iTunes Podcast, LibGen and Project Gutenberg ebook repositories.


#### Motivation & Inspiration


For many of us, Quora is a beloved online repository of knowledge - a virtual meetingplace for hungry minds. True to its tagline, Quora often provides *"The best answer to any question"* on topics from Hinduism to horticulture. Quora democratizes the knowledge, stories and intellectual resources of some of the most interesting and accomplished people in the world - public figures whose names you know (Jimmy Wales! Sheryl Sandberg!) but many others you may not.

My work is motivated by frequently asked Quora questions of the form: "*How / where can I learn more about ____*"; my goal is to augment the endogenous functionality of Quora's Stack Exchange-esque question and answer format by identifying latent user interests and recommending a curated set of resources among the following: 

1. Project Gutenberg ebook repository
2. Khan Academy lessons
3. Coursera courses
4. iTunes podcasts

...thereby empowering autodidacts and curious individuals to continue their education free of charge.


#### Getting started

The first step was to obtain the data that feeds the engine: the data from a user's Quora profile page, which has questions asked and answers upvoted. Scraping Quora was a bit tricky: the function I wrote takes needs your first and last name, username and password and uses the Chrome webdriver in Python's selenium library to navigate to the page and log in with your information. 

Stumbling block: Quora generates content with AJAX, so I needed to use the `selenium` webdriver to execute a bit of JavaScript to scroll through the page. The functions in `quora_scrape.py` return a full list of questions followed and asked from the user's *entire* history!


#### Getting data from Khan Academy  (how do I turn this into a link to another readme?)

Many of my targeted users want to deepen their understanding of a topic - overwhelmingly, Quora users seem to want explanations of various topics in layman's terms. I can't think of a better resource for this than Khan Academy. Fortunately, I'm the beneficiary of KA's *very* user-friendly and well-documented [API](api-explorer.khanacademy.org/api/v1)

Want to use the topictree API and grab a composite of slug, description, title and keywords.



