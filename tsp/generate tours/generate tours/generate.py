from random import uniform
from math import sqrt

n = 10
type = 'noneuclidean'
filename = 'noneuc_10'

f = open(filename, 'w+')

towrite = []
towrite.append(type)
towrite.append(str(n))
points = []
for i in range(n):
  r1 = uniform(-100.0, 100.0)
  r2 = uniform(-100.0, 100.0)
  points.append([r1, r2])
  towrite.append(str(r1) + ' ' + str(r2))

def dist(l1, l2):
    return sqrt( (l2[0] - l1[0])**2 + (l2[1] - l1[1])**2 )


mat = [ [0.0 for x in range(n)] for y in range(n) ]
for i in range(n):
    for j in range(i+1,n):
      if type=='euclidean':
        print('gotama')
        mat[i][j] = dist(points[i],points[j])
        mat[j][i] = mat[i][j]
      else:
        mat[i][j] = uniform(50.0, 150.0)
        mat[j][i] = mat[i][j]

for i in range(n):
    line = str(mat[i][0])
    for j in range(n-1):
      line = line + ' ' + str(mat[i][1+j])
    towrite.append(line)

f.write('\n'.join(towrite))
f.close()
