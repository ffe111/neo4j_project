#! /usr/bin/env python3
""" compass_16point_planB.py: Get compass directions from a vector

                   N
             NNW       NNE

        NW                  NE

     WNW                      ENE

   W               .             E

     WSW                      ESE

        SW                  SE

             SSW       SSE
                   S

The angles used in this program assume due East is 0 degrees,
and the circle has 360 degrees, 0..359, and 360 is another name
for 0.
"""
import math

def get_compass_direction(*,vector):
    numerator = (vector[1][1] - vector[0][1])
    denominator = (vector[1][0] - vector[0][0])
    if denominator == 0:
        if numerator >= 0:
            angle = 90
        else:
            angle = 270
    elif numerator == 0:
        if denominator >= 0:
            angle = 0
        else:
            angle = 180
    else:
        fraction = (numerator / denominator)
        # get angle in degrees
        fval=math.degrees(math.atan(fraction))
        # magic.... to get rounding right
        angle = int(math.ceil(round(fval,1)))
        # adjust for quadrant if not quadrant I
        if (denominator < 0): # quandrants II & III
            angle += 180
        elif (numerator < 0): # quandrant IV
            angle += 360
    slotno = ((angle-HALF_SLOTSIZE) // SLOTSIZE) # rotate CLOCKWISE half_slotsize
    # that might move 1/2 of the "E" negative, so fix that special case
    if (slotno < 0):
        slotno = 0.0  # fix the special case
    else:
        slotno += 1.0 # remember, rotate CLOCKWISE by 1
    slotno = int(slotno) % POINT_COUNT
    try:
        retval = DIRECTIONS[slotno]
    except IndexError as xcpn:
        print(f"slotno={slotno:d}, angle={angle:f}:{str(xcpn)}")
    return retval

def main():
    retval = EXIT_SUCCESS
    vectors = (((0.0,  0.0), (1.0,  0.0),"E"),
               ((0.0,  0.0), (math.cos(math.radians(1)), math.sin(math.radians(1))), "E"),
               ((0.0,  0.0), (math.cos(math.radians(359)), math.sin(math.radians(359))), "E"),
               ((0.0,  0.0), (COS_22_5,  SIN_22_5),"ENE"),
               ((0.0,  0.0), (SQR_ROOT_2,  SQR_ROOT_2),"NE"),
               ((0.0,  0.0), (SIN_22_5,  COS_22_5),"NNE"),
               ((0.0,  0.0), (0.0,  1.0),"N"),
               ((0.0,  0.0), (-SIN_22_5,  COS_22_5),"NNW"),
               ((0.0,  0.0), (-SQR_ROOT_2,  SQR_ROOT_2),"NW"),
               ((0.0,  0.0), (-COS_22_5,  SIN_22_5),"WNW"),
               ((0.0,  0.0), (-1.0,  0.0),"W"),
               ((0.0,  0.0), (math.cos(math.radians(179)), math.sin(math.radians(179))), "W"),
               ((0.0,  0.0), (math.cos(math.radians(181)), math.sin(math.radians(181))), "W"),
               ((0.0,  0.0), (-COS_22_5,  -SIN_22_5),"WSW"),
               ((0.0,  0.0), (-SQR_ROOT_2, -SQR_ROOT_2),"SW"),
               ((0.0,  0.0), (-SIN_22_5,  -COS_22_5),"SSW"),
               ((0.0,  0.0), (0.0, -1.0),"S"),
               ((0.0,  0.0), (SIN_22_5, -COS_22_5),"SSE"),
               ((0.0,  0.0), (SQR_ROOT_2, -SQR_ROOT_2),"SE"),
               ((0.0,  0.0), (COS_22_5, -SIN_22_5),"ESE"))
    for vector in vectors:
        print(f"From {vector[0]} to {vector[1]}, expected {vector[2]:s}, got ",end="")
        compass_direction = get_compass_direction(vector=(vector[0],vector[1]))
        print(compass_direction,end=", ")
        if vector[2] != compass_direction:
            print("FAIL")
            retval = EXIT_FAILURE
        else:
            print("PASS")
    return retval

# These globals are for get_compass_direction()
DIRECTIONS = ["East","East North East","North East","North North East","North","North North West","North West","West North West",
              "West","West South West","South West","South South West","South","South South East","South East","East South East"]
# number of directions (pie slices, points in compass rose)
POINT_COUNT = len(DIRECTIONS)
# map from angle in degrees to direction name
SLOTSIZE = (360 / POINT_COUNT)
HALF_SLOTSIZE = SLOTSIZE / 2 # amount to rotate CLOCKWISE

# The following globals are for the test harness in main()
DBUG = False
SIN_22_5 = 0.3826834323650898 # sin(22.5 degrees)
COS_22_5 = 0.9238795325112867 # cos(22.5 degrees)
SQR_ROOT_2 = 1.4142135623730951
EXIT_SUCCESS, EXIT_FAILURE = 0, 1
if __name__ == '__main__':
    raise SystemExit(main())
