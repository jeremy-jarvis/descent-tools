# To Do

The following are potential improvements that could be made to the level parser:

* Look deeper into vertex byte order. The vertex bytes seem to be in Z, Y, X order. Interpreting the vertex data in that order allows the resulting OBJ file to look correct when it is loaded into Blender. Further analysis may be needed to ensure that this interpretation is correct.
* Add parsing for end of exit tunnel information in cube neighbor bitmask. A value of -2 signifies the end of the exit tunnel.
* Determine what the properties of an energy center mean. Update relevant details in level spec.
* Add information about the differences of parsing a shareware file.
* According to descent2.com, the "special" property of an energy center is a unsigned int. Does the parsing of that value need to change? What about the level spec?
* Find out what the static light value is for, and add a description to the spec.
