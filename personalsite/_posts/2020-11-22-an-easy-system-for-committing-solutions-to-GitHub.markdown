---
layout: post
title:  "An easy system for committing solutions to GitHub"
date:   2019-10-01 13:40:53 -0400
categories: teaching 
---

### An easy system for committing solutions to GitHub
#### How to post solutions to public repos without giving away the answer

This semester, I found myself making a lot of solutions to problem sets and exams, which I organize in public GitHub repos. I wanted a way to store the solutions to these assignments in the repos.

After a few months I found a solution that seemed to work well. The basic idea is to created a symlinked script on my local machine which encrypts solutions files so they can be committed. 

Here is how it works 

```
$ ls # secret_solutions.ipynb
$ enc secret_solutions.ipynb. # my encrypt script
$ ls secret_solutions.ipynb secret_solutions.ipynb.enc
$ head -1 secret_solutions.ipynb.enc
ք|�m@�!�3�����3+�~�V��j:����a a;}�Y�a�r�H�F,yʠv�1h;%�^�}'"�i�ɸ�L���M�
$ git add secret_solutions.ipynb.enc && git commit -m solutions && git push origin main 
$ rm secret_solutions.ipynb
$ dec secret_solutions.ipynb  # my decrypt script
$ ls secret_solutions.ipynb, secret_solutions.ipynb.enc
```

Here is how to set it up. I am assuming you have have installed openssl and set up a private key at ~/.ssh/id_rsa

First download enc.sh and dec.sh

```
$ wget https://gist.githubusercontent.com/AbeHandler/2682a90d2dc8f70ec3999bf1f54cefa2/raw/f76875941e18f90701b7da4e092526c367e97aaf/enc.sh -O $HOME/.enc.sh

$ wget https://gist.githubusercontent.com/AbeHandler/c12519ce198b13522628c916c9084191/raw/c00938416060a14adc7850ea9c805414d4ecc9d5/dec.sh -O $HOME/.dec.sh
```

```
$ chmod +x $HOME/.dec.sh && chmod +x $HOME/.enc.sh # give run permission
```

Then symlink the files so you can access them in your PATH 

```
$ ln -s $HOME/.dec.sh ~/bin/dec.sh
$ ln -s $HOME/.enc.sh ~/bin/enc.sh
```

Finally, alias the scripts (I did this in a .zshrc file)

```
alias enc="enc.sh"
alias dec=“dec.sh”
```

After that you should be able to run 

```
$ enc file.txt # encrypts file.txt into file.txt.enc
$ dec file.txt # decrypts file.txt.enc into file.txt
```

Important note: this system relies on a private key stored on your local machine. If you lose the key (e.g. maybe you get a new laptop), you will lose the encrypted answer forever. If you are teaching a class, losing your solutions is probably not such a big deal. But I did want to make a note of this.

Important note: if you are a student and you have read to here and also find a way to hack this system, I will give you an A.