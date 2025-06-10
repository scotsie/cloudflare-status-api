#!/bin/bash

NAME=$(python3 -c 'print(eval(open("package.manifest").read())["name"])')
VERSION=$(python3 -c 'print(eval(open("package.manifest").read())["version"])')
rm /omd/sites/cmk/var/check_mk/packages/${NAME} \
   /omd/sites/cmk/var/check_mk/packages_local/${NAME}-*.mkp ||:

mkp -v package package.manifest 2>&1 | sed '/Installing$/Q' ||:

cp /omd/sites/cmk/var/check_mk/packages_local/$NAME-$VERSION.mkp .

mkp inspect $NAME-$VERSION.mkp