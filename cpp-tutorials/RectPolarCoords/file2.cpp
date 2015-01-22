// file2.cpp -- contains the functions called in file1.cpp
#include <iostream>
#include <cmath>
#include "coord_in.h"

// convert rectangular coords to polar coords
polar rect_to_polar(rect xypos)
{
  using namespace std;
  polar answer;
  
  answer.distance =
    sqrt( xypos.x*xypos.x + xypos.y*xypos.y);
  answer.angle = atan2(xypos.y, xypos.x);
  return answer;  // returns a polar struct
}

// show polar coords (must convert angle to degrees)
void show_polar(polar dapos)
{
  using namespace std;
  const double Rad_to_deg = 57.29577951;
  
  cout << "distance = " << dapos.distance;
  cout << ", angle = " << dapos.angle * Rad_to_deg;
  cout << " degrees\n";
}