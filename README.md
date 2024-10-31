# g-code-lib
`gcode_lib.py` is a python library for programatically generating g-codes for CNC machining.
It provides functions for:
* simple 2D geometries : lines, rectangles, ...
* importing polygons from [Inkscape](https://inkscape.org/)
* transforming 2D shapes : mirroring, applying offset and gain, expanding, shrinking, ...
* drilling shapes with multiple passes

The repository further contains the `gcodeToSvg.py` script which reads a g-code file
and writes an [Inkscape](https://inkscape.org/) `.svg` file
where the different pass depths are shown in different layers and with different gray levels.

It also has a python library, `text_lib.py`, which allows to mill a line made out of simple letters using a single pass.

The [wiki](https://github.com/fcorthay/g-code-lib/wiki) shows how to use the library.

---

Some application-specific shape generators are provided in the
`linuxCNC` [Simple G-Code Generators](https://github.com/LinuxCNC/simple-gcode-generators).
