"""
Particle class for the simulation.
A particle has a position, velocity, size, and color.
"""
import math as m

class Particle:
    def __init__(self, x, y, vx, vy, radius=10, color=(255, 255, 255)):
        """
        Initialize a particle.
        
        Args:
            x: Starting x position
            y: Starting y position
            vx: Velocity in x direction (pixels per frame)
            vy: Velocity in y direction (pixels per frame)
            radius: Size of the particle 
            color: RGB color tuple 
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        pass

    def move(self):

        # Update the particle's position based on its velocity
        self.x += self.vx
        self.y += self.vy

        pass

    
    def bounce_off_walls(self, width, height):
        """
        Check if particle hits the walls and reverse direction if needed.
        
        Args:
            width: Width of the box/window
            height: Height of the box/window
        """
        # Check horizontal walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx = -abs(self.vx)

        # Check vertical walls
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.vy = -abs(self.vy)
        

    def bounce_off_particle(self, other):
        # Checks to see if particles collides with another particle and bounces off:
        dx = other.x - self.x
        dy = other.y - self.y
        dist_sq = dx * dx + dy * dy # distance squared between centers
        min_dist = self.radius + other.radius

        #no collision
        if dist_sq >= min_dist * min_dist:
            return

        # Handle overlap
        if dist_sq == 0:
            nx, ny = 1.0, 0.0
            dist = 1.0
        else:
            dist = m.sqrt(dist_sq)
            nx = dx / dist
            ny = dy / dist
        
        # rel velo
        rvx = other.vx - self.vx
        rvy = other.vy - self.vy

        # speed along normal
        vel_along_normal = rvx * nx + rvy * ny

        # resolve overlap if colliding
        if vel_along_normal > 0:
            penetration = min_dist - dist
            if penetration > 0:
                correction = penetration / 2
                self.x -= correction * nx
                self.y -= correction * ny
                other.x += correction * nx
                other.y += correction * ny
            return
        
        # Elastic collision response (m1 = m2 = 1 for simplicity)
              #m1   #m2
        j = -(1.0 + 1.0) * vel_along_normal / 2
        impulse_x = j * nx
        impulse_y = j * ny

        self.vx -= impulse_x
        self.vy -= impulse_y
        other.vx += impulse_x
        other.vy += impulse_y

        # Handle overlap after collision response
        penetration = min_dist - dist
        if penetration > 0:
            correction = penetration / 2
            self.x -= correction * nx
            self.y -= correction * ny
            other.x += correction * nx
            other.y += correction * ny
    
