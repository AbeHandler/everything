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

incorrect_model <- "
data {
  int N; // number of observations
  vector[N] y; //outcome vector
}

parameters {
  real mu; 
  real sigma;
}

model {

  //prior
  mu ~ normal(0, 5);
  sigma ~ normal(0, 10);
  
  // The likelihood
  y ~ normal(mu, sigma);

}
generated quantities {
  // For model comparison, we'll want to keep the likelihood contribution of each point
  // We will also generate posterior predictive draws (yhat) for each data point. These will be elaborated on below. 
  
  vector[N] log_lik;
  vector[N] y_sim;
  for(i in 1:N){
    log_lik[i] = normal_log(y[i], mu, sigma);
    y_sim[i] = normal_rng(mu, sigma);
  }
}
"

compiled_function <- stan_model(model_code = dgp_string)

expose_stan_functions(compiled_function)

mus = c(-10, 10)

N = 1000

y_sim = sample_normal_rng(mus, theta, N)

df = data_frame(y_sim = y_sim)

p <- ggplot(df, aes( x = y_sim)) + geom_histogram(bins=30) + ggtitle("Simulated data")

data_list_2 <- list(N = N, y = y_sim)

incorrect_fit <- stan(model_code = incorrect_model, data = data_list_2, cores = 1, chains = 2, iter = 2000)