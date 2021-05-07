#### Intro

The normalizer of the Dirichlet distribution includes the gamma function $\Gamma(x)$. Textbooks often describe the gamma function as a ``generalization of the factorial function''. But based on the definition 

$$
\Gamma(x) \triangleq \int^{\infty}_0 t^{x- 1}e^{-1} dt
$$

it is not clear why this is so. [This](https://www.youtube.com/watch?v=XZIVrkkYBRI) great video clarifies.

#### Product rule for derivatives

Recall the product rule for derivatives:  $(pq)' = p'q + q'p$. If we integrate both sides we have 

$$
\int^{\infty}_0(pq)' = \int^{\infty}_0p'q + \int^{\infty}_0q'p
$$  (1)

which can be rearranged to 


$$
pq - \int^{\infty}_0q'p = \int^{\infty}_0p'q 
$$  (2)

and then

$$
\int^{\infty}_0p'q = pq - \int^{\infty}_0q'p
$$  (3)

to arrive at the formula for integration by parts.


#### Gamma function as generalization of factorial 

By definition 

$$
\Gamma(x + 1) = \int^{\infty}_0 t^{x + 1 -1}e^{-1} dt = \int^{\infty}_0 t^{x}e^{-1} dt
$$ (4)

which we can use to show the connection to the factorial function by evaluating the integral. 

Let $q=t^x$ and $p'$ = $e^{-t}$. Then $q'$ = $x t ^{x-1}$ and $p$ = $-e^{-t}$ because $\frac{d}{dx} (-e^{-t})$ = $\frac{d}{dx} (-t) * - e^{-t}$ = $\frac{d}{dx} (-1) * - e^{-t}$ = $e^{-t}$. Substituting these definitions, $pq$ = $-e^{-t}t^x$. 

Applying these definitions and plugging in to (3) we have 

$$
\int^{\infty}_0 t^{x}e^{-1} dt = pq - \int^{\infty}_0 q' p = [-e^{-t}t^x]^{\infty}_0 - \int_{0}^{\infty}x t ^{x-1} (-e^{-t})dt
$$ (5)

which can be written as

$$
\int^{\infty}_0 t^{x}e^{-1} dt = pq - \int^{\infty}_0 q' p = [-e^{-t}t^x]^{\infty}_0  + x\int_{0}^{\infty} t ^{x-1} (e^{-t})dt
$$ (5) 

because a constant -x can be pulled out from the integral.

Because the first term tends to zero we have 

$$
\int^{\infty}_0 t^{x}e^{-1} dt = pq - \int^{\infty}_0 q' p = x\int_{0}^{\infty} t ^{x-1} (e^{-t})dt
$$ (5)

Thus, $\Gamma(x + 1)=x\Gamma(x)$ noting the definition of $\Gamma(x)$.

#### Putting it together 

Let $x$ = $n-1$. We know that $\Gamma(x)= x\Gamma(x)$. Filling in $n-1$ we have 

$$\Gamma(n-1 + 1)= \Gamma(n) = (n-1)\Gamma(n-1)$$

By the same logic let $x=n-2$ and we have 

$$\Gamma(n-1)= (n-2)\Gamma(n-2)$$

Or we say that  $x=n-3$ and we have 

$$\Gamma(n-2)= (n-3)\Gamma(n-3)$$ 

If we keep applying this rule we have 

$$\Gamma(n)= (n-1)(n-2)(n-3)(n-4).... $$ 

Thus the $\Gamma$ is a generalization of the factorial.