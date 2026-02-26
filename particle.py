"""
Particle class for the simulation.
A particle has a position, velocity, size, and color.
"""

class Particle:
    def __init__(self, x, y, vx, vy, radius=10, color=(255, 255, 255)):
        """
        Initialize a particle.
        
        Args:
            x: Starting x position
            y: Starting y position
            vx: Velocity in x direction (pixels per frame)
            vy: Velocity in y direction (pixels per frame)
            radius: Size of the particle (default: 10)
            color: RGB color tuple (default: white)
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
        # Checks if particle hits left or right wall
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.vx = -self.vx

        
        #Checks if particle hits top or bottom wall  
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.vy = -self.vy
        pass

    def bounce_off_particle(self, other):
        # Checks to see if particles collides with another particle and bounces off:
        ox = other.x - self.x
        oy = other.y - self.y
        distance_squared = ox**2 + oy**2
        radius_sum = self.radius + other.radius
        if distance_squared < radius_sum**2:
            # transfers some of the "energy" as velocity to the other particles
            transfer_factor = 0.1 

            # Simple elastic collision response (not physically accurate)
            self.vx, other.vx = other.vx, self.vx
            self.vy, other.vy = other.vy, self.vy

            # Transfer energy: self loses, other gains
            energy_x = transfer_factor * self.vx
            energy_y = transfer_factor * self.vy
            
            self.vx -= energy_x
            self.vy -= energy_y
            other.vx += energy_x
            other.vy += energy_y