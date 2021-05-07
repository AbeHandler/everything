aws s3 cp _site/2020/02/04/news-indexes.html s3://www.abehandler.com/2020/02/04/news-indexes.html --acl public-read --content-type text/html
aws s3 cp _site/mcmc/2019/11/01/why-does-metropolis-work.html s3://www.abehandler.com/mcmc/2019/11/01/why-does-metropolis-work.html --acl public-read --content-type text/html
aws s3 cp _site/mcmc/2019/10/09/why-does-metropolis-work.html s3://www.abehandler.com/mcmc/2019/10/09/why-does-metropolis-work.html --acl public-read --content-type text/html
aws s3 cp _site/teaching/2019/10/01/an-easy-system-for-committing-solutions-to-GitHub.html s3://www.abehandler.com/teaching/2019/10/01/an-easy-system-for-committing-solutions-to-GitHub.html --acl public-read --content-type text/html
aws s3 cp _site/em/2019/10/01/implementing-em-without-tears.html s3://www.abehandler.com/em/2019/10/01/implementing-em-without-tears.html --acl public-read --content-type text/html
aws s3 cp _site/syntax/lstms/2018/05/15/assessing_the_abililty_of_lstms.html s3://www.abehandler.com/syntax/lstms/2018/05/15/assessing_the_abililty_of_lstms.html --acl public-read --content-type text/html
aws s3 cp _site/acceptability/linguistics/2018/01/26/grammaticality_acceptability_probability.html s3://www.abehandler.com/acceptability/linguistics/2018/01/26/grammaticality_acceptability_probability.html --acl public-read --content-type text/html
aws s3 cp _site/formalisms/mt/2018/01/15/quasi-synchronous_grammars.html s3://www.abehandler.com/formalisms/mt/2018/01/15/quasi-synchronous_grammars.html --acl public-read --content-type text/html
aws s3 cp _site/summarization/compression/2018/01/11/sentence-redution-for-automatic-text-summarization.html s3://www.abehandler.com/summarization/compression/2018/01/11/sentence-redution-for-automatic-text-summarization.html --acl public-read --content-type text/html
aws s3 cp _site/summarization/neuralnets/2018/01/10/neural-summarization-by-extracting-sentences-and-words.html s3://www.abehandler.com/summarization/neuralnets/2018/01/10/neural-summarization-by-extracting-sentences-and-words.html --acl public-read --content-type text/html
aws s3 cp images s3://www.abehandler.com/images --recursive  --acl public-read
aws s3 cp _site/index.html s3://www.abehandler.com/index.html --acl public-read
aws cloudfront create-invalidation --distribution-id E2NDQN6OXXN3XW --paths "/*"
