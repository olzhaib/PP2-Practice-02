
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(self.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y

    def dist(self, point):
        dx = point.x - self.x
        dy = point.y - self.y
        return (dx ** 2 + dy ** 2) ** 0.5


point1 = Point(0, 0)
point2 = Point(6, 8)

point1.show()
point1.move(2, 5)
point1.show()

print(point1.dist(point2))
