"""
Main simulation file - runs the particle in a box animation.
Press the close button to exit.
"""

import pygame
import random
import math
from particle import Particle

# Constants - feel free to modify these!
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
FPS = 60  # Frames per second
BACKGROUND_COLOR = (20, 20, 40)  # Dark blue background

# Particle settings
PARTICLE_RADIUS = 5
PARTICLE_COLOR = (255, 192, 203) # pink particles
PARTICLE_COLOR_2 = (255, 215, 0) # gold particles
INITIAL_SPEED= 5  # Pink speed
INITIAL_SPEED_2 = 5 # Gold Speed

# Bond settings
BOND_DISTANCE = PARTICLE_RADIUS * 3.0  # Distance threshold to create bond
BOND_COLOR = (220, 220, 255)  # Color of rigid bar between bonded particles
BOND_WIDTH = 2

# Energy tracking
GRAPH_WIDTH = 200
GRAPH_HEIGHT = 100
GRAPH_X = WINDOW_WIDTH - GRAPH_WIDTH - 10
GRAPH_Y = 10

def particle_energy(particles):
    # Calculate the total kinetic energy of the system
    total_energy_pink = 0
    total_energy_gold = 0
    for p in particles:
        speed_squared = p.vx**2 + p.vy**2
        if p.color == PARTICLE_COLOR:
            total_energy_pink += 0.5 * speed_squared
        else:
            total_energy_gold += 0.5 * speed_squared
    return total_energy_pink, total_energy_gold

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
        max_energy_pink = max(energy_history, key=lambda x: x[0])[0] if energy_history else 1
        min_energy_pink = min(energy_history, key=lambda x: x[0])[0] if energy_history else 0
        energy_range_pink = max_energy_pink - min_energy_pink if max_energy_pink != min_energy_pink else 1

        max_energy_gold = max(energy_history, key=lambda x: x[1])[1] if energy_history else 1
        min_energy_gold = min(energy_history, key=lambda x: x[1])[1] if energy_history else 0
        energy_range_gold = max_energy_gold - min_energy_gold if max_energy_gold != min_energy_gold else 1

        # Draw grid lines
        for i in range(0, len(energy_history) - 1):
            x1 = GRAPH_X + 10 + (i / (len(energy_history) - 1)) * (GRAPH_WIDTH - 20)
            y1_pink = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i][0] - min_energy_pink) / energy_range_pink) * (GRAPH_HEIGHT - 40)
            y1_gold = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i][1] - min_energy_gold) / energy_range_gold) * (GRAPH_HEIGHT - 40)
            x2 = GRAPH_X + 10 + ((i + 1) / (len(energy_history) - 1)) * (GRAPH_WIDTH - 20)
            y2_pink = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i + 1][0] - min_energy_pink) / energy_range_pink) * (GRAPH_HEIGHT - 40)
            y2_gold = GRAPH_Y + GRAPH_HEIGHT - 10 - ((energy_history[i + 1][1] - min_energy_gold) / energy_range_gold) * (GRAPH_HEIGHT - 40)

            pygame.draw.line(window, (255, 192, 203), (x1, y1_pink), (x2, y2_pink), 2)
            pygame.draw.line(window, (255, 215, 0), (x1, y1_gold), (x2, y2_gold), 2)  # Gold line slightly below pink for visibility
    
    # Display current energy value and frame count
    if energy_history:
        font_small = pygame.font.Font(None, 18)
        energy_text_pink = font_small.render(f"Pink: {energy_history[-1][0]:.2f}", True, PARTICLE_COLOR)
        energy_text_gold = font_small.render(f"Gold: {energy_history[-1][1]:.2f}", True, PARTICLE_COLOR_2)
        window.blit(energy_text_pink, (GRAPH_X + 10, GRAPH_Y + GRAPH_HEIGHT - 45))
        window.blit(energy_text_gold, (GRAPH_X + 10, GRAPH_Y + GRAPH_HEIGHT - 25))


def enforce_bond(p1, p2, bond_length):
    """Apply a rigid-distance constraint between two bonded particles."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist = math.hypot(dx, dy)

    if dist == 0:
        return

    nx = dx / dist
    ny = dy / dist

    # Positional correction to keep bar length fixed
    offset = (dist - bond_length) / 2
    p1.x += nx * offset
    p1.y += ny * offset
    p2.x -= nx * offset
    p2.y -= ny * offset

    # Remove relative velocity along bond normal to keep rigid behavior
    rvx = p2.vx - p1.vx
    rvy = p2.vy - p1.vy
    vel_along_normal = rvx * nx + rvy * ny
    correction_vx = nx * vel_along_normal / 2
    correction_vy = ny * vel_along_normal / 2
    p1.vx += correction_vx
    p1.vy += correction_vy
    p2.vx -= correction_vx
    p2.vy -= correction_vy

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

    ###
    particlecount = 100 # Number of particles in the simulation
    ###

    particles = []
    max_spawn_attempts = 500
    for i in range(particlecount):
        color = PARTICLE_COLOR if i < particlecount // 2 else PARTICLE_COLOR_2
        vx = INITIAL_SPEED if color == PARTICLE_COLOR else INITIAL_SPEED_2
        vy = INITIAL_SPEED if color == PARTICLE_COLOR else INITIAL_SPEED_2

        spawned_particle = None
        for _ in range(max_spawn_attempts):
            x = random.randint(PARTICLE_RADIUS, WINDOW_WIDTH - PARTICLE_RADIUS)
            y = random.randint(PARTICLE_RADIUS, WINDOW_HEIGHT - PARTICLE_RADIUS)

            overlaps_existing = any(
                (x - p.x) ** 2 + (y - p.y) ** 2 < (PARTICLE_RADIUS + p.radius) ** 2
                for p in particles
            )
            if not overlaps_existing:
                spawned_particle = Particle(
                    x=x,
                    y=y,
                    vx=vx if random.random() > 0.5 else -vx,
                    vy=vy if random.random() > 0.5 else -vy,
                    radius=PARTICLE_RADIUS,
                    color=color
                )
                break

        if spawned_particle is not None:
            particles.append(spawned_particle)
        else:
            print(f"Could only place {len(particles)} particles without overlap. Reduce radius or count.")
            break

    print(f"Configured particle radius: {PARTICLE_RADIUS}")
    if particles:
        print(f"Spawned particles: {len(particles)} | Actual particle radius: {particles[0].radius}")
    else:
        print("Spawned particles: 0")

    # Store bonds as {(i, j): bond_length}
    bonds = {}
    
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

                # Create same-color bonds when particles get close enough
                if p1.sametypebonding(p2, bond_distance=BOND_DISTANCE):
                    pair_key = (i, j)
                    if pair_key not in bonds:
                        bond_length = math.hypot(p2.x - p1.x, p2.y - p1.y)
                        bonds[pair_key] = max(bond_length, p1.radius + p2.radius)

        # Enforce rigid bar constraints for all bonded pairs
        for (i, j), bond_length in bonds.items():
            enforce_bond(particles[i], particles[j], bond_length)
        
        # creates a background color
        window.fill(BACKGROUND_COLOR)

        # Draw rigid bars between bonded particles
        for i, j in bonds:
            p1 = particles[i]
            p2 = particles[j]
            pygame.draw.line(window, BOND_COLOR, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), BOND_WIDTH)
        
        #Displays the particles as circles
        for p in particles:
            pygame.draw.circle(window, p.color, (int(p.x), int(p.y)), p.radius)

        # prints total energy of the system to the console
        frame_count += 1
        total_energy_pink, total_energy_gold = particle_energy(particles)
        
        if frame_count % update_interval == 0:
            energy_history.append((total_energy_pink, total_energy_gold))
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
