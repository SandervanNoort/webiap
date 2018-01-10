#!/bin/sh

# apt-get install imagemagick

rm -Rf scaled
mkdir scaled
convert -size 160x30 xc:white canvas.png
for i in `ls *.*`; do
    convert -geometry 160x30 $i scaled/$i;
    composite -gravity south scaled/$i canvas.png scaled/$i
done;
# convert -geometry 160x60 ecdc.jpg scaled/ecdc.jpg
rm canvas.png
