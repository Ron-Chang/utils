CURRENT_LOCATION=$PWD
PROJECT_NAME=${1:-$(basename $PWD)}
PROJECT_HEAD=$(cat $CURRENT_LOCATION/.git/HEAD)
PROJECT_BRANCH=$(echo $PROJECT_HEAD | awk -F'/' '{print $NF}')
SUBMODULE_PATH=$(git submodule | awk 'NR==1 {print $2}')
# awk 'NR==1 {print $2}' limitation while the project has more than one submodules
SUBMODULE_NAME=$(echo $SUBMODULE_PATH | awk -F'/' '{print $NF}')
SUBMODULE_HEAD=$(cat $CURRENT_LOCATION/.git/modules/$SUBMODULE_PATH/HEAD)
SUBMODULE_BRANCH=$(echo $SUBMODULE_HEAD | awk -F'/' '{print $NF}')

if [[ $PROJECT_BRANCH != develop ]]
then
    git checkout develop
fi
echo "[PROJECT]"
echo "[$PROJECT_NAME] | PROJECT BRANCH: [$PROJECT_BRANCH]"
git pull

cd "$CURRENT_LOCATION/$SUBMODULE_PATH"
if [[ $SUBMODULE_BRANCH != develop ]]
then
    git checkout develop
fi
echo "[SUBMODULE]"
echo "[$SUBMODULE_NAME] BRANCH: [$SUBMODULE_BRANCH]"
git pull

cd $CURRENT_LOCATION
