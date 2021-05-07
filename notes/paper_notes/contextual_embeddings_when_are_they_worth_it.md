Contextual embeddings, when are they worth it?

Simran Arora et al
May, Zhang and Re

Chris Re group

Paper that examines when Bert embeddings are worth it. They compare best to simpler models like glove and also a cool idea of random embeddings. Jo variable for all of these is how much memory you need versus how good your performance is. They compare on a ner dash on o somethi else and find that as you add training data you get closer to best. They also quantify I thank ambiguity sparseness iirc and see that BERT is better on more ambiguous and novel language.

The really cool thing from this paper I think is the random embeddings. Prior work has them too but this was new to me. You just initialize the vector randomly and update. It sounds lie need to all you need to stare in memory is the seed.

https://www.youtube.com/watch?v=bCPeg0Tp64s