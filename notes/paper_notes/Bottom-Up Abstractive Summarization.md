#### Bottom-Up Abstractive Summarization
- Gehrmann, Deng, Rush
- EMNLP 2018

##### Basic idea

- Neural abstractive summarization, but with a two-stage pipeline. First select content. Then generate based on that content. 

- Better ROUGE results on benchmark datasets

- Claims this is better for domain adaptation. This seems interesting. You could give a model some pieces and ask it to generate based on those constraints. Maybe you know that there are some things that are important in your domain and you want a news style statement about that domain, using your suggested content. The abstractive headline generation models a la Rush (2015) require so much data. 

##### Modeling

- Paired input output $(\mathcal{X}, \mathcal{Y})$ where $x\in \mathcal{X}, y \in \mathcal{Y}$ are sequences of input output tokens.

- Run a content selection module to get $q_i$, the probability that the word is selected. Details in section 4.1. 

- Set the attention $p(\alpha_j^{~i}| x_i, y_{1:j-1})$ if $q_i > \epsilon$ and 0 otherwise, applying some form of normalization to ensure it is a valid distribution.

- Following See and Manning's pointer generator model, they set the copy probabilty to the sum of the attention over the unit. In the See and Manning framework, $p(w) = p_{gen}P(w) - (1 - p_{gen})\sum_{1:w_i}a_t^t$. What Rush & coauthors are doing is I think zeroing out some of the input sequence based on $q_i$.

- In section 5 they discuss adding a length and repeat penalty for inference. These might be a bit hacky. I would be curious to see how they change results.

- They do some domain transfer results from CNN to NYT corpus. This is a very lightweight form of domain transfer I think. I am not sure how convincing this is really. It would be interesting to see this w/ far different domains. But I think it is an interesting aspsect of the model.

##### Other notes

- Related: Chris Kedzie, EMNLP context selection