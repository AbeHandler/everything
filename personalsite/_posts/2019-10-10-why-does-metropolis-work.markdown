---
layout: post
title:  "Why does Metropolis work?"
date:   2019-10-01 13:40:53 -0400
c_ategories: MCMC 
---


The first time I learned about the Metropolis algorithm, I found it quite mysterious. Metropolis allows you to sample from *any* complex target distribution $p*(x)$, by making a proposal to move from state $x$ to state $x’$ with probability $Q(x’ | x)$, and accepting the proposal with a probability defined by this seeming odd rule: 

$$
r = min(1, \frac{p*(x’)}{p(x)}
$$

You're allowed to pick any $Q$ you want so long the $Q$ is symmetric (i.e. $Q(x’ | x) = Q(x | x’)$) and has some chance of moving to all non-zero regions of the target distribution (note: an extension of the algorithm, Metropolis-Hastings, allows an asymmetric $Q$). 

When learning about Metropolis as a 1st-year PhD student, this whole procedure seemed very confusing. Why should this allow me to sample from *any* p I want?

#### Sampling from a Markov chain

Let’s ignore Metropolis for a minute and imagine that we have a Markov chain (see tutorial) with two states A and B, where A transitions to B with probability 1 and B transitions to A with probability .5, and remains in B with probability .5.

I am going to use the notation T to denote the transition from one state to another. For instance, in this c_ase $T(a|b)$ = .5, meaning state B transitions to state A with probability .5. I am going to use the notation pi to denote the probability of being in some state in the markov chain, e.g. \pi(a) is the probability of being in state A. 

One way to learn pi (i.e. how long this chain spends in A and B) is simply to “run” the Markov chain for a number of steps (i.e. step through the chain, by sampling the next state) and observing how often you spend in A and B. After executing this procedure, you’ll have a distribution over states A and B, denoted \hat{\pi}. This simple idea underlies the Metropolis algorithm. 

Here is a python implementation. If we run the code, we see that p(a) = .33 and p(b) = .66. 

<script src="https://gist.github.com/AbeHandler/c55f9ebc5b3f681d1d35edfcfa1af9d8.js"></script>

#### Detailed balance

In the previous example, T was fixed and we “ran” the chain to estimate $pi$, learning that pi(a) = 0.33 and pi(b) = 0.66.

Notice that these probabilities have an interesting property. p(a) = 0.33 * $T(b|a)$ = 1 == .33 == p(b) * $T(a|b)$ = 0.66 * .5. In other words, at any given timestep, the probability mass flowing out from state a to state b is the same as the probability mass flowing from b to a. Bec_ause the probability mass flowing in and out from a to b is equal, if we keep sampling from this chain our $hat{pi}$ would not change. 

Using more formal terminology, we c_an say that our $hat{pi}$ is a very, very close approximation of the stationary distribution of the markov chain. Moreover, bec_ause the probability mass flowing from each pair of states (in our c_ase, there are only two) is equal, our system \pi and T is also said to satisfy “detailed balance”. [Math monk]. 

To me, it seems very intuitive that if a Markov Chain has detailed balance then it is in a stationary distribution. If the flow in and out of each state is equal, then the distribution over states will not change. For a more formal proof, and some other details that I am skipping (e.g. not all chains have stationary distributions, some stationary distributions do not have detailed balance) see Murphy chapter 17.

The upshot of all this is that

pi(a)$T(b|a)$ = pi(b)$T(a|b)$ 

for all states a and b then pi is a stationary distribution. 

With that said, let’s define a Markov chain *slightly* more formally as a tuple, (pi, T) where \pi satisfies detailed balance w.r.t T. Bec_ause of detailed balance, if we draw samples X_1, X_2 … X_n \sim MC(pi, T) by “running the chain", we should expect that \hat{pi} \approx pi. 

#### The Metropolis algorithm

The Metropolis algorithm “works” by creating a Markov chain with a stationary distribution \pi equal to p*, the target distribution. By running the chain, we sample from \pi and thus sample from p*. 

How c_an we create this Markov chain? Based on our previous definition, we need some MC(\pi, T) s.t. \pi = p* and s.t. p* satisfies detailed balance w.r.t T. What if you did not have detailed balance? You’d just have to wait longer eh?

In other words, we need some p* and T such that

$$p*(a)$T(b|a)$ = p*(b)$T(a|b)$$$

for all a and b. 

Note that in this case p*(a) and p*(b) are fixed bec_ause p* is not anything we c_an control. In fact, p* is what we are trying to sample from in the first place!  To emphasize this point, let’s try replacing these terms with fixed constants c_a and c_b. While it might take us a long time to compute c_a and c_b, in principle, they are ordinary probabilities and we could compute them with enough time. With such constants, we c_an restate our goal as finding a T s.t.

$$
c_a $T(b|a)$ = c_b $T(a|b)$
$$

Bec_ause $$T(a|b)$$ and $T(b|a)$ are free variables, this is a single equation with two unknowns so we c_an’t just “solve” for both T terms. (There are many possible solutions.) However, we are free to pick any T we want for $T(b|a)$ or $T(a|b)$ — so long as c_a $$T(b|a)$$ = c_b $$T(a|b)$$. One easy choice is to set $T(b|a)$ and solve for $T(a|b)$, or vice versa. [1]

Which one should we pick to set to 1: $T(a|b)$ or $T(b|a)$? Bec_ause any given T(. | .) has to be a valid probability, we don’t really have a choice. Let’s look at the two possible c_ases.  

If p(b) > p(a)

In this c_ase, we must set $T(b|a)$=1. This is bec_ause, setting $T(b|a)$ =1 means that $T(a|b)$ = c_a / c_b

$T(b|a)$ = 1 => $c_a * 1$ = $c_b T(a|b)$ => $T(a|b)$ = $c_a / c_b$

If c_a / c_b is greater than 1 then $T(a|b)$ would not be a valid probability. 

If p(a) > p(b) 

By the exact same reasoning, in this c_ase, we must set $T(a|b)$=1. This is bec_ause, setting $T(a|b)$ =1 means that $T(a|b)$ = c_b / c_a

We c_an express T concisely as: 

$T(b|a)$ = 1 if p(b) > p(a) else c_b/c_a
$T(a|b)$ = 1 if p(a) > p(b) else c_a/c_b

If instead of a and b we c_an use names x and x’, and we c_an replace the following 2 lines with a 1-liner

T (x | x’) = 1 if  p(x') > p(x) else p*(x')/p*(x) 

In other words, if x’ is bigger we transition with probability 1. Otherwise we transition with probability p*(x')/p*(x), which we know is a number less than 1 (bec_ause p(x) > p(x’)), and also greater than 0 bec_ause both numbers are positive.

Another way to express this this same fact, we should transition from x to x’ with probability => min(1, *(x’)/p*(x))

This is the mysterious r from the Metropolis update algorithm. 

[1] I wonder if this is how MCMC was originally derived by the Metropolis authors, btw named Metropolis, Rosenbluth, Rosenbluth, Teller and Teller.