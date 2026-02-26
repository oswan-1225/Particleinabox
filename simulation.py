"""
Main simulation file - runs the particle in a box animation.
Press the close button to exit.
"""

import pygame
import random
from particle import Particle

# Constants - feel free to modify these!
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60  # Frames per second
BACKGROUND_COLOR = (20, 20, 40)  # Dark blue background

# Particle settings
PARTICLE_RADIUS = 15
PARTICLE_COLOR = (100, 200, 255)  # Light blue
INITIAL_SPEED = 5  # How fast the particle moves

# Energy tracking
GRAPH_WIDTH = 200
GRAPH_HEIGHT = 100
GRAPH_X = WINDOW_WIDTH - GRAPH_WIDTH - 10
GRAPH_Y = 10

def particle_energy(particles):
    # Calculate the total kinetic energy of the system
    total_energy = 0
    for p in particles:
        speed_squared = p.vx**2 + p.vy**2
        total_energy += 0.5 * speed_squared  # Assuming mass = 1 for simplicity
    return total_energy

def draw_energy_graph(window, energy_history):
    """Draw energy graph in top-right corner."""
    # Draw background panel
    pygame.draw.rect(window, (30, 30, 50), (GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT))
    pygame.draw.rect(window, (200, 200, 200), (GRAPH_X, GRAPH_Y, GRAPH_WIDTH, GRAPH_HEIGHT), 2)
    
    # Draw title
    font = pygame.font.Font(None, 24)
    title = font.render("Energy", True, (200, 200, 200))
    window.blit(title, (GRAPH_X + 10, GRAPH_Y + 5))
    
    # Draw graph
    if len(energy_history) > 1:
        max_energy = max(energy_history) if energy_history else 1
        min_energy = min(energy_history) if energy_history else 0
        energy_range = max_energy - min_energy if max_energy != min_energy else 1
        
        # Draw grid lines
        for i in range(0, len(energy_history) - 1):
            x1 = GRAPH_X + 10 + (i / (len(energy_history) - 1)) * (GRAPH_WIDTH - 20)
            y1 = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i] - min_energy) / energy_range) * (GRAPH_HEIGHT - 40)
            
            x2 = GRAPH_X + 10 + ((i + 1) / (len(energy_history) - 1)) * (GRAPH_WIDTH - 20)
            y2 = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i + 1] - min_energy) / energy_range) * (GRAPH_HEIGHT - 40)
            
            pygame.draw.line(window, (100, 200, 255), (x1, y1), (x2, y2), 2)
    
    # Display current energy value and frame count
    if energy_history:
        font_small = pygame.font.Font(None, 18)
        energy_text = font_small.render(f"Current: {energy_history[-1]:.1f}", True, (100, 200, 255))
        window.blit(energy_text, (GRAPH_X + 10, GRAPH_Y + GRAPH_HEIGHT - 25))
        

def main():
    """Main function that runs the simulation."""
    # defines window size and title
    def create_window():
        pygame.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Particle in a Box")
        return window
    window = create_window()

    # Initialize energy tracking
    energy_history = []
    update_interval = 30 # updates graph every 0.5 seconds at 60fps
    
    # creates an internal clock to control frame rate
    clock = pygame.time.Clock()
    
    # defines the parameters of the particle and creates an instance of the Particle class
    # create multiple particles by creating a list of Particle instances
    
    particlecount = 15

    particles = []
    for _ in range(particlecount):
        particle = Particle(
            x=random.randint(PARTICLE_RADIUS, WINDOW_WIDTH - PARTICLE_RADIUS),
            y=random.randint(PARTICLE_RADIUS, WINDOW_HEIGHT - PARTICLE_RADIUS),
            vx=INITIAL_SPEED if random.random() > 0.5 else -INITIAL_SPEED,
            vy=INITIAL_SPEED if random.random() > 0.5 else -INITIAL_SPEED,
            radius=PARTICLE_RADIUS,
            color=PARTICLE_COLOR
        )
        particles.append(particle)
    
    # Main game loop
    running = True
    frame_count = 0
    while running:
        
        # if the user clicks the close button, exit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #calls the move and bounce_off_walls methods of the particle to update its position and handle wall collisions
        for p in particles:
            p.move()
            p.bounce_off_walls(WINDOW_WIDTH, WINDOW_HEIGHT)

        #checks for particle-particle collisions and calls the bounce_off_particle method if a collision is detected
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                p1 = particles[i]
                p2 = particles[j]
                p1.bounce_off_particle(p2)
        
        # creates a background color
        window.fill(BACKGROUND_COLOR)
        
        #Displays the particles as circles
        for p in particles:
            pygame.draw.circle(window, p.color, (int(p.x), int(p.y)), p.radius)

        # prints total energy of the system to the console
        frame_count += 1
        total_energy = particle_energy(particles)
        
        if frame_count % update_interval == 0:
            energy_history.append(total_energy)
            if len(energy_history) > 100:  # Limit history length to avoid memory issues
                energy_history.pop(0)

        # Draw energy graph
        draw_energy_graph(window, energy_history)

        
        # update the display to show the new frame
        pygame.display.flip()
        
        # maintains 60fps
        clock.tick(FPS)
    
    # closes pygame when loop closes
    pygame.quit()

# This line ensures that the main function runs when the script is executed directly
if __name__ == "__main__":
    main()
