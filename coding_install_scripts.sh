#!/usr/bin/env bash
#install XCODE and "command line tools"
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"
echo "export PATH=/usr/local/bin:$PATH" >> ~/.bash_profile
brew install vim
brew install macvim
brew install gfortran
brew install python
pip install numpy
pip install scipy
pip install matplotlib
pip install ipython

brew install autojump
echo "[[ -s `brew --prefix`/etc/autojump.sh ]] && . `brew --prefix`/etc/autojump.sh" >> ~/.bash_profile

