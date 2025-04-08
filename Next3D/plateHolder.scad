// plateHolder.scad - holder for plates on the CNC
                                                                    // rendering
printHolder = false;
  printBottomPart = false;
  printTopPart = true;

eps = 0.01;
$fn = 200;   // facet number

//––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\\
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

railWidth = 5;
railWidthMargin = 0.25;
railSpacing = 32.5;
railDepth = 3;

firstBoltOffset = 10;

spacerWidth = spacingHeight;
spacerWidthMargin = 0.1;
frontSupportingWidth = 8;

edgeTotalLength1 = railSpacing + railWidth + 1;
edgeTotalLength2 = railSpacing + railWidth + 11;
edgeSupportingLength = spacerWidth;
edgeSupportingWidth = 4;

//............................................................................\\
                                                               // derived values
boltOffsets = [
  firstBoltOffset + railWidth/2,
  firstBoltOffset + railWidth/2 + railSpacing/2,
  firstBoltOffset + railWidth/2 + railSpacing
];
railOffsets = [boltOffsets[0], boltOffsets[2]];

frontSupportWidth = frontSupportingWidth + plateHeight;

//––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\\
                                                              // object geometry
if (printHolder)
                                                                // holder bottom
  if (printBottomPart)
    color("yellow")
      rotate([90, 0, 0])
        holderBottom();
                                                                   // holder top
  else if (printTopPart)
    color("yellow")
      holderTop();
                                                              // complete holder
  else {
    color("LightGrey")
      holderBottom();
    color("Silver")
      translate([0, 0, spacingHeight + plateHeight])
        holderTop();
  }

//============================================================================\\
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
  cube([
    holderStepLength, holderWidth, spacingHeight + plateHeight
  ], center=false);
}

//............................................................................\\
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

//............................................................................\\
                                                                         // bolt
module bolt(){
                                                                         // bolt
  translate([0, 0, spacingHeight])
    cylinder(d=boltDiameter, h=2*spacingHeight, center=true);
  translate([0, 0, boltHeadHeight/2 - railDepth/2 - eps])
    rotate([0, 0, 90])
      cylinder(
        d=boltHeadDiameter, h=boltHeadHeight+railDepth, center=true, $fn=6
      );
}

//============================================================================\\
                                                 // front and back side supports
module frontSupport(){
                                                                 // bottom plate
  cube([
    railSpacing + railWidth, frontSupportWidth, spacingHeight
  ], center = false);
                                                               // lateral holder
  cube([
    railSpacing + railWidth, plateHeight, spacingHeight + plateHeight
  ], center = false);
                                                                        // rails
  for (offset = [0, railSpacing])
    translate([offset + railWidthMargin/2, 0, -railDepth + eps])
      cube([
        railWidth - railWidthMargin, frontSupportWidth, railDepth
      ], center = false);
}

//============================================================================\\
                                                               // lateral spacer
module lateralSpacer(length){
                                                                       // spacer
  cube([
    spacerWidth, length, spacingHeight
  ], center = false);
                                                                         // rail
    translate([railWidthMargin/2, 0, -railDepth + eps])
      cube([railWidth - railWidthMargin, length, railDepth], center = false);
}
