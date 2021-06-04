---
layout: post
title:  "Data science self-study resources"
date:   2021-04-28 13:40:53-0400
categories: self-study 
---

Many CU INFO majors ask me for resources for studying data science on their own. Here is a list of some of my favorites. I've broken up this list into resources focused on [underlying math](#math-and-stats), [machine learning concepts](#machine-learning-concepts), and [programming](#programming-and-tools). I also include a section for students interested in [natural language processing](#nlp-resources).

### Underlying math

Data science is based on math and statistics, so it makes sense to spend time continually deepening your understanding of these fundamental ideas. Also, while the field will change all the time, the underlying quantitative concepts will remain consistent. 

While more math is always helpful, when you are starting out, I would recommend making sure you are comfortable with the fundamentals of calculus, statistics and linear algebra. Here are a few resources I have found helpful.

- **[3blue1brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)** is an AMAZING math YouTuber. I learn a ton from his videos, and am inspired by the quality of his teaching. I also leaned on videos from **[mathematicalmonk](https://www.youtube.com/channel/UCcAtD_VYwcYwVbTdvArsm7w)** to build my quantitative background during my first year in grad school. There are tons of math YouTubers, and I suggest poking around to find a teaching style that works for you. 

- Wasserman's **[All of Statistics](http://www.stat.cmu.edu/~larry/all-of-statistics/)** is a great book that focuses on offering a terse and rigorous introduction to statistics. It will be a challenge to get started with this resource, but you will learn a lot if you put in the effort. (I think the title is a little bit of a joke. All of statistics can not fit in one book, but it is a good start.) 

- Zico Kolter has a good **[quick start](https://www.cs.cmu.edu/~zkolter/course/15-884/linalg-review.pdf)** for linear algebra. I have not found a full linear algebra textbook I really like yet. (I've used books from Gilbert Strang and David Poole.)

- I really like the book **[Computer Age Statistical Inference](https://web.stanford.edu/~hastie/CASI/)** to give an overall modern perspective on the history of stats, but I would not start with this resource.

### Machine learning concepts

Machine learning is either [the same thing](https://stats.stackexchange.com/questions/6/the-two-cultures-statistics-vs-machine-learning) as statistics or somehow closely-related to statistics, depending on your perspective. Here are a few books to get started, more focused on ML.

- Packt's **[Python Machine Learning](https://www.packtpub.com/product/python-machine-learning-third-edition/9781789955750)** (PML). This is the textbook for INFO 4604/5604. It offers a nice hands-on introduction to ML, with a focus on using and understanding Python ML libraries.  

- Kevin Murphy's **[Machine Learning](https://probml.github.io/pml-book/book0.html)**. This is a standard graduate textbook in ML. It is much harder than Python Machine Learning (PML) and you will need to put in a lot of effort to get comfortable with the contents. (I came to grad school with a limited math background, and it took me around 6 months to get to the point where I could read Murphy). But the book offers a much deeper perspective on the field than you will get from PML. If you are serious about understanding the underlying details of machine learning, you will need to spend time working through resources with some mathematical depth. You don’t need to read every chapter in this book at once. Give yourself years to learn the material.

### Programming and tools

There are tens if not hundreds of thousands of books, tutorials and online courses for learning how to code. Someone even made a [game](https://vim-adventures.com/) that teaches you to use the Vim text editor. With that said, here are a few scattered thoughts on how to navigate the landscape. 

- **Basic stuff to learn.** Tools and languages change all the time, and I am not sure it makes too much sense to get too focused on any particular technology of framework. However, you will need to show some fluency with current tools to get started in your career. It is a good idea to learn how to use **[PyTorch](https://pytorch.org/)** or **[tensorflow](https://www.tensorflow.org/)**, as well as to be comfortable with **[SQL](https://www.w3schools.com/sql/)**, **[numpy](https://numpy.org/)**, **[pandas](https://pandas.pydata.org/)** and **[scikit-learn](https://scikit-learn.org/stable/)**. I love the **[tidyverse](https://www.tidyverse.org/)** for exploratory data analysis for small datasets (it's a collection of R packages), and some people like **[Julia](https://julialang.org/)** for writing faster code (Python can be slow). **[Altair](https://altair-viz.github.io/)** is nice for data visualization in Python, but there are many competitors like **[matplotlib](https://matplotlib.org/)**. It's a good idea to get the hang of using **[GitHub](https://github.com/)**, and to be comfortable using the command line. There is an MIT course that focuses on filling in these sorts of **[programming-adjacent skills](https://missing.csail.mit.edu/)**,  with free materials posted online.

- **Where to focus your effort.** There are so many tools and languages to learn, it can be hard to know where to focus. I can think of at least two strategies:
    1. One good option is to just **follow your own curiosity**. Learn what you want to learn to answer the kinds of questions you want to answer and take on the kinds of projects you'd like to complete! 

    2. Alternately, I also think it also makes sense to **be a bit analytic** about what you study first. The **[programmer competency matrix](https://web.archive.org/web/20210417182641/https://sijinjoseph.com/programmer-competency-matrix/)** helped me a lot when I started working as a software developer without a CS degree. What I like about it is you can sort of see where you land on this matrix, and systematically fill gaps in your background. Of course, if you are interested in a particular role or job, definitely speak with people in that area to understand what you need to know.

### NLP resources

If you are interested in natural language processing specifically, I recommend **[Jacob Eisenstein's textbook](https://mitpress.mit.edu/books/introduction-natural-language-processing)**. If you don't want to buy a copy, you can download [the original lecture notes from GitHub](https://github.com/jacobeisenstein/gt-nlp-class/blob/master/notes/eisenstein-nlp-notes.pdf). You should also probably learn to use the **[spacy](https://spacy.io/)** and **[Hugging Face Transformers](https://huggingface.co/transformers/)** libraries.
