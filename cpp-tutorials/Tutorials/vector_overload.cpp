// vectors - overloading operators example
#include <iostream>
using namespace std;

class CVector {
	public:
		int x,y;
		CVector () {};	// used as (parameters)
		CVector (int,int); // prototype function
		CVector operator + (CVector); //overloading operators of form:
		// type operator sign (parameters) { /*...*/ }
		// 
};

CVector::CVector (int a, int b) {	// declaration of function CVector
	x = a;
	y = b;
}

CVector CVector::operator+ (CVector param) {
	CVector temp;
	temp.x = x + param.x;
	temp.y = y + param.y;
	return (temp);
}

int main () {
	CVector a (3,1);
	CVector b (1,2);
	CVector c;
	c = a+ b;
	cout << c.x << ", " << c.y << endl;
	return 0;
}
