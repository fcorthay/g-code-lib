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
printBottomPart = true;
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
    translate([0, 0, holderTopHeight])
      rotate([180, 0, 0])
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
                                                                             // base
    translate([0, 0, 0])
      cube([holderLength, holderWidth, spacingHeight], center=false);
                                                                            // bolts
    for (offset = boltOffsets)
      translate([offset, holderWidth/2, 0])
        bolt();
  }
                                                                // plate height step
  cube([holderStepLength, holderWidth, spacingHeight + plateHeight], center=false);
                                                                            // rails
  difference(){
                                                                             // base
    for (offset = railOffsets)
      translate([offset, holderWidth/2, -railDepth/2])
        cube([
          railWidth - railWidthMargin, holderWidth, railDepth + eps
        ], center=true);
                                                                       // bolt holes
    for (offset = railOffsets)
      translate([offset, holderWidth/2, -railDepth/2])
        cylinder(d=boltHeadDiameter, h=railDepth + eps, center=true);
  }
}

//................................................................................\\
                                                                  // holder top part
module holderTop(){
  difference(){
                                                                             // base
    holderBottom();
                                                                          // top cut
    translate([-holderLength/2, -holderWidth/2, holderTopHeight])
      cube([2*holderLength, 2*holderWidth, spacingHeight + plateHeight]);
                                                                       // bottom cut
    translate([-holderLength/2, -holderWidth/2, -2*railDepth])
      cube([2*holderLength, 2*holderWidth, 2*railDepth]);
  }
}

//................................................................................\\
                                                                             // bolt
module bolt(){
                                                                             // bolt
  translate([0, 0, spacingHeight])
    cylinder(d=boltDiameter, h=2*spacingHeight, center=true);
  translate([0, 0, boltHeadHeight/2 - eps])
    rotate([0, 0, 90])
      cylinder(d=boltHeadDiameter, h=boltHeadHeight, center=true, $fn=6);
}