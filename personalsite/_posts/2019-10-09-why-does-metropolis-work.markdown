---
layout: post
title:  "Why Metropolis works"
date:   2019-10-09 13:40:53 -0400
categories: mcmc 
---

### Why MCMC works

<p>Markov Chain Monte Carlo (<a href="https://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo">MCMC</a>) is a common tool for sampling from complex distributions. Because MCMC methods can be easy to implement, it’s possible to use them years without understanding the bigger picture. <strong>This tutorial focuses on developing intuition for the basic idea underlying MCMC.</strong> <a href="https://www.cs.princeton.edu/courses/archive/spr06/cos598C/papers/AndrieuFreitasDoucetJordan2003.pdf">Other resources</a> include more techincal detail if you get hooked.</p>

<p>In general, MCMC algorithms allow you to sample from <strong>any</strong> target distribution <script type="math/tex">p^*</script> via a sampling procedure. I'll focus on one simple MCMC method, the <a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Metropolis</a> <a href="https://www.youtube.com/watch?v=gxHe9wAWuGQ">algorithm</a>.</p>

<p>Each iteration of Metropolis consists of two steps. In the first step, you make a proposal to move from state <script type="math/tex">x</script> to state <script type="math/tex">x’</script>. You’re allowed to pick <u>any</u> proposal distribution <script type="math/tex">Q</script> that you want, so long as <script type="math/tex">Q(x’\vert  x) = Q(x  \vert  x')</script> and so long as you have some chance of moving to all non-zero regions of  <script type="math/tex">p^*</script>. In the second step, you accept the proposal with a probability 
defined by this seemingly odd rule:<br />
<br /></p>
<div class="text-center">
$$
r = min(1, \frac{p^*(x’)}{p^*(x)})
$$  
</div>

<p><br /></p>

<p>If you run this procedure long enough, you will begin to draw samples from <em>any</em> <script type="math/tex">p^*</script>. When I first learned about this I found it quite surprising, especially since you can pick (basically) any proposal you want.</p>

<p>Why does this work?</p>


#### Sampling from a Markov chain


Let's ignore Metropolis for a minute and imagine that we have a <a href="https://www.youtube.com/watch?v=WUjt98HcHlk">Markov chain</a> with two states $$a$$ and $$b$$, where $$a$$ transitions to $$b$$ with probability 1 and $$b$$ transitions to $$a$$ with probability .5, and $$b$$ remains in $$b$$ with probability .5. I'll use $$T$$ to denote the probability of transitioning from one state to another. For instance, in this case $$ T(a \vert b) $$ = .5, $$ T(b \vert b) $$ = .5 and $$T(b \vert a) = 1$$.

We can imagine that that if we "run" this Markov chain for many steps (i.e. keep sampling the next state), it will eventualy reach a <a href="https://www.youtube.com/watch?v=tByUQbJdt14&list=PLD0F06AA0D2E8FFBA&index=143">stationary</a> equillibrium, where on average it spends some of its time in state $$a$$ and some of its time in state $$b$$. 

I will use $$\pi$$ to denote the probability of being in some state in the stationary distribution, e.g. $$\pi(a)$$ is the probability of being in state $$a$$. One way to estimate $$\pi$$ is just to "run" the Markov chain for a number of steps (i.e. step through the chain, by sampling the next state) and observe often it spends in each state. For example, if we run <a href="https://gist.github.com/AbeHandler/c55f9ebc5b3f681d1d35edfcfa1af9d8">this Python code</a> to sample based on $$T$$, we will find that $$\hat{\pi}(a) = .33$$ and $$\hat{\pi}(b) = .66$$, where $$\hat{\pi}$$ represents our estimate of $$\pi$$.

This simple idea underlies _Markov Chain_ Monte Carlo methods, including the Metropolis algorithm. In MCMC, you define a Markov chain with a distribution over states $$\pi$$ that is equal to $$p^*$$. Then you just draw samples from the chain to estimate $$p^*$$.

#### How do we find the right $$T$$?

The previous section explained how we can sample from some transition $$T$$, in order to estimate some $$\pi$$. This only works if we can find a $$T$$ such that its stationary distribution $$\pi$$ will be equal to $$p^*$$, our target distribution. Expressed more mathematically, we need a $$T$$ such that 

$$E_{x \backsim p*}[T(y|x)]=p^*(y)=\pi(y)$$

which asserts that once $$T$$ is in its stationary distribution $$\pi$$, the probability of being in state $$y$$ is the same as $$p^*(y)$$, which is also the same as the probability of transitioning into state $$y$$ at any given timestep under the stationary distribution. 

<!--
#### If you have detailed balance, the distribution is stationary

In the previous example, $$T$$ was fixed and we “ran” the chain to estimate $$\pi$$, learning that $$\hat{\pi}(a) = 0.33$$ and $$\hat{\pi}(b) = 0.66$$.

Notice that these probabilities have an interesting property. $$\hat{\pi}(a)T(b \vert a)$$ = $$\hat{\pi}(b)T(a \vert b)$$ = $$.33 \cdot 1=0.66 \cdot .5$$. In other words, at any given time, the probability mass flowing out from state $$a$$ to state $$b$$ is the same as the probability mass flowing from $$b$$ to $$a$$. Using more formal terminology, because the probability mass flowing from each pair of states (in our example, there are only two) is equal, $$\hat{\pi}$$ is said to satisfy <a href="https://www.youtube.com/watch?v=xxDkdwQdGvs&t=314s">"detailed balance"</a> w.r.t $$T$$.

To me, it seems very intuitive that if some distribution $$\pi$$ respects detailed balance with respect to some $$T$$ then $$\pi$$ is a <a href="https://www.youtube.com/watch?v=tByUQbJdt14&list=PLD0F06AA0D2E8FFBA&index=143">stationary distribution</a>. This is because if the flow in and out of each state is equal, then the distribution over states will not change with time. For a more formal proof, and some other details that I am skipping (e.g. not all chains have stationary distributions, some chains have stationary distributions $$\pi$$ that do not satisfy detailed balance w.r.t to their $$T$$) see <a href="https://www.cs.ubc.ca/~murphyk/MLbook/">Murphy chapter 17</a>. The upshot of all this is that if:

$$\pi(a)T(b \vert a) = \pi(b)T(a \vert b)$$ 

for all states $$a$$ and $$b$$ then this is sufficent to show that $$\pi$$ is a stationary distribution. 

With that said, let’s say we have Markov chain with a transition $$T$$ and a distribution $$\pi$$, where $$\pi$$ satisfies detailed balance with respect to $$T$$. If we draw samples $$X_1, X_2 … X_n \sim T$$ by sampling transitions between states, we should expect that the observed distribution $$\hat{\pi} \approx \pi$$. 

#### Seeking a Markov chain

Let's say we had a Markov chain with a stationary distribution $$\pi$$ equal to $$p^*$$, the target distribution. If we had a chain like this, then by sampling from the chain, we would sample $$p^*$$.  
-->

One sufficient way to do so is to identify a $$T$$ where

$$p^*(a)T(b \vert a) = p^*(b)T(a \vert b)$$ 

for all states $$a$$ and $$b$$. This equation says that, for all $$a$$ and $$b$$, the probability mass flowing out from state $$a$$ to state $$b$$ is the same as the probability mass flowing from $$b$$ to $$a$$. When this occurs, $$p^*$$ is said to satisfy <a href="https://www.youtube.com/watch?v=xxDkdwQdGvs&t=314s">"detailed balance"</a>  with respect to $$T$$. It can be shown (and to me seems very inuitive) that some distribution satisfies detailed balance, it is stationary. If the probability mass going in to a given state is equal to the probability mass going out of a state, the distribution will never change.


#### Back to Metropolis

Recall the somewhat mysterious Metropolis update rule, in which you move from state $$x$$ to state $$x'$$ with probability

$$
r = min(1, \frac{p^*(x’)}{p^*(x)})
$$  

which produces a sample from $$p^*$$.

This equation makes a lot more sense if you recall that we are searching for a $$T$$ such that 

$$p^*(a)T(b \vert a) = p^*(b)T(a \vert b)$$

for all states $$a$$ and $$b$$. Because $$p^*$$ is what we are trying to sample from (and thus can't change), we need to define some $$T(b \vert a)$$ and $$T(a \vert b)$$ so that the equation is true for all $$a$$ and $$b$$. 


Let's rewrite the previous equation using the names $$x$$ and $$x'$$


$$p^*(x')T(x \vert x') = p^*(x)T(x' \vert x)$$


and rearrange to get 


$$\frac{p^*(x')}{p^*(x)} = \frac{T(x' \vert x)}{T(x \vert x')}$$


This is a single equation with two unknowns, so there is no single solution. However, we are free to pick any $$T$$ we want — so long as the equation holds and given transition $$T(\cdot \vert \cdot)$$ is a valid probability, between 0 and 1. 


Let's assume for now that $$p^*(x) > p^*(x')$$ and therefore $$\frac{p^*(x')}{p^*(x)}$$ is a valid probability. If we set $$T(x \vert x') = 1$$ we get $$\frac{T(x' \vert x)}{1} =  T(x' \vert x) = \frac{p^*(x')}{p^*(x)}$$, which will be a number between 0 and 1.


Now let's assume that $$p^*(x) < p^*(x')$$. If so $$\frac{p^*(x')}{p^*(x)}$$ will not be a valid probability, and so if we set $$T(x' \vert x) = 1$$ we will have 

$$\frac{p^*(x')}{p^*(x)} = \frac{1}{T(x \vert x')}$$

$$T(x \vert x') = \frac{p^*(x)}{p^*(x')}$$

In either case, we have $$T(a \vert b) = \frac{p^*(b)}{p^*(a)}$$ where $$p^*(a) > p^*(b)$$ and $$T(a \vert b)=1$$. 


<div class="col-xs-1" align="center">
<img src="https://s3.us-west-2.amazonaws.com/www.abehandler.com/images/Threshold.jpg">
</div>

I find it helpful to imagine this as a threshold function, like the one above. If $$p^*(x') > p^*(x)$$ then their ratio is a probability (the part of the graph that is climing) and we sample a transition from $$x$$ to $$x'$$ in proportion to their ratio. Otherwise, we transition from $$x$$ to $$x'$$ with probability one.

Another way to express all this, is that if we transition from $$x$$ to $$x'$$ with probability 

<div class="text-center">
 $$min(1, \frac{p^*(x’)}{p^*(x)})$$
</div>

we will eventually reach a stationary distribution with $$\pi=p^*$$.


#### Thanks

Thanks for <a href="https://twitter.com/JavierBurroni">Javier Burroni</a> for helping me better understand some of the mathematical details behind MCMC and to <a href="http://www.nickeubank.com/">Nick Eubank</a> for his help presenting the material in this post.