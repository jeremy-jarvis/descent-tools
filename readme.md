# Descent 1 Tools

## Overview
This repository is a collection of tools for reading and working with data files from 1995 by Parallax Software and Interplay.

### Compatibility
The parser is built to work with the full version of Descent 1. Currently, the shareware version of Descent is not supported.

## Tools

### LevelParser

Reads in Descent 1 level (RDL) files, and output OBJ representation of the level geometry (cubes and vertices). The OBJ file can be imported as a 3D model into a tool like Blender.

Usage: `python3 levelParser.py <rdl-input-file> <obj-output-file>`