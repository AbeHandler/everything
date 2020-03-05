aws s3 cp _site/mcmc/2019/11/01/why-does-metropolis-work.html s3://www.abehandler.com/mcmc/2019/11/01/why-does-metropolis-work.html --acl public-read --content-type text/html
aws s3 cp _site/em/2019/10/01/implementing-em-without-tears.html s3://www.abehandler.com/em/2019/10/01/implementing-em-without-tears.html --acl public-read --content-type text/html
aws s3 cp images s3://www.abehandler.com/images --recursive  --acl public-read
aws s3 cp _site/index.html s3://www.abehandler.com/index.html --acl public-read
aws s3 cp _site/css/style.css s3://www.abehandler.com/css/style.css
aws cloudfront create-invalidation --distribution-id E2NDQN6OXXN3XW --paths "/*"
