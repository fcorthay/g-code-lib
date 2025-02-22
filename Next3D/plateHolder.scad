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

railWidth = 5;
railWidthMargin = 0.1;
railSpacing = 27.5;
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
                                                                    // rendering
printHolder = false;
  printBottomPart = false;
  printTopPart = true;
printSupportsAndSpacers = true;
  printBoardWidthSpacers = false;
  print2cmSpacers = true;
  printFrontSupports = false;
  printLongEdgeSupports = false;
  printShortEdgeSupports = true;
printSupports = !printSupportsAndSpacers && false;
  printFrontSupports1 = !printSupportsAndSpacers && false;
printSpacers = !printHolder && !printSupportsAndSpacers && !printSupports;
  printSpacer2 = false;

eps = 0.01;
$fn = 200;   // facet number

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

if (printSupportsAndSpacers) {
  translate([0, 2*railDepth + spacingHeight + plateHeight, 0]){
    translate([0, 2*railDepth + spacingHeight + plateHeight, 0]){
      translate([0, 2*railDepth + spacingHeight + plateHeight, 0]){
        translate([0, 2*railDepth + spacingHeight, 0]){
          translate([0, 2*railDepth + spacingHeight, 0])
                                                          // board width spacers
            if (printBoardWidthSpacers)
              for (xIndex = [0:3])
                translate([xIndex*(spacerWidth + railWidth), 0, 0])
                  rotate([90, 0, 0])
                    lateralSpacer(plateHeight);
                                                                 // 2 cm spacers
          if (print2cmSpacers)
            for (xIndex = [0:7])
              translate([xIndex*(spacerWidth + railWidth), 0, 0])
                rotate([90, 0, 0])
                  lateralSpacer(2*spacerWidth);
        }
                                                               // front supports
        if (printFrontSupports)
          for (xIndex = [0:3])
            translate([xIndex * (railSpacing + 2*railWidth), 0, 0])
              rotate([90, 0, 0])
                frontSupport();
      }
                                                // long edge support and spacers
      if (printLongEdgeSupports)
        for (xIndex = [0:1])
          translate([xIndex*(edgeTotalLength2 + railWidth), 0, 0])
            rotate([90, 0, 0])
              spacerEdge(
                edgeTotalLength2, edgeSupportingLength, edgeSupportingWidth
              );
    }
                                       // mirrored long edge support and spacers
    if (printLongEdgeSupports)
      for (xIndex = [0:1])
        translate([xIndex*(edgeTotalLength2 + railWidth), 0, 0])
          rotate([90, 0, 0])
            translate([edgeTotalLength2, 0, 0])
              mirror([1, 0, 0])
                spacerEdge(
                  edgeTotalLength2, edgeSupportingLength, edgeSupportingWidth
                );
  }
                                               // short edge support and spacers
  if (printShortEdgeSupports)
    for (xIndex = [0:1])
      translate([xIndex*(edgeTotalLength1 + railWidth), 0, 0])
        rotate([90, 0, 0])
          if (xIndex < 1)
            spacerEdge(
              edgeTotalLength1, edgeSupportingLength, edgeSupportingWidth
            );
          else
            translate([edgeTotalLength1, 0, 0])
              mirror([1, 0, 0])
                spacerEdge(
                  edgeTotalLength1, edgeSupportingLength, edgeSupportingWidth
                );
}
else if (printSupports)
                                                                // front support
  if (printFrontSupports1)
    frontSupport();
  else
                                                      // edge support and spacer
    spacerEdge(edgeTotalLength2, edgeSupportingLength, edgeSupportingWidth);

                                                                      // spacers
else if (printSpacer2)
                                                                  // 2 cm spacer
  if (printSpacer)
    lateralSpacer(2*spacerWidth);

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

//============================================================================\\
                                                                  // edge spacer
module spacerEdge(totalLength, supportingLength, supportingWidth){
                                                                       // spacer
  cube([
    totalLength, spacerWidth + supportingWidth, spacingHeight
  ], center = false);
                                                              // holding L-shape
  difference() {
    translate([totalLength - spacerWidth - supportingLength, 0, 0])
      cube([
        spacerWidth + supportingLength,
        spacerWidth + supportingWidth,
        spacingHeight + plateHeight
      ], center = false);
    translate([
      totalLength - supportingLength - spacerWidthMargin,
      spacerWidth,
      spacingHeight
    ])
      cube([
        2*supportingLength,
        2*supportingWidth,
        2*plateHeight
      ], center = false);
  }
                                                                        // rails
  for (offset = [0, railSpacing])
    translate([offset + railWidthMargin/2, 0, -railDepth + eps])
      cube([
        railWidth - railWidthMargin, frontSupportWidth, railDepth
      ], center = false);
}
