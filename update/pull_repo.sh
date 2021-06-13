branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
git add .
git commit -m $1
git push --set-upstream origin $branch