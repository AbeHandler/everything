---
layout: post
title:  "Why Metropolis works"
date:   2019-10-09 13:40:53 -0400
categories: mcmc 
---

### Why Metropolis works

The first time I learned about the 
<a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Metropolis</a> <a href="https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm">algorithm</a>, I found it quite mysterious. Metropolis allows you to sample from *any* complex target distribution $$p^*(x)$$, by making a proposal to move from state $$x$$ to state $$x’$$ and accepting the proposal with a probability 
defined by this seemingly odd rule:  
<br>
<div class="text-center">
$$
r = min(1, \frac{p^*(x’)}{p(x)})
$$  
</div>
<br>
You're allowed to pick any proposal distribution $$Q$$, so long as $$Q(x’\vert  x) = Q(x  \vert  x')$$ [1]. **Why does this procedure allow you to sample from *any* p?**

<div class="text-secondary" style="color:grey;font-size:15px">
[1] Note: An extension, Metropolis-Hastings, drops this requirement. In either case, the proposal must have some chance of moving to all non-zero regions of the target distribution.
</div>

#### Sampling from a Markov chain


Let's ignore Metropolis for a minute and imagine that we have a <a href="https://www.youtube.com/watch?v=WUjt98HcHlk">Markov chain</a> with two states $$a$$ and $$b$$, where $$a$$ transitions to $$b$$ with probability 1 and $$b$$ transitions to $$a$$ with probability .5, and remains in $$b$$ with probability .5. I am going to use the notation $$T$$ to denote the probability of transition from one state to another. For instance, in this case $$ T(a \vert b) $$ = .5, meaning state $$b$$ transitions to state $$a$$ with probability $$.5$$. 

I am going to use the notation $$\pi$$ to denote the probability of being in some state in the markov chain, e.g. $$\pi(a)$$ is the probability of being in state a.  

One way to learn $$\pi$$ (i.e. how long this chain spends in $$a$$ and $$b$$) is simply to “run” the Markov chain for a number of steps (i.e. step through the chain, by sampling the next state) and observing how often you spend in $$a$$ and $$b$$. After executing this procedure, you’ll have a distribution over states $$a$$ and $$b$$, denoted $$\hat{\pi}$$. This simple idea underlies the Metropolis algorithm.

Here is a Python implementation. If we run the code, we see that $$\hat{\pi}(a) = .33$$ and $$\hat{\pi}(b) = .66$$.

<script src="https://gist.github.com/AbeHandler/c55f9ebc5b3f681d1d35edfcfa1af9d8.js"></script>

#### Detailed balance

In the previous example, $$T$$ was fixed and we “ran” the chain to estimate $$\pi$$, learning that $$\hat{\pi}(a) = 0.33$$ and $$\hat{\pi}(b) = 0.66$$.

Notice that these probabilities have an interesting property. $$\hat{\pi}(a)T(b \vert a)$$ = $$\hat{\pi}(b)T(a \vert b)$$ = $$.33 \cdot 1=0.66 \cdot .5$$. In other words, at any given time, the probability mass flowing out from state $$a$$ to state $$b$$ is the same as the probability mass flowing from $$b$$ to $$a$$. Because the probability mass flowing in and out from $$a$$ to $$b$$ is equal, if we keep sampling from this chain our $$\hat{\pi}$$ would not change. 

Using more formal terminology, we can say that our $$\hat{\pi}$$ is a very, very close approximation of the <a href="https://www.youtube.com/watch?v=tByUQbJdt14&list=PLD0F06AA0D2E8FFBA&index=143">stationary distribution</a> of the Markov Chain. Moreover, because the probability mass flowing from each pair of states (in our example, there are only two) is equal, our system $$\pi$$ and $$T$$ is also said to satisfy <a href="https://www.youtube.com/watch?v=xxDkdwQdGvs&t=314s">"detailed balance"</a>.

To me, it seems very intuitive that if a Markov Chain has detailed balance then it is in a stationary distribution, because if the flow in and out of each state is equal, then the distribution over states will not change. For a more formal proof, and some other details that I am skipping (e.g. not all chains have stationary distributions, some stationary distributions do not have detailed balance) see <a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Murphy chapter 17</a>. The upshot of all this is that if:

$$\pi(a)T(b \vert a) = \pi(b)T(a \vert b)$$ 

for all states $$a$$ and $$b$$ then $$\pi$$ is a stationary distribution. 

With that said, let’s define a Markov chain *slightly* more formally as a tuple $$(\pi, T)$$ where $$\pi$$ satisfies detailed balance with respect to $$T$$. Because of detailed balance, if we draw samples $$X_1, X_2 … X_n \sim MC(\pi, T)$$ by “running the chain", we should expect that $$\hat{\pi} \approx \pi$$. 

#### The Metropolis algorithm

The Metropolis algorithm “works” by creating a Markov chain $$(\pi, T)$$ with a stationary distribution $$\pi$$ equal to $$p^*$$, the target distribution. By running the chain, we sample from $$\pi$$ and thus sample from $$p^*$$. 

How can we create this Markov chain? Based on our previous definition, we need some $$MC(\pi, T)$$ such that $$\pi$$ = $$p^*$$ and $$p^*$$ satisfies detailed balance with resepect to $$T$$.  

Question: What if you did not have detailed balance? You’d just have to wait longer eh?

In other words, we need some $$p^*$$ and $$T$$ such that $$p^*(a)T(b \vert a) = p^*(b)T(a \vert b)$$ for all a and b.  


Note that in this case $$p^*(a)$$ and $$p^*(b)$$ are fixed because $$p^*$$ is not anything we can control. In fact, $$p^*$$ is what we are trying to sample from in the first place!  To emphasize this point, let’s try replacing these terms with fixed constants $$c_a$$ and $$c_b$$. While it might take us a long time to compute $$c_a$$ and $$c_b$$, in principle, they are ordinary probabilities and we could compute them with enough time. With such constants, we can restate our goal as finding a $$T$$ such that   
$$
c_a $$T(b \vert a)$$ = c_b $$T(a \vert b)$$
$$   
Because $$T(a \vert b)$$ and $$T(b \vert a)$$ are free variables, this is a single equation with two unknowns so we can’t just “solve” for both T terms. (There are many possible solutions.) However, we are free to pick any T we want for $$T(b \vert a)$$ or $$T(a \vert b)$$ — so long as c_a $$T(b \vert a)$$ = c_b $$T(a \vert b)$$. One easy choice is to set $$T(b \vert a)$$ and solve for $$T(a \vert b)$$, or vice versa. [2]

Which one should we pick to set to 1: $$T(a \vert b)$$ or $$T(b \vert a)$$? Because any given $$T( \cdot \vert  \cdot)$$ has to be a valid probability, we don’t really have a choice. Let’s look at the two possible cases.  

If p(b) > p(a)

In this case, we must set $$T(b \vert a)$$=1. This is bec_ause, setting $$T(b \vert a)$$ =1 means that $$T(a \vert b)$$ = c_a / c_b

$$T(b \vert a)$$ = 1 => $$c_a * 1$$ = $$c_b T(a \vert b)$$ => $$T(a \vert b)$$ = $$c_a / c_b$$

If c_a / c_b is greater than 1 then $$T(a \vert b)$$ would not be a valid probability. 

If p(a) > p(b) 

By the exact same reasoning, in this case, we must set $$T(a \vert b)$$=1. This is bec_ause, setting $$T(a \vert b)$$ =1 means that $$T(a \vert b) = c_b / c_a $$

We can express $$T$$ concisely as: 

$$T(b \vert a)$$ = 1 if p(b) > p(a) else c_b/c_a$$
$$T(a \vert b)$$ = 1 if p(a) > p(b) else c_a/c_b$$

If instead of a and b we can use names $$x$$ and $$x’$$, and we can replace the following 2 lines with a 1-liner

$$T (x  \vert  x') = 1$$ if  $$p(x') > p(x)$$ else $$p^*(x')/p^*(x)$$

In other words, if $$x'$$ is bigger we transition with probability 1. Otherwise we transition with probability $$p^*(x')/p^*(x)$$, which we know is a number less than 1 (because $$p(x) > p(x’)$$), and also greater than 0 because both numbers are positive.

Another way to express this this same fact, we should transition from $$x$$ to $$x'$$ with probability => min$$(1, *(x’)/p^*(x))$$

This is the mysterious $$r$$ from the Metropolis update algorithm. 

[2] I wonder if this is how MCMC was originally derived by the Metropolis authors, btw named Metropolis, Rosenbluth, Rosenbluth, Teller and Teller.
