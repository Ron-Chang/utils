# Color Tag
if [ "$TERM" = 'xterm-256color' ]; then
	RESET='\x1b[0m'
	ON_RED='\x1b[5;30;41m'
	ON_YELLOW='\x1b[5;30;43m'
	ON_BLUE='\x1b[5;30;44m'

	RED='\x1b[5;30;31m'
	YELLOW='\x1b[5;30;33m'
	BLUE='\x1b[5;30;34m'
elif [ "$TERM" = 'screen-256color-bce' ]; then
	RESET='\e[0m'
	ON_RED='\e[5;30;41m'
	ON_YELLOW='\e[5;30;43m'
	ON_BLUE='\e[5;30;44m'

	RED='\e[5;30;31m'
	YELLOW='\e[5;30;33m'
	BLUE='\e[5;30;34m'
else
	RESET=''
	ON_RED=''
	ON_YELLOW=''
	ON_BLUE=''
fi

if [ "$1" = '' ]
then
	echo "$ON_RED[ERROR   ]$RESET| [ * 'TAG' Not Specified!]"
fi

TAG=$1

if [ "$TAG" = 'develop' ] || [ "$TAG" = 'version1' ] || [ "$TAG" = 'release' ] || [ "$TAG" = 'master' ]
then
	PREFIX=`basename $PWD | awk -F'_' '{print $1}'`
	echo "${ON_BLUE}[INFO    ]${RESET}| [ * Switch ${BLUE}Repo${RESET} and Submodule ${BLUE}'$PREFIX'${RESET} to ${RED}$TAG${RESET}]"
	git checkout ${TAG}; git config --file .gitmodules --get-regexp path | awk '{ print $2 }' | grep $PREFIX | xargs -I@ git -C @ checkout $TAG
	echo "${ON_BLUE}[INFO    ]${RESET}| [ * Switch Submodule ${BLUE}'general'${RESET} to ${RED}master${RESET} if exist]"
	git config --file .gitmodules --get-regexp path | awk '{ print $2 }' | grep general | xargs -I@ git -C @ checkout master
fi

