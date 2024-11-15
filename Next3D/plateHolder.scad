// plateHolder.scad - holder for plates on the CNC
                                                                // holder dimensions
holderLength = 52;
holderWidth = 20;
holderTopHeight = 5;
holderStepLength = 5;

spacingHeight = 10;
plateHeight = 6;

boltDiameter = 5.1;
boltHeadDiameter = 9.1;
boltHeadHeight = 4;

railWidth = 5.2;
railWidthMargin = 1;
railSpacing = 32.6;
railDepth = 3;

firstBoltOffset = 10;

//................................................................................\\
                                                                   // derived values
boltOffsets = [
  firstBoltOffset + railWidth/2,
  firstBoltOffset + railWidth/2 + railSpacing/2,
  firstBoltOffset + railWidth/2 + railSpacing
];
railOffsets = [boltOffsets[0], boltOffsets[2]];

//––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\\
                                                                        // rendering
printBottomPart = false;
printTopPart = false;

eps = 0.01;
$fn = 200;   // facet number

//––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\\
                                                                  // object geometry
if (printBottomPart)
  color("yellow")
    rotate([90, 0, 0])
      holderBottom();
else if (printTopPart)
  color("yellow")
//    translate([0, 0, holderTopHeight])
//      rotate([180, 0, 0])
        holderTop();
else {
  color("LightGrey")
    holderBottom();
  color("Silver")
    translate([0, 0, spacingHeight + plateHeight])
      holderTop();
}

//................................................................................\\
                                                               // holder bottom part
module holderBottom(){
  difference(){
    union(){
                                                                             // base
      cube([holderLength, holderWidth, spacingHeight], center=false);
                                                                            // rails
      for (offset = railOffsets)
        translate([offset, holderWidth/2, -railDepth/2])
          cube([
            railWidth - railWidthMargin, holderWidth, railDepth + eps
          ], center=true);
    }
                                                                            // bolts
    for (offset = boltOffsets)
      translate([offset, holderWidth/2, 0])
        bolt();
                                                                      // 45° cutouts
    for (side = [-1, 1])
      translate([
        holderLength - 2*holderWidth/3,
        holderWidth/2 + side*holderWidth/2 + side*holderWidth/3,
        -0.1*spacingHeight - railDepth
      ])
        rotate([0, 0, -45])
          cube([holderWidth, holderWidth, 1.2*spacingHeight + railDepth]);
  }
                                                                // plate height step
  cube([holderStepLength, holderWidth, spacingHeight + plateHeight], center=false);
}

//................................................................................\\
                                                                  // holder top part
module holderTop(){
  difference(){
                                                                             // base
    cube([holderLength, holderWidth, holderTopHeight], center=false);
                                                                       // bolt holes
    for (offset = boltOffsets)
      translate([offset, holderWidth/2, -spacingHeight])
        bolt();
                                                                      // 45° cutouts
    for (ySide = [-1, 1])
      translate([
        holderLength - 2*holderWidth/3,
        holderWidth/2 + ySide*holderWidth/2 + ySide*holderWidth/3,
        -spacingHeight/4
      ])
        rotate([0, 0, -45])
          cube([holderWidth, holderWidth, spacingHeight]);
  }
}

//................................................................................\\
                                                                             // bolt
module bolt(){
                                                                             // bolt
  translate([0, 0, spacingHeight])
    cylinder(d=boltDiameter, h=2*spacingHeight, center=true);
  translate([0, 0, boltHeadHeight/2 - railDepth/2 - eps])
    rotate([0, 0, 90])
      cylinder(d=boltHeadDiameter, h=boltHeadHeight+railDepth, center=true, $fn=6);
}