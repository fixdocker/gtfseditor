#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import radians, degrees, acos, cos, sin, asin, sqrt, atan
import cmath

EARTH_RADIUS = 6371

# Complex-number utility functions
def headingC(n1,n2):
  """Returns a complex number representing a heading"""
  p1 = (float(n1['lat'])+float(n1['lon'])*1j)
  p2 = (float(n2['lat'])+float(n2['lon'])*1j)

  assert p1 != p2, "points should be different"
  u = (p2-p1)/abs(p2-p1)
  #n = {'lat':u.real,'lon':u.imag}
  return u

def leftHand(point,heading,offset):
  p = (float(point['lat'])+float(point['lon'])*1j)
  EARTH_RADIUS = 6371000 # en metros
  ang = degrees(offset/EARTH_RADIUS)
  o = p + ang*heading*(1j)
  return {'lat':o.real,'lon':o.imag}

def haversineDict(p1,p2):
  """
  Calculate great circle distance between two points on earth, 
  given in decimal degrees.
  """
  EARTH_RADIUS = 6371
  # Convert decimal to radians
  lon1,lat1 = map(radians,map(float,[p1['lon'],p1['lat']]))
  lon2,lat2 = map(radians,map(float,[p2['lon'],p2['lat']]))

  # haversine formula
  s = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)
  # clamping to avoid domain error
  s = min(max(s,-1.0),1.0)
  arc = acos(s)
  km = EARTH_RADIUS * arc
  return km

def tripLength(tripShape):
  """
  Takes a list of dicts {lat:"",lon:""} point and returns the 
  curve lenght
  """
  ac = 0
  lastPt = tripShape[0]
  for pt in tripShape[1:]:
    ac += haversineDict(lastPt,pt)
    lastPt = pt
  return ac

def mPoint(n1,n2,s0):
  EARTH_RADIUS = 1
  p1 = EARTH_RADIUS*(float(n1['lat'])+float(n1['lon'])*1j)
  p2 = EARTH_RADIUS*(float(n2['lat'])+float(n2['lon'])*1j)
  s = EARTH_RADIUS*(float(s0['lat'])+float(s0['lon'])*1j)
  
  assert p1 <> p2
  u = (p2-p1)
  d = abs(u)
  t0 = - ( ( (p1-s)*(u).conjugate() ).real ) / d**2
  nearest = p1 + t0 * u
  
  n = {'lat':nearest.real,'lon':nearest.imag}
  between = False
  if 0<=t0<=1:
    between = True
  
  return between,n

def snapPointToPolygon(point, polygon):
  allInterpolators = []
  allCorners = []
  accumulated = 0
  for i in range(len(polygon)-1):
    # find nearest corner node
    p1 = polygon[i]
    p2 = polygon[i+1]
    if p1 == p2:
      continue
    heading = headingC(p1,p2)
    length = tripLength([p1,p2])
    d1 = haversineDict(point,p1)
    d2 = haversineDict(point,p2)
    cornerSol = {'heading':heading}
    if d1 <= d2:
      cornerSol.update({'node':p1,'dist':d1,'traveled':accumulated})
    else:
      cornerSol.update({'node':p2,'dist':d2,'traveled':accumulated + length})
    allCorners.append(cornerSol)

    b,n = mPoint(p1, p2, point)
    if b:
      mSol = {'heading':heading, 
        'node': n, 
        'dist':haversineDict(point,n), 
        'traveled': accumulated + tripLength([p1,n])}
      allInterpolators.append(mSol)    

    accumulated += length

  nearestCorner = min(allCorners,key=lambda x:x['dist'])
  if allInterpolators:
    nearestInterpolator = min(allInterpolators,key=lambda x:x['dist'])
  else:
    nearestInterpolator = []

  if nearestInterpolator:
    if nearestInterpolator['dist'] <= nearestCorner['dist']:
      snap = nearestInterpolator
    else:
      snap = nearestCorner
  else:
    snap = nearestCorner

  return snap