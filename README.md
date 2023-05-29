# Descent 1 Tools

## Overview
This repository is a collection of tools for reading and working with data files from Descent, a first-person 360-degree shooter video game from 1995 by Parallax Software and Interplay.

### Compatibility
The parser is built to work with the full version of Descent. The shareware version of Descent is not supported.

### File Spec
For a specification of the descent level format (RDL), see the [level spec](./LEVEL-SPEC.md). 

### Dependencies

Before using the tools, you must first install Python3 and the following Python dependencies: `bitstring` and `fixedpoint`.

You can install both dependencies using `pip3 install -r requirements.txt`

## Tools

### LevelParser

This tool reads in Descent 1 level (RDL) files, and output OBJ representation of the level geometry (cubes and vertices). The OBJ file can be imported as a 3D model into a tool like Blender.

Usage: `python3 levelParser.py <rdl-input-file> <obj-output-file>`