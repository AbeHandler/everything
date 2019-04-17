In statistics, the ``odds'' are a ratio $\frac{p}{q}$, where $q = 1-p$ and $p$ is a probability. If there is an 80\% chance it will rain, then the odds of rain are $\frac{.8}{.2}$ = $4:1$. The logit function is the log of the odds, i.e. logit($p$) = log($\frac{p}{1-p}$).

If $Y_i \in \{0,1\}$ the logistic regression model asserts that $p_i \triangleq p(Y_i = 1 | X = x)$ = $\frac{e^{\bm{w} \cdot \bm{x}}}{1 + e^{\bm{w} \cdot \bm{x}}}$, where $\bm{w}$ is a learned vector of weights and $\bm{x}$ is a vector of features. A function of the form $\frac{e^{A}}{1  +e^A}$ is called the logistic function. Another way of defining logistic regression is logit($p_i$) =  $\bm{w} \cdot \bm{x}$. We can see that this definition is equivalent by defining $A =  \bm{w} \cdot \bm{x}$, so $p(y = 1) = \frac{A}{1 + A}$. By definition

\begin{align}
\text{logit} (p_i) &= \frac{\frac{A}{1 + A}}{1 - \frac{A}{1 + A}} \\
                         &=  \frac{A}{1 + A - A} \\ 
                         &= A \\ 
                         &=  \bm{w} \cdot \bm{x}
\end{align}