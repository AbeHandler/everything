class RougeScorer(object):

    '''
    https://www.aclweb.org/anthology/W04-1013.pdf

    Here we assume there is a single reference summary
    '''

    def __init__(self, reference):
        assert type(reference) == list
        assert [type(o) == 'unicode' for o in reference]
        self.reference = reference

    def getRougeN(self, summary, N):

        assert type(summary) == list
        assert N > 0
        assert type(N) == int

        '''http://www.locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/'''
        def find_ngrams(input_list, n):
            return zip(*[input_list[i:] for i in range(n)])

        ng_summary = list(find_ngrams(summary, n=N))

        ng_reference = list(find_ngrams(self.reference, n=N))

        overlap = sum(1 for i in ng_summary if i in ng_reference)
        total = sum(1 for i in ng_reference)
        return overlap/total


if __name__ == "__main__":
    rs = RougeScorer(["hi", "there"])
    assert (rs.getRougeN(["hi"], N=1)) == .5
    assert (rs.getRougeN(["hi"], N=2)) == 0.0
    assert (rs.getRougeN(["hi", "there"], N=2)) == 1.0

    rs = RougeScorer(["hi", "there", "bob", "jones"])
    assert (rs.getRougeN(["hi", "there"], N=2)) == 1/3
