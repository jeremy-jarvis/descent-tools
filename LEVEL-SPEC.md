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
* Objects offset
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

* Vertices
  * 12 bytes * vertex count
  * Each vertex is defined by 3 coordinates: x, y, and z. Each coordinate is represented by 4 bytes of data. So, each vertex is represented by 4 + 4 + 4 = 12 bytes of data.
  * Each coordinate should be interpreted as a 32-bit fixed-point number in 16.16 format. That means that 16 bits represent the integer portion of the number, and 16 bits represent the fractional portion of the number.
  * For more details on how this data is stored, see the detailed explanation later in this spec.

* Cubes

  The data for each cube is of variable length depending on the cube's properties. So, one cannot simply multiply the cube count by a known size to determine the total amount of data that represents the cubes. If you want to calculate the number of bytes of cube data, you should be able to do so as follows: `number of bytes of cubes data = objects offset - current byte location in RDL data`

  The data for each cube is provided one after the other within the RDL file, until all the cubes have been specified. The following provides a brief specification for a single cube.A more in-depth walkthrough of the cube data is provided later in this specification.

  * Cube Neighbor Bitmask
    * 1 byte
    * Bits 0-5 of the bitmask indicate whether another cube is attached to a specific side of the cube in question. If a bit is set to 1, then that means that there is another cube attached to that side.
      * 0 = Left
      * 1 = Top
      * 2 = Right
      * 3 = Bottom
      * 4 = Back
      * 5 = Front
    * If Bit 6 is set to 1, then the cube is an energy center.
    * Bit 7 is not used.

  * Cube Neighbor IDs
    * 2 byte integer (per cube neighbor, if any)
    * For each cube neighbor specified by the Cube Neighbor Bitmask, a 2-byte integer will follow the bitmask that represents the ID of the neighbor cube. The ID specifies the index of the neighbor cube within the cubes data. A cube can have multiple neighbors, which would mean that multiple cube IDs will follow the bitmask.

  * Vertex References
    * TODO


The geometry of a Descent 1 level is made up of cubes, each of which has 8 vertices (corners). Each vertex is specified by its x, y, z coordinates in the level. If you can imagine level made up of only a single cube at the center of the level, that cube could be defined by 8 vertices as follows:
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

Now, imagine a level made up of two cubes. The two cubes are connected by one side to make a very short hallway. Those two cubes could be defined by 12 vertices as follows: 

<pre>
 10.0  10.0 -20.0
 10.0 -10.0 -20.0
-10.0 -10.0 -20.0
-10.0  10.0 -20.0
 10.0  10.0  0.0
 10.0 -10.0  0.0
-10.0 -10.0  0.0
-10.0  10.0  0.0
 10.0  10.0  20.0
 10.0 -10.0  20.0
-10.0 -10.0  20.0
-10.0  10.0  20.0
</pre>

In this case, the vertices with a z-value of 0.0 are those that are located in the very middle of the level. You might wonder why there are only 12 vertices instead of 16 (8 for each cube). There are 12 because the two cubes share four of the vertices where they are attached to each other. Each cube has four vertices all to its own (on each end of the hallway), and each cube has four vertices that are shared with the other cube.
