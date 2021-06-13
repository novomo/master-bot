branch=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
git add .
git commit -m $1
git push --set-upstream origin $branch

#update os
sudo apt update -y
#install git
sudo apt-get install git
#install pip3
sudo apt install -y python3-pip
#install node
curl -sL https://deb.nodesource.com/setup_15.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt-get update
sudo apt-get install nodejs
npm install -g yarn
#install c++
sudo apt install -y g++
#install mpi
sudo apt-get install -y mpich
#install ping server
read -p 'Do you have a ping server Y/n: ' response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
  command = "bash $(realpath "$0" | sed 's|\(.*\)/.*|\1|')/ping_server.sh"
  #write out current crontab
  crontab -l > mycron
  #echo new cron into cron file
  echo "*/5 * * * * $command" >> mycron
  #install new cron file
  crontab mycron
  rm mycron
fi

#get linux repo
while IFS="" read -r p || [ -n "$p" ]
do
  sudo add-apt-repository $p
done < install/linux-repos.txt
#update os
sudo apt update -y
#install os packages
while IFS="" read -r p || [ -n "$p" ]
do
  sudo apt install -y $p
done < system.txt
#install python packages
if [[ -f "install/requirements.txt" ]]; then
    pip3 install -r requirements.txt
fi
#install node modules
if [[ -f "package.json" ]]; then
    yarn install
fi

for f in *; do
    if [[ -d "$f" && ! -L "$f" ]]; then
        cd $f && git checkout master
        git branch --set-upstream-to=origin/master master
        git pull
        cd ..
    fi
done