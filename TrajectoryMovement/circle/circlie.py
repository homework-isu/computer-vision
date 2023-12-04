class Circle:
    def __init__(self, coords):
        self.center_x = coords[0]
        self.center_y = coords[1]
        self.coords = [coords]

    def is_right_center(self, new_coords, threshold=10):
        return ((new_coords[0] - self.center_x) ** 2 + (new_coords[1] - self.center_y) ** 2) ** 0.5 <= threshold

    def add_coords(self, coords):
        self.center_x = coords[0]
        self.center_y = coords[1]
        self.coords += [coords]

    def get_x(self):
        return [coord[0] for coord in self.coords]

    def get_y(self):
        return [coord[1] for coord in self.coords]