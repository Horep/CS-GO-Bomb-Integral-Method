# CS-GO-Bomb-Integral-Method
This is an implementation of an integral based method for average bomb damage from a bombsite/section of a bombsite.

The LaTeX document details derivations for the functions within the python code.

To use the python code implementation:
A rectangular piece of bombsite is written in standard hammer coordinates in the form

    [x_0,y_0,x_1,y_1,z_0]

where (x_0,y_0) is the bottom left part of the site, and (x_1,y_1) is the top left. z_0 is the height of the planar piece.

A full bombsite can be written as a list of pieces, e.g.

    TestSite = [
        [-32, -32, 32, -16, 0],
        [16, -16, 32, 32, 0],
        [-32, 0, 0, 32, 500]
        ]

Operations can then be performed on TestSite, such as getArea which returns the area of each piece in the order they are written in TestSite, which would output 

    array([1024,  768, 1024])

The centre of the bombsite can be found using getCentroid, which returns the centre of the entire bombsite in an array. It takes in the TestSite list as well as the output of getArea, which is done for convenience elsewhere. It returns a 3x1 array of coordinates, which in this case is 

    array([  0.72727273,  -0.72727273, 181.81818182]).

==Creating a bombsite field function==
To create a bombsite field function using CreateFieldFunction, write the bombsite in rectangular pieces in a list, then write something like

    myFunction = CreateFieldFunction(mySite)

Then you can evaluate myFunction(X_p,Y_p,Z_p) to get the average damage receieved from that bombsite at position (X_p,Y_p,Z_p) in the map. This can also be used with matplotlib or anything compatible with numpy and scipy to produce graphs.

For example using the CreateFieldFunction on the TestSite above, and then evaluating at (1056,0,64) returns 39.01379338747492.
