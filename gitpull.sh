DEV="develop"
CURRENT_LOCATION=$PWD
PROJECT_NAME=$(basename $PWD)
PROJECT_HEAD=$(cat $CURRENT_LOCATION/.git/HEAD)
PROJECT_BRANCH=$(echo $PROJECT_HEAD | awk -F'/' '{print $NF}')
SUBMODULE_PATH=$(git submodule | awk 'NR==1 {print $2}')
# awk 'NR==1 {print $2}' limitation while the project has more than one submodules
BRANCH=${1:-$PROJECT_NAME}
SUBMODULE_NAME=$(echo $SUBMODULE_PATH | awk -F'/' '{print $NF}')
SUBMODULE_HEAD=$(cat $CURRENT_LOCATION/.git/modules/$SUBMODULE_PATH/HEAD)
SUBMODULE_BRANCH=$(echo $SUBMODULE_HEAD | awk -F'/' '{print $NF}')

if [[ $PROJECT_BRANCH != $DEV ]]
then
    git checkout $DEV
fi
echo "\nPROJECT: [$PROJECT_NAME] | BRANCH: [$PROJECT_BRANCH] -> [$DEV]"; git pull

cd "$CURRENT_LOCATION/$SUBMODULE_PATH"
if [[ $SUBMODULE_BRANCH != $DEV ]]
then
    git checkout $DEV
fi
echo "\nSUBMODULE: [$SUBMODULE_NAME] BRANCH: [$SUBMODULE_BRANCH] -> [$DEV]"; git pull

cd $CURRENT_LOCATION
