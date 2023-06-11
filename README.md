# Descent Tools

## Overview
The purpose of this repository is to be a collection of tools for reading and working with data files from [Descent](https://en.wikipedia.org/wiki/Descent_(video_game)), a first-person 360-degree shooter video game from 1995 by Parallax Software and Interplay. Currently, the only tool in this repository is the Level Parser.

## Future Improvements
For a list of potential improvements, see [TODO.md](./TODO.md).

## LevelParser

This tool reads in Descent 1 level (RDL) files, and outputs an OBJ representation of the level geometry (cubes and vertices). The OBJ file can be imported as a 3D model into a tool like Blender.

### Usage

`python3 levelParser.py <rdl-input-file> <obj-output-file>`

### Dependencies

Before using the parser, you must first install Python 3 and the following Python dependencies: `bitstring` and `fixedpoint`.

After installing Python 3, you can install both dependencies using `pip3 install -r requirements.txt`

### Compatibility
The parser is built to work with the full version of Descent. The shareware version of Descent is not supported.

### File Spec
For a specification of the Descent level format (RDL), see the [level spec](./LEVEL-SPEC.md).