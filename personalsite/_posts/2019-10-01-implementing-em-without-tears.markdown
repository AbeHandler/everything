---
layout: post
title:  "Implementing EM without tears"
date:   2019-10-01 13:40:53 -0400
categories: EM 
---

### Implementing EM without tears
#### What to do when your EM code isn't working

There are many great [books](https://www.cs.ubc.ca/~murphyk/MLbook/), [lectures](https://www.youtube.com/watch?v=AnbiNaVp3eQ) and [tutorials](https://s3-us-west-2.amazonaws.com/www.abehandler.com/static/em-mixtures.pdf) on the EM algorithm. These materials often derive an E step and an M step for some mixture model (e.g. mixture of Gaussians), before offering a theoretical view of the procedure using Jensen's inequality and KL divergence. These tutorials are great. But in order to *really* understand EM, you'll have to code an implementation yourself. This step is non-trivial: if you are still learning the math, it can be hard to spot bugs when your implementation doesn't work.


**This tutorial focuses on EM in code, instead of in latex.** I will list some debugging strategies to verify and troubleshoot your implementation of EM. 

#### Assert is your friend

In general, implementing ML algorithms can be tricky. Unlike some other programming contexts (e.g. updating a database), the inputs, initialization and steps of an ML algorithm usually aren't deterministic. This can make it hard to spot and fix bugs.

One good way to implement ML algorithms (including EM) is to:
1. identify the theoretical guarantees underlying the method (understand what each step does)
2. use assert statements to make sure that your implementation matches the guarantees
 
This tutorial goes into the details of how to do step one for the EM algorithm. Step two is just a matter of adding asserts.

#### Are your expected complete log likelihood and observed data log likelihood functions correct?
When implementing EM, I think it's helpful to code the expected complete data log likelihood and observed data log likelihood functions at the very start of the process. Murphy Chapter 11 describes what these are. I'd recommend implementing these two functions for your model before doing *anything* else. (The exact mathematical form will vary, depending on your model).  

Implementing these functions might *seem* like a straightforward task of translating latex into matrix operations using some linear algebra package, such as numpy. But this step is surprisingly easy to bungle. I screwed it up recently and it added days of debugging work. Make sure these functions are perfectly correct or your implementation will fail.

#### Does your observed data log likelihood increase monotonically after each iteration? 
EM guarantees that your observed data LL will increase after each E step and M step. Chapter 11 of Kevin Murphy's Machine Learning textbook includes a proof. If your observed data LL is not increasing monotonically (i.e. sometimes takes a step away from zero), you have a bug. Use assert to verify this!

#### Does your M step actually optimize your expected data log likelihood? 
The M step of EM resets the parameters \theta so that they maximize the expected data log likelihood (according to the expectation at a given timestep). If $\theta^t$ are the parameters at the start of the M step and  $\theta^{t + 1}$ are the parameters at the end of the M step, make sure $Q(\theta^{t + 1}) >= Q(\theta^{t})$. The M step should optimize the lower bound $Q$ w.r.t $\theta$. Again, assert if your friend.

#### Can you recover true parameters averaging over multiple runs with simulated data?
One good way to verify your EM implementation (for a generative model) is to set some true parameters (e.g. known mixture proportions and distributions for a mixture of multinomials), generate data based on those parameters and then see how well your estimated parameters recover the true parameters.    

Remember that when you generate data from the true parameters you'll get a noisy sample from the true distribution. For instance, if you are drawing from a 1-D Gaussian, the mean of your sample might be 1.1 and the true mean might be 1. Your model might learn the right parameters for your sample (e.g. estimate a mean of 1.1) and thus deviate from the true parameters.    

To get around this issue, my friend [Javier](https://twitter.com/JavierBurroni) suggested fitting a model multiple times, using multiple draws from the true parameters. In general, as you make more draws and keep fitting the model, the KL divergence between the true parameters and the average learned parameters (across runs of the model) should decrease. If you see this, it is evidence that your implementation works.  

#### Is your expected complete log likelihood always less than your observed data log likelihood?
EM guarantees that the expected complete log likelihood is less than or equal to the observed data log likelihood. This material is explained using Jensen’s inequality in most tutorials that provide a theoretical view of EM. When you implement, verify that the expected complete log likelihood is less or equal to than the observed data log likelihood. If not, you have a bug. 

#### Does your implementation work with different random seeds?

Debugging probabilistic algorithms can be hard, because bugs may appear and disappear depending on different draws and random data or different random configurations of the parameters. For debugging, it can sometimes be helpful to set a random seed, so that you can observe the exact same behavior each time you run your program. However, *it is important to turn off the random seed when you are done* to make sure that your random seed is not masking other bugs in your implementation.


#### Is np.allclose hiding bugs?

If you are coding in Python, as you add assert statements, you might find that they are failing for values that are very close together (e.g. assert 2.21 * 10-10 == 2.22 * 10-10). It might be tempting to use np.allclose to get around this issue. But make sure you understand how this function works. If you are comparing large and small numbers it can behave unexpectedly.  
 

For instance, if you are expecting f(x)=1 (but you get f(x)=10!), you would probably say that your program has a bug. But `np.allclose([1e-8], [1e-9])` will return `True`, even though 1e-8 is also 10 times bigger. A good rule of thumb: if you are skipping an assert statement b/c of allclose print out a warning to verify the method is doing what you think it is doing. 

#### Do you have numerical underflow or overflow?
Computing expectations and maximizations often involves computing the probability of rare events, particularly for natural language processing models (most words are rare). This can cause numerical underflow. This is described in many other places (e.g. [Jurafsky and Martin](https://web.stanford.edu/~jurafsky/slp3/)), so I will just mention it briefly here.

