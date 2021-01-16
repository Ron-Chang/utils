FILE='tmp.out'

if test -f $FILE
then
    rm -f $FILE
fi
gcc $1 -o $FILE && "./$FILE"
