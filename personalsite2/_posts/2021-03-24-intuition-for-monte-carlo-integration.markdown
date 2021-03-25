---
layout: post
title:  "Geometric intuition for Monte Carlo Integration"
date:   2020-11-22 13:40:53-0400
categories: sampling 
---

Monte Carlo integration allows you to calculate the area under a curve via samples with a computer, without analytically deriving the value with math. This is helpful because some integrals are hard to solve with pen and paper. Wasserman's <a href="https://www.stat.cmu.edu/~larry/all-of-statistics/">All of Statistics</a> presents Monte Carlo integration by deriving the following expression for $$\hat{I}$$, the estimated integral: 

$$\hat{I} \triangleq \frac{1}{N} \Sigma^N_{i=0} (b-a) f(x_i)$$

Reading Wasserman, I could always follow the derivation (I include it at the end of this post for reference) but had trouble developing deeper geometric intuitions. This post presents an informal and visual perspective to build intuition, inspired by <a href="https://www.youtube.com/watch?v=FnJqaIESC2s">3blue1brown</a>. See other <a href="http://people.duke.edu/~ccc14/sta-663-2019/notebook/S14D_Monte_Carlo_Integration.html">posts</a> for a more formal presentation.

To build intuition, begin by recalling that integrals are areas under a curve, and rearranging the expression for $$\hat{I}$$ by pulling out the constant $$(b-a)$$ like this:

$$ \hat{I} \triangleq (b-a) \frac{1}{N} \Sigma^N_{i=0} f(x_i)$$ 

Let's look at this expression in more detail. We can interpret $$\frac{1}{N}\Sigma^N_{i=0} f(x_i)$$ term by imagining that we are compute the height of the function height $$f(x_i)$$ at some (uniformly) random $$x_i$$ a total of $$N$$ times, and then take the average to get the average function height. Visually, that means at each step, we will get $$N$$ different 1-dimensional values for $$f$$ at points $$x_1$$ to $$x_N$$, and take their average. 

<img class="img-fluid z-depth-1 rounded" src="/assets/img/diagram1.jpg">

The expression then says that to approximate the interval, we multiply the mean height by the width of the interval (i.e. $$(b-a)$$). Thus we can write the expression as follows as equation \#1: 

$$\begin{equation}\hat{I} \triangleq \underbrace{(b-a)}_\text{Interval width} \underbrace{1/N * \Sigma^N_{i=0} f(x_u)}_\text{Average height}\tag{1}\end{equation}$$

And we can imagine things visually like this:

<img class="img-fluid z-depth-1 rounded" src="/assets/img/diagram2.jpg">

Things are a little more intuitive now, because an area is a height times a width, and integrals are areas under curves. But it not super clear *why* multiplying the mean height times the interval width should approximate the interval.

#### Why is the area given by equation \#1 a good approximation for the integral?

We might want to use these samples to estimate the integral, by making $$N-1$$ rectangles with height equal to $$f(x)$$ and width equal to $$x_{i+1} - x_{i}$$ where $$x_i$$ is some point in the sample and $$x_{i + 1}$$ is the next largest point in the sample. Let's call this width $$dx_i$$. We can show our visual approximation like this:

[diagram 2]

And write it with math like this, where I change $$\triangleq$$ to $$\approx$$ to emphasize that we have an approximation:

$$ I \approx \Sigma^N_{i=0} dx_1*f_1(x) + dx_2*f_2(x)  + dx_3*f_3(x)  + dx_4*f_4(x) ...  dx_N*f_N(x)$$

In general, as you take more and more samples, the distance between samples will become small. At a certain point, all of the distances will really little and we can just approximate the width of each rectangle with the same small value $$dx\approx (b-a)/N$$, because the interval $$(b-a)$$ is split into $$N$$ small regions of length $$dx$$. 

If we assume all of the dx are (roughly) the same size, we can rewrite the expression above without the subscripts on the the $$dx$$ factors. This seems a little hand-wavey, but remember that our initial expression was just an approximation. By removing the subscripts, we now have another (less precise) approximation.

$$ I \approx \Sigma^N_{i=0} dx*f_1(x) + dx*f_2(x)  + dx*f_3(x)  + dx*f_4(x) ...  dx*f_N(x)$$

Assuming that the two samples are ordered, we can pull out two smallest rectangles from the sum, and replace them with $$2dx$$ times their average height, where the average height is $$\frac{f_1(x) + dx*f_2(x)}{2}$$. Hence our expression becomes 

$$\hat{I} \approx 2*dx*\frac{f_1(x) + dx*f_2(x)}{2}  + dx*f_3(x)  + dx*f_4(x) ...  dx*f_N(x)$$

We can show this visually as follows. 

[diagram]

In the same way, we could also imagine pulling out another rectangle and averaging it with the first two, to get: 

[diagram] 

Which can be expressed in math as 3 times the average hight of the first three rectangles times the rest. 

If we keep going like this for all N rectangles we eventually get an expression $$Ndx \Sigma^N_{i=0} f(x)/N$$

Well, what is $$N dx$$? It is the width $$dx$$ repeated $$N$$ times which is roughly the length of our interval, i.e. (b-a).

So we have:

$$\hat{I} \approx (b-a) \Sigma^N_{i=0} \frac{f(x)}{N}$$

We can interpret a Monte Carlo integral as the average height of a function over a given interval, times the width of the interval.

#### Another symbolic interpretation

Consider again the equation: 

$$\hat{I} \approx (b-a) \Sigma^N_{i=0} \frac{f(x)}{N}  \approx N dx \Sigma^N_{i=0} \frac{f(x)}{N}$$ 

Note that in this expression, each $$f(x)$$ is divided by $$N$$. So we can also rearrange this expression by pulling out the fraction $$\frac{1}{N}$$ to get 

$$\hat{I} \approx dx N \frac{1}{N} \Sigma^N_{i=0}f(x)$$

The $$N$$ terms cancel so we have:

$$\hat{I} \approx dx \Sigma^N_{i=0}f(x)$$

If we push in the $$dx$$ term (recall this is some small constant) we have:

$$\hat{I} \approx \Sigma^N_{i=0} f(x) dx$$

which is very close to the definition of a continuous integral.