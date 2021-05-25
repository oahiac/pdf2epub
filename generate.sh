#/bin/bash

echo "$1"
# pdf to pics
mkdir ./pics
rm ./pics/.DS_Store
mkdir ./res
rm ./res/.DS_Store
mkdir ./pages
rm ./pages/.DS_Store

pdftoppm $1 ./pics/pic -jpeg

./main.py

# copy all the files into res
cp ./pics/pic-001.jpg ./pics/cover.jpeg
cp ./pages/* ./res/
cp ./pics/* ./res/
cp  -r ./stableFiles/* ./res/

# generate epub file
zip -r book.epub ./res/*

mv book.epub $1/../book/epub

rm -rf ./pics
rm -rf ./pages
rm -rf ./res
