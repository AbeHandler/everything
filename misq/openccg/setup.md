conda activate misq  # activate the MISQ environment
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-16.0.1.jdk/Contents/Home # set java home
export OPENCCG_HOME=/Users/abramhandler/everything/misq/openccg
./bin/tccg grammars/tiny/grammar.xml # run tccg on grammar.xml
tccg> Yan studies nlg # parse it
tccg> :r # render it (i.e. generate from parse)
tccg> :2xml parses/she.xml # send parse to a file
tccg> :r parses/she.xml # parse from file
$ ./bin/ccg-realize parses/she.xml -g grammars/tiny/grammar.xml # we want the top level parse, $s$

$ cd grammars/tiny && ./test.sh # make sure everything still parses
