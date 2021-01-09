# Descent 1 Level Specification (RDL)

## Introduction
Each Descent level is stored in a separate binary file with an *.rdl file extension. RDL stands for "Registered Descent Level". Multiple RDL files can be stored within a single HOG file as a unified level set, also known as a "mission". Alternatively, a single RDL file can stand alone and be played without being packaged in a HOG file. Either way, either an RDL or HOG file must be paired with a MSN metadata file to enable it to be loaded by Descent and played.

An RDL file contains binary data in a specific order. The length of the file and the presense of specific binary elements is determined by how many cubes (and objects?) are in the level, and the properties of each cube.

The following is a specification of the RDL file format from beginning to end.

## The Spec
### Header
Every Descent level begins with a header containing the following elements:
* Signature
  * 4 byte string
  * This will be "LVLP".
* Version
  * 4 byte integer
  * For Descent 1 this is the value 1
* Mine structures offset
  * 4 byte integer
  * The byte location in the file where the mine structures start (vertices and cubes).
* Object offset
  * 4 byte integer
  * The byte location in the file where the objects start (player, power-ups, enemies, etc).
* File size
  * 4 byte integer
  * The size of the entire file.

### Mine Structures
This data starts immediately after the header (always true?) which will correspond to the the mine structures offset location specified in the header. The first element, though, is a spacer of empty data before the actual mine structures begin. After the spacer is information about the level's vertex count and cube count.

* Spacer
  * 1 byte
  * The contents of this byte can be ignored.

* Vertex Count
  * 2 byte integer
  * The number of vertices in the level.

* Cube Count
  * 2 byte integer
  * The number of cubes in the level.

The geometry of a Descent 1 level is made up of cubes, each of which has 8 vertices (corners). Each vertex is specified by its x, y, z coordinates in the level. If you can imagine level made up of only a single cube at the center of the level, it could be defined by 8 vertices as follows:
<pre>
 10.0  10.0 -10.0
 10.0 -10.0 -10.0
-10.0 -10.0 -10.0
-10.0  10.0 -10.0
 10.0  10.0  10.0
 10.0 -10.0  10.0
-10.0 -10.0  10.0
-10.0  10.0  10.0
</pre>

In this case, the center of the cube is at the very origin (center) of the level, and each side of the cube is 20 units long. Each vertex defines one of the 8 corners of the cube.

#### NEXT: Descibe how vertices are shared among cubes, with a two-cube example.

