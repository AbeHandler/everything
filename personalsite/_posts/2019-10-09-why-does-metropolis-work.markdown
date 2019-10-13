---
layout: post
title:  "Why Metropolis works"
date:   2019-10-09 13:40:53 -0400
categories: mcmc 
---

### Why MCMC works

Markov Chain Monte Carlo ([MCMC](https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo)) methods can be easy to implement. If you've studied a  bit of machine learning, you might have coded a Gibbs sampler for a something like a mixture model or LDA. Because actual implementations can be fairly straightforward, it's possible to use MCMC for years before really understanding why it works. __This tutorial focuses on developing intuition for the basic idea underlying MCMC.__ [Other resources](https://www.cs.princeton.edu/courses/archive/spr06/cos598C/papers/AndrieuFreitasDoucetJordan2003.pdf) include far more techincal detail. However, I think it helps to see bigger picture first. 

Recall that MCMC allows you to learn properties of __any__ target posterior distribution, by drawing samples from the target $$p^*$$. I am going to focus on one particular MCMC method, the 
Metropolis algorithm, because it is often covered first when introducing MCMC (e.g. in [Murphy](https://www.cs.ubc.ca/~murphyk/MLbook/) or [mathematicalmonk](https://www.youtube.com/watch?v=gxHe9wAWuGQ))

Each iteration of Metropolis consists of two steps. In the first step, you make a proposal to move from state $$x$$ to state $$x’$$. You're allowed to pick any proposal distribution $$Q$$ that you want, so long as $$Q(x’\vert  x) = Q(x  \vert  x')$$ and so long as you have some chance of moving to all non-zero regions of  $$p^*$$. In the second step, you accept the proposal with a probability 
defined by this seemingly odd rule:  
<br>
<div class="text-center">
$$
r = min(1, \frac{p^*(x’)}{p(x)})
$$  
</div>


<br>

This procedure allow you to sample from *any* $$p^*$$. Why is that the case?



#### Sampling from a Markov chain


Let's ignore Metropolis for a minute and imagine that we have a <a href="https://www.youtube.com/watch?v=WUjt98HcHlk">Markov chain</a> with two states $$a$$ and $$b$$, where $$a$$ transitions to $$b$$ with probability 1 and $$b$$ transitions to $$a$$ with probability .5, and remains in $$b$$ with probability .5. Let $$T$$ denote the probability of transition from one state to another. For instance, in this case $$ T(a \vert b) $$ = .5 and $$T(b \vert a) = 1$$. Let $$\pi$$ denote the probability of being in some state in the chain, e.g. $$\pi(a)$$ is the probability of being in state $$a$$.  

One way to estimate $$\pi$$ is just to "run" the Markov chain for a number of steps (i.e. step through the chain, by sampling the next state) and observe often it spends in each state. This simple idea underlies _Markov Chain_ Monte Carlo methods, including the Metropolis algorithm. In MCMC, you define a Markov chain with a distribution over states equal to $$p^*$$. Then you just draw samples from the chain to estimate $$p^*$$.

Let's look at our simple example in Python. If we sample based on $$T$$, we find that $$\hat{\pi}(a) = .33$$ and $$\hat{\pi}(b) = .66$$, where $$\hat{\pi}$$ represents our estimate of $$\pi$$.

<script src="https://gist.github.com/AbeHandler/c55f9ebc5b3f681d1d35edfcfa1af9d8.js"></script>

#### How do we find a Markov chain?

The previous section explained how if we knew a $$T$$ with a $$\pi$$=$$p^*$$ we could just sample from $$T$$ to learn $$p^*$$. How do we find $$T$$? 

Informally, we need a $$T$$ such that if you kept drawing samples 

$$E_{x}[T(y|x)]=p^*(y)$$

#### If you have detailed balance, the distribution is stationary

In the previous example, $$T$$ was fixed and we “ran” the chain to estimate $$\pi$$, learning that $$\hat{\pi}(a) = 0.33$$ and $$\hat{\pi}(b) = 0.66$$.

Notice that these probabilities have an interesting property. $$\hat{\pi}(a)T(b \vert a)$$ = $$\hat{\pi}(b)T(a \vert b)$$ = $$.33 \cdot 1=0.66 \cdot .5$$. In other words, at any given time, the probability mass flowing out from state $$a$$ to state $$b$$ is the same as the probability mass flowing from $$b$$ to $$a$$. Using more formal terminology, because the probability mass flowing from each pair of states (in our example, there are only two) is equal, $$\hat{\pi}$$ is said to satisfy <a href="https://www.youtube.com/watch?v=xxDkdwQdGvs&t=314s">"detailed balance"</a> w.r.t $$T$$.

To me, it seems very intuitive that if some distribution $$\pi$$ respects detailed balance with respect to some $$T$$ then $$\pi$$ is a <a href="https://www.youtube.com/watch?v=tByUQbJdt14&list=PLD0F06AA0D2E8FFBA&index=143">stationary distribution</a>. This is because if the flow in and out of each state is equal, then the distribution over states will not change with time. For a more formal proof, and some other details that I am skipping (e.g. not all chains have stationary distributions, some chains have stationary distributions $$\pi$$ that do not satisfy detailed balance w.r.t to their $$T$$) see <a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Murphy chapter 17</a>. The upshot of all this is that if:

$$\pi(a)T(b \vert a) = \pi(b)T(a \vert b)$$ 

for all states $$a$$ and $$b$$ then this is sufficent to show that $$\pi$$ is a stationary distribution. 

With that said, let’s say we have Markov chain with a transition $$T$$ and a distribution $$\pi$$, where $$\pi$$ satisfies detailed balance with respect to $$T$$. If we draw samples $$X_1, X_2 … X_n \sim T$$ by sampling transitions between states, we should expect that the observed distribution $$\hat{\pi} \approx \pi$$. 

#### Seeking a Markov chain

Let's say we had a Markov chain with a stationary distribution $$\pi$$ equal to $$p^*$$, the target distribution. If we had a chain like this, then by sampling from the chain, we would sample $$p^*$$.  One way to find such a chain is to identify a $$T$$ such that 

$$p^*(a)T(b \vert a) = p^*(b)T(a \vert b)$$ 

for all $$a$$ and $$b$$.

Note that $$p^*(a)$$ and $$p^*(a)$$ are just ordinary probabilities fixed by our target distribution $$p^*$$. (They are fixed because we want to sample from, not modify, the target distribution). To make this fact more clear, let's write $$p^*(a)$$ as an ordinary scalar $$c_a$$ and $$ p^*(b)$$ as an ordinary scalar $$p_b$$. Our task is to find a $$T$$ such that 

$$c_a T(b \vert a) = c_b T(a \vert b)$$

for all $$a$$ and $$b$$.

Because there are two unknowns in this single equation (the transitions between each pair of states), there are many possible solutions. However, we are free to pick any $$T$$ we want — so long as $$c_a T(b \vert a) = c_b T(a \vert b)$$ and so long as any given transition $$T(\cdot \vert \cdot)$$ is a valid probability. 

One easy way to get a valid $$T$$ is to set $$T(b \vert a)=1$$ and solve for $$T(a \vert b)$$, or to set $$T(a \vert b)=1$$ and solve for $$T(a \vert b)$$. However, because any given $$T( \cdot \vert  \cdot)$$ has to be a valid probability, this actually limits which transition we can set to one. Let's look at each case:
<br>
- If $$p^*(b) > p^*(a)$$:

    - In this case, we must set $$T(b \vert a)$$=1. 
    - This is because, if $$T(b \vert a)$$ = 1 then $$c_a \cdot 1$$ = $$c_b T(a \vert b)$$ $$\Rightarrow T(a \vert b)$$ = $$c_a / c_b$$ = $$p^*(a) / p^*(b)$$.
    - If $$p^*(a) / p^*(b)$$ is greater than 1 because  $$p^*(a) > p^*(b)$$, then $$T(a \vert b)$$ would not be a valid probability.   
<br>
- If $$p^*(a) > p^*(b)$$: 

    - By the exact same reasoning, in this case, we must set $$T(a \vert b)$$=1.

We can express $$T$$ concisely as: 

- $$T(b \vert a)$$ = 1 if $$p^*(b) > p^*(a)$$ else $$c_b/c_a$$

- $$T(a \vert b)$$ = 1 if $$p^*(a) > p^*(b)$$ else $$c_a/c_b$$

If instead of a and b we can use names $$x$$ and $$x’$$, and we can replace the following 2 lines with a 1-liner

- $$T (x  \vert  x') = 1$$ if  $$p(x') > p(x)$$ else $$p^*(x')/p^*(x)$$

In other words, if $$x'$$ is bigger we transition with probability 1. Otherwise we transition with probability $$p^*(x')/p^*(x)$$, which we know is a number less than 1 (because $$p(x) > p(x’)$$), and also greater than 0 because both numbers are positive.

Another way to express this this same fact, we should transition from $$x$$ to $$x'$$ with probability 

<div class="text-center">
 $$min(1, *(x’)/p^*(x))$$
</div>

This is the mysterious $$r$$ from the Metropolis update algorithm. 

[2] I wonder if this is how MCMC was originally derived by the Metropolis authors, btw named Metropolis, Rosenbluth, Rosenbluth, Teller and Teller.
