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

#### Sample from a Markov chain to learn its distribution over states


Let's ignore Metropolis for a minute and imagine that we have a <a href="https://www.youtube.com/watch?v=WUjt98HcHlk">Markov chain</a> with two states $$a$$ and $$b$$, where $$a$$ transitions to $$b$$ with probability 1 and $$b$$ transitions to $$a$$ with probability .5, and remains in $$b$$ with probability .5. I am going to use the notation $$T$$ to denote the probability of transition from one state to another. For instance, in this case $$ T(a \vert b) $$ = .5 and $$T(b \vert a) = 1$$. I am going to use the notation $$\pi$$ to denote the probability of being in some state in the chain, e.g. $$\pi(a)$$ is the probability of being in state $$a$$.  

One way to learn $$\pi$$ (i.e. how long some chain spends in each state) is just to "run" the Markov chain for a number of steps (i.e. step through the chain, by sampling the next state) and observe often it spends in each state in order to get an estimated distribution over states $$\hat{\pi}$$. This simple idea underlies the Metropolis algorithm.

Here's that same idea in Python. If we run the code, we see that $$\hat{\pi}(a) = .33$$ and $$\hat{\pi}(b) = .66$$.

<script src="https://gist.github.com/AbeHandler/c55f9ebc5b3f681d1d35edfcfa1af9d8.js"></script>

#### If you have detailed balance, the distribution is stationary

In the previous example, $$T$$ was fixed and we “ran” the chain to estimate $$\pi$$, learning that $$\hat{\pi}(a) = 0.33$$ and $$\hat{\pi}(b) = 0.66$$.

Notice that these probabilities have an interesting property. $$\hat{\pi}(a)T(b \vert a)$$ = $$\hat{\pi}(b)T(a \vert b)$$ = $$.33 \cdot 1=0.66 \cdot .5$$. In other words, at any given time, the probability mass flowing out from state $$a$$ to state $$b$$ is the same as the probability mass flowing from $$b$$ to $$a$$. Because the probability mass flowing in and out from $$a$$ to $$b$$ is equal, if we keep sampling from this chain our $$\hat{\pi}$$ would not change. 

Using more formal terminology, we can say that $$\hat{\pi}$$ is a good approximation of the <a href="https://www.youtube.com/watch?v=tByUQbJdt14&list=PLD0F06AA0D2E8FFBA&index=143">stationary distribution</a>, the distribution over states that occurs if you keep running the Markov chain. Moreover, because the probability mass flowing from each pair of states (in our example, there are only two) is equal, our system $$\hat{\pi}$$ is said to satisfy <a href="https://www.youtube.com/watch?v=xxDkdwQdGvs&t=314s">"detailed balance"</a> w.r.t $$T$$.

To me, it seems very intuitive that $$\pi$$ respects detailed balance with respect to some $$T$$ then the chain a stationary distribution, because if the flow in and out of each state is equal, then the distribution over states will not change with time. For a more formal proof, and some other details that I am skipping (e.g. not all chains have stationary distributions, some stationary distributions do not have detailed balance) see <a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Murphy chapter 17</a>. The upshot of all this is that if:

$$\pi(a)T(b \vert a) = \pi(b)T(a \vert b)$$ 

for all states $$a$$ and $$b$$ then $$\pi$$ is a stationary distribution. 

With that said, let’s define a Markov chain *slightly* more formally as a tuple $$(\pi, T)$$ where $$\pi$$ satisfies detailed balance with respect to $$T$$. Because of detailed balance, if we draw samples $$X_1, X_2 … X_n \sim MC(\pi, T)$$ by “running the chain", we should expect that $$\hat{\pi} \approx \pi$$. 

#### Seeking a Markov chain, finding Metropolis

Let's say we had a Markov chain $$(\pi, T)$$ with a stationary distribution $$\pi$$ equal to $$p^*$$, the target distribution. If we had a chain like this, then by sampling from the chain, we would sample $$p^*$$.  Using our notation, we would write this as $$MC(\pi=p^*, T)$$, where we'd need some $$T$$ such that 

$$p^*(a)T(b \vert a) = p^*(b)T(a \vert b)$$ 

for all $$a$$ and $$b$$.

Note that $$p^*(a)$$ and $$p^*(a)$$ are just ordinary probabilities fixed by our target distribution $$p^*$$. Even if it takes a really long time to find $$p^*(a)$$ and $$p^*(b)$$ we could still compute each quantity. To make this fact more clear, let's write $$p^*(a)$$ as an ordinary scalar $$c_a$$ and $$ p^*(b)$$ as an ordinary scalar $$p_b$$. Our task is to find a $$T$$ such that 

$$c_a T(b \vert a) = c_b T(a \vert b)$$

for all $$a$$ and $$b$$.

Because there are two unknowns in this equation (per pair of states), we can’t just “solve” for both T terms. There are many possible solutions. However, we are free to pick any $$T$$ we want — so long as $$c_a T(b \vert a) = c_b T(a \vert b)$$ and so long as any given transition $$T(\cdot \vert \cdot)$$ is a valid probability. 

One easy choice is to set $$T(b \vert a)=1$$ and solve for $$T(a \vert b)$$, or vice versa. [2]

Because any given $$T( \cdot \vert  \cdot)$$ has to be a valid probability, this actually limits which transition we can set to one. Let’s look at the two possible cases (ignoring ties):

- If $$p^*(b) > p^*(a)$$

    - In this case, we must set $$T(b \vert a)$$=1. This is because, if $$T(b \vert a)$$ = 1 then $$c_a \cdot 1$$ = $$c_b T(a \vert b)$$ $$\Rightarrow T(a \vert b)$$ = $$c_a / c_b$$ = $$p^*(a) / p^*(b)$$. If $$p^*(a) / p^*(b)$$ is greater than 1 (because  $$p^*(a) > p^*(b)$$) then $$T(a \vert b)$$ would not be a valid probability. 

- If p(a) > p(b) 

    - By the exact same reasoning, in this case, we must set $$T(a \vert b)$$=1.

We can express $$T$$ concisely as: 

$$T(b \vert a)$$ = 1 if p(b) > p(a) else c_b/c_a$$
$$T(a \vert b)$$ = 1 if p(a) > p(b) else c_a/c_b$$

If instead of a and b we can use names $$x$$ and $$x’$$, and we can replace the following 2 lines with a 1-liner

$$T (x  \vert  x') = 1$$ if  $$p(x') > p(x)$$ else $$p^*(x')/p^*(x)$$

In other words, if $$x'$$ is bigger we transition with probability 1. Otherwise we transition with probability $$p^*(x')/p^*(x)$$, which we know is a number less than 1 (because $$p(x) > p(x’)$$), and also greater than 0 because both numbers are positive.

Another way to express this this same fact, we should transition from $$x$$ to $$x'$$ with probability => min$$(1, *(x’)/p^*(x))$$

This is the mysterious $$r$$ from the Metropolis update algorithm. 

[2] I wonder if this is how MCMC was originally derived by the Metropolis authors, btw named Metropolis, Rosenbluth, Rosenbluth, Teller and Teller.
