// virtual members example
// a virtual member is a member of a class that can be redefined in its dervied classes

#include <iostream>
using namespace std;

class CPolygon {
	protected:
		int width, height;
	public:
		void set_values (int a, int b)
			{ width = a; height = b; }
		virtual int area () // defined as virtual in base because later it is redefined
			{ return (0); }
	};

class CRectangle: public CPolygon {
	public: 
		int area ()
			{ return (width * height); }
	};

class CTriangle: public CPolygon {
	public:
		int area ()
			{ return (width*height/2); };
	};

int main () {
	CRectangle rect;
	CTriangle trgl;
	CPolygon poly;
	CPolygon * ppoly1 = &rect;
	CPolygon * ppoly2 = &trgl;
	CPolygon * ppoly3 = &poly;
	ppoly1 ->set_values (4,5); 	// set_values.*ppoly1
	ppoly2 ->set_values (4,5);
	ppoly3 ->set_values (4,5);
	cout << ppoly1 ->area() << endl;
	cout << ppoly2 ->area() << endl;
	cout << ppoly3 ->area() << endl;
	return 0;
}

