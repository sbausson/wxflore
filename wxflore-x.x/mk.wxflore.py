#!/bin/bash


if [ $# == 1 ]; then
    version=$1
else
    version=`date +"%Y.%m.%d"`
    target="wxflore-$version"
    if [ ! -d "$target" ]; then
	echo "DOES NOT EXIST"
    else
	echo "ALREADY EXIST" $target
	i=1
	while [ -d "$target-r$i" ]; do
	    i=$((i+1))
	done
	version="$version-r$i"
    fi
fi

target="wxflore-$version"
src="wxflore-x.x"
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
