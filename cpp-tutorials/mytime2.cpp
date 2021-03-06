// mytime2.cpp -- implementing Time methods
#include <iostream>
#include "mytime2.h"

Time::Time()
{
  hours = minutes = 0;
}

Time::Time(int h, int m)
{
  hours = h;
  minutes = m;
}

void Time::AddMin(int m)
{
  minutes += m;
  hours += minutes/60;
  minutes %= 60;
}

void Time::AddHr(int h)
{
  hours += h;
}

void Time::Reset(int h, int m)
{
  hours = h;
  minutes = m;
}

Time Time::operator+(const Time & t) const
{
  Time sum;
  sum.minutes = minutes + t.minutes;
  sum.hours = hours + t.hours + sum.minutes/60;
  sum.minutes %= 60;
  return sum;
}

Time Time::Sum(const Time & t) const
{
  Time sum;
  sum.minutes = minutes + t.minutes;
  sum.hours = hours + t.hours + sum.minutes/60;
  sum.minutes %= 60;
  return sum;
}

Time Time::operator-(const Time & t) const
{
  Time diff;
  int tot1, tot2;
  tot1 = t.minutes + 60 * t.hours;
  tot2 = minutes + 60 * hours;
  diff.minutes = (tot2 - tot1) % 60;
  diff.hours = (tot2 - tot1) / 60;
  return diff;
}

Time Time::operator*(double mult) const
{
  Time prod;
  long totalminutes = hours * mult * 60 + minutes * mult;
  prod.hours = totalminutes / 60;
  prod.minutes = totalminutes % 60;
  return prod;
}

void Time::Show() const
{
  std::cout << hours << " hours, " << minutes << " minutes";
}

// this is called implicitly
void Time::set_now(int set)
{
  set_later = set;
}

void Time::Min2(int min2)
{
  AddMin(min2 * 2);
}


