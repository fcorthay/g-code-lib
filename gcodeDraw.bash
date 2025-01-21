#!/bin/bash

BASE_DIR=`dirname $BASH_SOURCE`
cd $BASE_DIR/..

DRAWING=$1
rm $DRAWING.gcode $DRAWING.svg

./$DRAWING.py
$BASE_DIR/gcodeToSvg.py $DRAWING.gcode $DRAWING.svg
sed -i 's/rgb(228, 228, 228)/blue/g' $DRAWING.svg
sed -i 's/rgb(229, 229, 229)/blue/g' $DRAWING.svg
inkscape --verb ZoomDrawing $DRAWING.svg 2>/dev/null
