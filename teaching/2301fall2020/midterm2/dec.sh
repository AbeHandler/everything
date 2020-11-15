echo $1
openssl enc -d -aes-256-cbc -in $1.enc -out Midterm2_answers.ipynb -iter 10000 -pass file:$HOME/.ssh/id_rsa
