---
layout: post
title:  "Geometric intuition for Monte Carlo Integration"
date:   2020-11-22 13:40:53-0400
categories: sampling 
---

Monte Carlo integration allows you to calculate the area under a curve via samples with a computer, without analytically deriving the value with math. This is helpful because some integrals are hard to solve with pen and paper. Wasserman's All of Statistics presents Monte Carlo integration by deriving the following expression: 

$\hat{I} \defeq \frac{1}{N} \Sigma^N_{i=0} (b-a) f(x_i)$

Reading Wasserman, I could always follow the derivation (I include it at the end of this post for reference) but had trouble developing deeper geometric intuitions. This post presents an informal and visual perspective to build intuition, inspired by <a href="https://www.youtube.com/watch?v=FnJqaIESC2s">3blue1brown</a>. See other <a href="http://people.duke.edu/~ccc14/sta-663-2019/notebook/S14D_Monte_Carlo_Integration.html">posts</a> for a more formal presentation.

We begin by rearranging the expression for $\hat{I}$. We multiply each $f(x_i)$ by the constant $(b-a)$ so we can pull out $(b-a)$ to get:

$\hat{I} = \frac{1}{N} \Sigma^N_{i=0}(b-a)f(x_i) = (b-a) \frac{1}{N} \Sigma^N_{i=0} f(x_u)$

When you arrange the equation this way, it reads as if the the approximate integral $\hat{I}$ is equal to the average height of $f(x)$ (i.e. $\frac{1}{N} \Sigma^N_{i=0} f(x)$) times the width of the interval (i.e. $(b-a)$). This expression seems to type check, as an area is a width times a height and integrals are areas under curves. 

Let's look at this expression in more detail. First, let's say we sample $f(x)$$N$ times. Visually, that means at each step, we will get $N$ 1-dimensional values for $f$ at points $x_1$ to $x_N$. 

[diagram 1]

We might want to use these samples to estimate the integral, by making $N-1$ rectangles with height equal to $f(x)$ and width equal to $x_{i+1} - x_{i}$ where $x_i$ is some point in the sample and $x_{i + 1}$ is the next largest point in the sample. Let's call this width $dx_i$. We can show our visual approximation like this:

[diagram 2]

And write it with math like this

$\hat{I} \approx \Sigma^N_{i=0} dx_1*f_1(x) + dx_2*f_2(x)  + dx_3*f_3(x)  + dx_4*f_4(x) ...  dx_N*f_N(x)$

In general, as you take more and more samples, the distance between samples will become small. At a certain point, all of the distances will really little and we can just approximate the width of each rectangle with the same small value $dx$.  If we assume all of the dx are (roughly) the same size, we can rewrite the expression above without the subscripts on the the $dx$ factors. This seems a little hand-wavey, but remember that our initial expression was an approximation. This is (slightly less precise) approximation.

$\hat{I} \approx \Sigma^N_{i=0} dx*f_1(x) + dx*f_2(x)  + dx*f_3(x)  + dx*f_4(x) ...  dx*f_N(x)$

Recall that when taking an integral $dx$ stands for some very small interval along the $x-axis$. In our case, what is the length of the interval $dx$? Well roughly if we take $N$ samples, and assume that in general the samples are evenly distributed so that the distances between each sample are roughly similar, we should expect $dx \approx (b-a)/N$ because the interval $(b-a)$ is split into $N$ small regions. Similarly, the interval $(b-a)$ is equal to $N$ segments of roughly length $dx$. 

Let's go back to our expression. 

$\hat{I} \approx \Sigma^N_{i=0} dx*f_1(x) + dx*f_2(x)  + dx*f_3(x)  + dx*f_4(x) ...  dx*f_N(x)$

Assuming that the two samples are ordered, we can pull out two smallest rectangles from the sum, and replace them with $2dx$ times their average height, where the average height is $\frac{f_1(x) + dx*f_2(x)}{2}$. Hence our expression becomes 

$\hat{I} \approx 2*dx*\frac{f_1(x) + dx*f_2(x)}{2}  + dx*f_3(x)  + dx*f_4(x) ...  dx*f_N(x)$

We can show this visually as follows. 

[diagram]

In the same way, we could also imagine pulling out another rectangle and averaging it with the first two, to get: 

[diagram] 

Which can be expressed in math as 3 times the average hight of the first three rectangles times the rest. 

If we keep going like this for all N rectangles we eventually get an expression $Ndx \Sigma^N_{i=0} f(x)/N$

Well, what is $N dx$? It is the width $dx$ repeated $N$ times which is roughly the length of our interval, i.e. (b-a).

So we have:

$\hat{I} \approx (b-a) \Sigma^N_{i=0} \frac{f(x)}{N}$

We can interpret a Monte Carlo integral as the average height of a function over a given interval, times the width of the interval.

#### H5 Another symbolic interpretation

Consider again the equation: 

$\hat{I} \approx (b-a) \Sigma^N_{i=0} \frac{f(x)}{N}  \approx N dx \Sigma^N_{i=0} \frac{f(x)}{N}$ 

Note that in this expression, each $f(x)$ is divided by $N$. So we can also rearrange this expression by pulling out the fraction $\frac{1}{N}$ to get 

$\hat{I} \approx dx N \frac{1}{N} \Sigma^N_{i=0}f(x)$

The $N$ terms cancel so we have:

$\hat{I} \approx dx \Sigma^N_{i=0}f(x)$

If we push in the $dx$ term (recall this is some small constant) we have:

$\hat{I} \approx \Sigma^N_{i=0} f(x) dx$, which is very close to the definition of a continuous integral.