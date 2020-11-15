# On machine: ln -s /Users/abramhandler/.enc.sh ~/bin/enc.sh
# in zshrc: alias enc="enc.sh"

openssl enc -aes-256-cbc -salt -in $1 -out $1.enc -iter 10000 -pass file:$HOME/.ssh/id_rsa 
