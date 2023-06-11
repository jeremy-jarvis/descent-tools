# Descent 1 Level Specification (RDL)

## Introduction
The purpose of this documentation is to be a comprehensive and clear specification of the RDL file format from beginning to end. It currently contains a few gaps in specification (e.g. Objects) due to the Level Parser not yet being able to parse those elements. Those gaps are marked with TODOs.

This spec and the Level Parser are based mainly upon the RDL spec [posted here](https://web.archive.org/web/20180801215219/http://www.descent2.com/ddn/specs/rdl/) on the Internet Archive, as well as knowledge gleaned from examining other parsers. 

Each Descent level is stored in a separate binary file with an *.rdl file extension. RDL stands for "Registered Descent Level". Multiple RDL files can be stored within a single HOG file as a unified level set, also known as a "mission". Alternatively, a single RDL file can stand alone and be played without being packaged in a HOG file. Either way, an RDL or HOG file must be paired with a MSN metadata file to enable it to be loaded by Descent and played.

An RDL file contains binary data in a specific order. The length of the file and the presence of specific binary elements are determined by how many cubes (and objects?) are in the level, and the properties of each cube. The following describes the file data from beginning to end.

## The RDL File Spec
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
This data starts immediately after the header (TODO: Is this always true?) which will correspond to the the mine structures offset location specified in the header. The first element, though, is a spacer of empty data before the actual mine structures begin. After the spacer is information about the level's vertex count and cube count.

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

  The data for each cube is of variable length depending on the cube's properties. So, one cannot simply multiply the cube count by a known size to determine the total amount of data that represents the cubes. To calculate the number of bytes of cube data, you should be able to do so as follows: 
  
  `number of bytes of cubes data = objects offset - current byte location in RDL data`

  The data for the cubes are provided one after the other within the RDL file, until all the cubes have been specified. The following provides a brief specification for a single cube. A more in-depth walkthrough of the cube data is provided later in this specification.

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
    * 2 byte integer (per cube neighbor)
    * For each cube neighbor specified by the Cube Neighbor Bitmask, a 2-byte integer will follow the bitmask - each representing the ID of the neighbor cube. The ID specifies the index of the neighbor cube within the cubes data. A cube will often have multiple neighbors, which would mean that multiple 2-byte cube IDs will follow the bitmask.

  * Vertex IDs
    * 16 bytes = 2 bytes * 8 vertices
    * Each vertex ID is a 2 byte integer that references which vertex belongs to which corner of the cube. Each vertex ID specifies the index of the vertex within the collection of vertices found earlier in the file. For example, if the vertex ID is 0, then it is the first vertex in the list. If the vertex ID is 5, then it is the 6th vertex.
    * The order of the Vertex IDs indicates which corner of the cube it belongs to:
      * 0 = Left, Front, Top
      * 1 = Left, Front, Bottom
      * 2 = Right, Front, Bottom
      * 3 = Right, Front, Top
      * 4 = Left, Back, Top
      * 5 = Left, Back, Bottom
      * 6 = Right, Back, Bottom
      * 7 = Right, Back, Top

  * Energy Center Information

    Note: This is only present when cube is an energy center, per bitmask bit 6
    * 1 byte integer: special (TODO: Determine what this is for)
    * 1 byte integer: energy center number
    * 2 byte integer: value

  * Static Light Value
    * 2 bytes
    * The Static Light value should be interpreted as a 16-bit fixed-point number in 4.12 format. That means that 4 bits represent the integer portion of the number, and 12 bits represent the fractional portion of the number.

  * Walls Bitmask
    * 1 byte
    * Bits 0-5 of the bitmask indicate whether a specific side of the cube has a wall. If a bit is set to 1, then that means that there is a wall on that side.
      * 0 = Left
      * 1 = Top
      * 2 = Right
      * 3 = Bottom
      * 4 = Back
      * 5 = Front
    * An explanation of walls: A wall is not located on an exterior side of a cube, but rather on an interior side (e.g. a side that joins a cube to another cube). Think of two cubes that are adjacent to each other. They share a side (and the four vertices that define that side). That side normally would be open air, but a wall can be defined for that side such as a rock wall with a grate or fan. Such a wall would prevent the player from flying through it. Other types of walls allow the player to pass-through, such as the sparkling texture floating in the air of an energy generator.

  * Wall IDs
    * 1 byte integer (per wall)
    * For each wall specified by the Walls Bitmask, a 1-byte integer will follow the bitmask that represents the ID of the wall. A cube can have multiple walls, which would mean that multiple 1-byte cube IDs will follow the bitmask.
    * TODO: Determine if wall IDs can be 255 (-1), and if that represents "no wall".

  * Cube Textures
    
    Cube texture information is of a variable length, depending on whether a side has a texture, and whether or not the there a secondary texture in addition to the primary texture. 

    For each side of the cube, the side will have texture information if either of these statements are true:
    * The side is not connected to another cube. In other words, it is an exterior/disconnected side.
    * The side has a wall.

    The texture information for each side, if present, is in the same order as defined by the walls bitmask and cube neighbor bitmask: Left, Top, Right, Bottom, Back, Front. 

    * Primary Texture
      * 2 bytes
      * Bit 0: The first bit (the high bit) of the primary texture bytes indicates whether a secondary texture follows the primary texture.
      * Bits 1-15: The remaining bits (the lower 15 bits) should be interpreted as an integer that represents the ID of the primary texture on that side of the cube.

    * Secondary Texture (if present)
      * 2 byte integer
      * The ID of the secondary texture on that side of the cube.

    * UVL Information
      * 24 bytes
      * TODO: Describe the meaning of the UVL data.

### Objects
Following the mine structure data is the object data. Objects include the player(s), enemies, power-ups, etc that populate the level.

* TODO: Add specification for the object data.

## Detailed Explanation of Cubes and Vertices

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
