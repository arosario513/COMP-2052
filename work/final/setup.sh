#!/bin/bash
mkdir mass
cd mass
git init
git branch -m main
git remote add origin https://github.com/arosario513/COMP-2052.git
git sparse-checkout init
git sparse-checkout add work/final
git pull origin main
mv ./work/final ..
cd ..
rm -rf mass

