openssl enc -aes-256-cbc -salt -in $1 -out $1.enc -iter 10000 -kfile /Users/abramhandler/.ssh/id_rsa 
