# set up the env
sudo apt -y update
sudo apt -y install python3-pip
sudo apt -y install moreutils

# install Google-OCR
if [ -d ~/ocr/img2opf ]; then
  cd ~/ocr/img2opf;
  git pull;
  cd ..;
else
  git clone https://github.com/Esukhia/img2opf.git;
fi

pip3 install -r img2opf/requirements.txt
pip3 install -e img2opf[bdrc]

# git setup
pip3 uninstall gitdb2
pip3 install gitdb
git config --global user.email "ten13zin@gmail.com"
git config --global user.name "tenzin"
