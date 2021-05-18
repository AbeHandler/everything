options(jupyter.plot_mimetypes = "image/png")

options(warn=-1, message =-1)
library(dplyr); library(ggplot2); library(rstan); library(reshape2)
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

dgp_string <- "
functions {
    /**
   * Return draws from a mixture of gaussians with means mu and std=1 and
   * mixing parameter theta

   * @param mu A vector of J means
   * @param theta A J-dimensional simplex
   * @param N Number of draws
   * @return Return an N-vector of draws from the model.
   */

    vector sample_normal_rng(vector mu, vector theta, int N) {
      vector[N] z;
      int j[rows(theta)];
      for (n in 1:N){
        j = multinomial_rng(theta, 1);
        for(i in 1:rows(theta)){
          if (j[i] == 1){
              z[n] = normal_rng(mu[i], 1.0);
          }
        }
      }
      return z;
    }
}
data {
 // If we were estimating a model, we'd define the data inputs here
}
parameters {
  // ... and the parameters we want to estimate would go in here
}
model {
  // This is where the probability model we want to estimate would go
}
"

compiled_function <- stan_model(model_code = dgp_string)

expose_stan_functions(compiled_function)