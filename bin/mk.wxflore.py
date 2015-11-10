#!/bin/bash


if [ $# == 1 ]; then
    version=$1
else
    version=`date +"%Y.%m.%d"`
fi

src="wxflore-x.x"
target="wxflore-$version"
archive="$target".tar.bz2

#for arg in $( echo $* ); do 
#    echo $arg
#done

if  [ -e $archive ];then
    rm -v $archive
fi

if  [ -e $target ];then
    rm -r -v $target
fi

cp -av $src $target
rm $target/*~ $target/*.pyc
echo "version=\""$version"\"" > $target/version.py

tar cvfj $archive $target
