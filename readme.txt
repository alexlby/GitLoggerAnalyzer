1. generate git log cmd :
    git log --after={2014-04-19} --before={2014-05-18} --no-merges --name-only develop_rel_1.7.0 >> develop_rel_1_7_0.txt
2. after generating git log file, remember to use notepad++ to transform its format to utf8
3. remember to remove some Chinese char manually
4. truncate tables
5. run reader
6. run report

know issues:
1. how to convert git log file from non-utf8 to utf8?
2. need set charset of mysql db to support some non-latin chars

tobe enhanced:
1. refactor API to handle different system names
2. refactor API to handle different branch names
3. output file naming standard for each team