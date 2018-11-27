#! bin/bash
chmod +x SPC.py
chmod +x sync.sh
sudo cp sync.sh /usr/bin/
sudo cp SPC.1.gz /usr/share/man/man1/
sudo ln -s ~/SPC_config/Linux\ Client/SPC.py /usr/local/bin/
sudo mv /usr/local/bin/SPC.py /usr/local/bin/SPC
python3 replace.py