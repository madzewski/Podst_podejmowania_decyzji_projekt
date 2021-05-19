import random


random.seed(42)


# Config
CAPACITY = 20
RANGE = 100
X, Y = 5, 5
VALUES = (1,10)
MASS = (1,10)
CATEGORIES_N = 5
SAMPLES_N = 6

# Constants
CATEGORIES = [random.randrange(*VALUES) for _ in range(CATEGORIES_N)]


def e_dist(p1, p2):
  # Dystans euklidesowy
  return round( ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** (1/2), 3 )


class Robot:
  def __init__(self, capacity, range):
    self.capacity = capacity
    self.range = range


class Sample:
  def __init__(self, id):
    self.id = id
    self.category = random.randrange(0, CATEGORIES_N)
    self.value = CATEGORIES[self.category]
    self.mass = random.randrange(*MASS)
    self.position = (None,None)
    self.base_distance = (None,None)

  def __str__(self):
    return str(self.id)
    # return str([self.id, self.category, self.value, self.mass, self.position, self.base_distance])


class MarsMap:
  def __init__(self, x, y):
    self.x, self.y = x, y
    self.spaces = [[None for _ in range(self.y)] for _ in range(self.x)]
    self.spaces[self.x//2][self.y//2] = -1  # set base

  def __str__(self):
    output = ''
    for level in self.spaces:
      for point in level:
        output += str(point) + ' '
      output += '\n'
    return output

  def get_base(self):
    return self.x//2,self.y//2

  def push_sample(self, sample):
    while True:
      pos = (random.randrange(0, self.x), random.randrange(0, self.y))
      if self.spaces[pos[0]][pos[1]] == None:
        self.spaces[pos[0]][pos[1]] = sample
        sample.position = pos
        sample.base_distance = (round(e_dist((self.x//2,self.y//2), pos) * random.uniform(1.0, 1.1), 2),
        round(e_dist((self.x//2,self.y//2), pos) * random.uniform(1.0, 1.1), 2))
        break


class DistanceMap:
  def __init__(self, x, y, samples):
    self.x, self.y = x, y
    self.distances = [[None for _ in range(self.y)] for _ in range(self.x)]
    for i, s1 in enumerate(samples):
      for j, s2 in enumerate(samples):
        self.distances[i][j] = round(
          e_dist(s1.position, s2.position) * random.uniform(1.0, 1.1), 2)
    for i, d in enumerate(self.distances):
      d.insert(0, samples[i].base_distance[0])
    self.distances.insert(0,[0])
    for s in samples:
      self.distances[0].append(s.base_distance[1])
    

  def __str__(self):
    return '\n'.join([str(level) for level in self.distances])


def mass_constraint(capacity, decision, samples):
  sum = 0
  for i in range(len(samples)):
    sum += decision[i] * samples[i]
  if sum <= capacity:
    return True
  return False


def range_constraint(range, path, distance_map):
  sum = 0
  for i in range(len(path)):
    for j in range(len(path)):
      sum += path[i][j]*distance_map[i][j]
  if sum <= range:
    return True
  return False


def category_constraint(samples, decisions, categories):
  sum = 0
  for j in categories:
    counter = 0
    for i in range(len(decisions)):
      if samples[i].category == j:
        counter += 1
    if counter == 0:
      return False
    sum += 1
  if sum == len(categories):
    return True
  return False


def comeback_constraint(path):
  row_sum = sum([i for i in path[0][1:]])
  col_sum = sum([path[j][0] for j in range (len(path[1:])+1)])

  if row_sum + col_sum == 2:
    return True
  return False
  
  
def objective(samples, decisions):
  sum = sum([samples[i].value * decisions[i] for i in range(len(decisions))])
  return sum


robot = Robot(CAPACITY, RANGE)

mars_map = MarsMap(X,Y)

samples = [Sample(i) for i in range(SAMPLES_N)]
for sample in samples:
  mars_map.push_sample(sample)

distance_map = DistanceMap(SAMPLES_N,SAMPLES_N, samples)


# Variables
decisions = [0 for _ in range(SAMPLES_N)]
path = [[0 for _ in range(SAMPLES_N + 1)] for _ in range(SAMPLES_N + 1)]

print(mars_map)
print(distance_map)