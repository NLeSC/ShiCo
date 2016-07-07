### Boost method
Method used to determine the weight given to words produced, before the aggregation step. Two methods are available:

 - Sum similarity -- this method uses the similarity (between the seed word and each word) to determine the weight. The similarities are added for each word, as each word can appear in the results of different seed terms.
 - Counts -- count the number of times a word appears as the result of a seed term.
