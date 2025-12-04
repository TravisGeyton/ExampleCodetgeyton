import pygame
import sys
import time
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 700
GRAPH_AREA = pygame.Rect(50, 50, 700, 600)
CONTROL_AREA = pygame.Rect(800, 50, 350, 600)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (240, 240, 240)
GREEN = (16, 185, 129)
RED = (239, 68, 68)
BLUE = (59, 130, 246)
DARK_BLUE = (37, 99, 235)
SLATE = (100, 116, 139)
LIGHT_BLUE = (219, 234, 254)

# Fonts
FONT_LARGE = pygame.font.Font(None, 32)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 20)

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.radius = 24
    
    def draw(self, screen, color, border_color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, border_color, (self.x, self.y), self.radius, 3)
        text = FONT_MEDIUM.render(self.id, True, BLACK if color == WHITE else WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
    
    def contains_point(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2

class Edge:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    
    def draw(self, screen, highlighted=False):
        color = BLUE if highlighted else SLATE
        thickness = 3 if highlighted else 2
        
        # Calculate arrow direction
        dx = self.to_node.x - self.from_node.x
        dy = self.to_node.y - self.from_node.y
        length = (dx ** 2 + dy ** 2) ** 0.5
        
        if length == 0:
            return
        
        # Unit vector
        ux = dx / length
        uy = dy / length
        
        # End point adjusted for node radius
        end_x = self.to_node.x - ux * self.to_node.radius
        end_y = self.to_node.y - uy * self.to_node.radius
        
        # Draw line
        pygame.draw.line(screen, color, (self.from_node.x, self.from_node.y), 
                        (end_x, end_y), thickness)
        
        # Draw arrowhead
        arrow_size = 10
        angle = 0.5
        left_x = end_x - arrow_size * (ux * pygame.math.Vector2(1, 0).rotate_rad(angle).x - 
                                       uy * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
        left_y = end_y - arrow_size * (ux * pygame.math.Vector2(1, 0).rotate_rad(angle).y + 
                                       uy * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
        
        right_x = end_x - arrow_size * (ux * pygame.math.Vector2(1, 0).rotate_rad(-angle).x - 
                                        uy * pygame.math.Vector2(1, 0).rotate_rad(-angle).y)
        right_y = end_y - arrow_size * (ux * pygame.math.Vector2(1, 0).rotate_rad(-angle).y + 
                                        uy * pygame.math.Vector2(1, 0).rotate_rad(-angle).x)
        
        pygame.draw.polygon(screen, color, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])
        
        # Draw weight label
        mid_x = (self.from_node.x + end_x) // 2
        mid_y = (self.from_node.y + end_y) // 2
        
        # Background for weight
        weight_text = FONT_SMALL.render(str(self.weight), True, color)
        text_rect = weight_text.get_rect(center=(mid_x, mid_y))
        padding = 5
        bg_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, WHITE, bg_rect)
        pygame.draw.rect(screen, color, bg_rect, 1)
        screen.blit(weight_text, text_rect)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
    
    def draw(self, screen):
        color = tuple(max(0, c - 20) for c in self.color) if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surf = FONT_SMALL.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class ShortestPathVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shortest Path Visualizer - Pygame")
        self.clock = pygame.time.Clock()
        
        # Initialize graph
        self.nodes = {
            'A': Node('A', 150, 150),
            'B': Node('B', 350, 150),
            'C': Node('C', 550, 150),
            'D': Node('D', 350, 300),
            'E': Node('E', 150, 300)
        }
        
        self.edges = [
            Edge(self.nodes['A'], self.nodes['B'], 4),
            Edge(self.nodes['A'], self.nodes['E'], 2),
            Edge(self.nodes['B'], self.nodes['C'], 3),
            Edge(self.nodes['B'], self.nodes['D'], 1),
            Edge(self.nodes['C'], self.nodes['D'], 2),
            Edge(self.nodes['D'], self.nodes['E'], 3),
            Edge(self.nodes['E'], self.nodes['B'], 7)
        ]
        
        self.start_node = 'A'
        self.end_node = 'C'
        self.algorithm = 'dijkstra'
        self.result = None
        
        # UI Elements
        self.run_button = Button(820, 200, 310, 40, "Run Algorithm", BLUE)
        self.clear_button = Button(820, 250, 310, 40, "Clear Result", RED)
        
        self.dijkstra_button = Button(820, 320, 150, 35, "Dijkstra", DARK_BLUE)
        self.bellman_button = Button(980, 320, 150, 35, "Bellman-Ford", DARK_BLUE)
        
        # Input state
        self.adding_edge_from = None
        self.weight_input = ""
        self.input_active = False
    
    def dijkstra(self, start, end):
        start_time = time.perf_counter()
        
        graph = defaultdict(list)
        for edge in self.edges:
            graph[edge.from_node.id].append((edge.to_node.id, edge.weight))
        
        distances = {node: float('inf') for node in self.nodes}
        previous = {node: None for node in self.nodes}
        unvisited = set(self.nodes.keys())
        visit_order = []
        
        distances[start] = 0
        
        while unvisited:
            current = min(unvisited, key=lambda node: distances[node])
            
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            
            # Only add to visit_order if it's not the start node
            if current != start:
                visit_order.append(current)
            
            if current == end:
                break
            
            for neighbor, weight in graph[current]:
                alt = distances[current] + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        end_time = time.perf_counter()
        
        return {
            'distance': distances[end],
            'path': path if distances[end] != float('inf') else [],
            'execution_time': (end_time - start_time) * 1000,
            'visit_order': visit_order,
            'algorithm': 'Dijkstra'
        }
    
    def bellman_ford(self, start, end):
        start_time = time.perf_counter()
        
        distances = {node: float('inf') for node in self.nodes}
        previous = {node: None for node in self.nodes}
        visit_order = []
        
        distances[start] = 0
        
        # Relax edges V-1 times
        for _ in range(len(self.nodes) - 1):
            updated = False
            for edge in self.edges:
                if distances[edge.from_node.id] != float('inf'):
                    alt = distances[edge.from_node.id] + edge.weight
                    if alt < distances[edge.to_node.id]:
                        distances[edge.to_node.id] = alt
                        previous[edge.to_node.id] = edge.from_node.id
                        updated = True
                        if edge.to_node.id not in visit_order and edge.to_node.id != start:
                            visit_order.append(edge.to_node.id)
            if not updated:
                break
        
        # Check for negative cycles
        for edge in self.edges:
            if distances[edge.from_node.id] != float('inf'):
                if distances[edge.from_node.id] + edge.weight < distances[edge.to_node.id]:
                    end_time = time.perf_counter()
                    return {
                        'error': 'Negative cycle detected',
                        'execution_time': (end_time - start_time) * 1000,
                        'algorithm': 'Bellman-Ford'
                    }
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        end_time = time.perf_counter()
        
        return {
            'distance': distances[end],
            'path': path if distances[end] != float('inf') else [],
            'execution_time': (end_time - start_time) * 1000,
            'visit_order': visit_order,
            'algorithm': 'Bellman-Ford'
        }
    
    def run_algorithm(self):
        if self.algorithm == 'dijkstra':
            self.result = self.dijkstra(self.start_node, self.end_node)
        else:
            self.result = self.bellman_ford(self.start_node, self.end_node)
    
    def is_path_edge(self, edge):
        if not self.result or 'path' not in self.result:
            return False
        path = self.result['path']
        for i in range(len(path) - 1):
            if path[i] == edge.from_node.id and path[i + 1] == edge.to_node.id:
                return True
        return False
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw title
        title = FONT_LARGE.render("Shortest Path Visualizer", True, BLACK)
        self.screen.blit(title, (50, 10))
        
        # Draw graph area background
        pygame.draw.rect(self.screen, LIGHT_GRAY, GRAPH_AREA, border_radius=10)
        pygame.draw.rect(self.screen, DARK_GRAY, GRAPH_AREA, 2, border_radius=10)
        
        # Draw edges
        for edge in self.edges:
            highlighted = self.is_path_edge(edge)
            edge.draw(self.screen, highlighted)
        
        # Draw nodes
        for node_id, node in self.nodes.items():
            if self.result and node_id in self.result.get('path', []):
                color = BLUE
                border = DARK_BLUE
            elif node_id == self.start_node:
                color = GREEN
                border = GREEN
            elif node_id == self.end_node:
                color = RED
                border = RED
            else:
                color = WHITE
                border = SLATE
            node.draw(self.screen, color, border)
        
        # Draw control panel
        pygame.draw.rect(self.screen, LIGHT_GRAY, CONTROL_AREA, border_radius=10)
        pygame.draw.rect(self.screen, DARK_GRAY, CONTROL_AREA, 2, border_radius=10)
        
        # Configuration section
        config_text = FONT_MEDIUM.render("Configuration", True, BLACK)
        self.screen.blit(config_text, (820, 60))
        
        # Start/End node selection
        start_text = FONT_SMALL.render(f"Start: {self.start_node}", True, BLACK)
        self.screen.blit(start_text, (820, 100))
        
        end_text = FONT_SMALL.render(f"End: {self.end_node}", True, BLACK)
        self.screen.blit(end_text, (820, 130))
        
        instruction1 = FONT_SMALL.render("Left-click node: Set Start", True, SLATE)
        self.screen.blit(instruction1, (820, 155))
        
        instruction2 = FONT_SMALL.render("Right-click node: Set End", True, SLATE)
        self.screen.blit(instruction2, (820, 175))
        
        # Buttons
        self.run_button.draw(self.screen)
        self.clear_button.draw(self.screen)
        
        # Algorithm selection
        algo_text = FONT_SMALL.render("Algorithm:", True, BLACK)
        self.screen.blit(algo_text, (820, 295))
        
        self.dijkstra_button.draw(self.screen)
        self.bellman_button.draw(self.screen)
        
        # Highlight selected algorithm
        if self.algorithm == 'dijkstra':
            pygame.draw.rect(self.screen, BLUE, self.dijkstra_button.rect, 3, border_radius=5)
        else:
            pygame.draw.rect(self.screen, BLUE, self.bellman_button.rect, 3, border_radius=5)
        
        # Results section
        if self.result:
            results_y = 380
            results_text = FONT_MEDIUM.render("Results", True, BLACK)
            self.screen.blit(results_text, (820, results_y))
            results_y += 35
            
            if 'error' in self.result:
                error_text = FONT_SMALL.render(self.result['error'], True, RED)
                self.screen.blit(error_text, (820, results_y))
            else:
                algo = FONT_SMALL.render(f"Algorithm: {self.result['algorithm']}", True, BLACK)
                self.screen.blit(algo, (820, results_y))
                results_y += 25
                
                dist_str = "∞" if self.result['distance'] == float('inf') else str(self.result['distance'])
                dist = FONT_SMALL.render(f"Distance: {dist_str}", True, BLACK)
                self.screen.blit(dist, (820, results_y))
                results_y += 25
                
                path_str = " → ".join(self.result['path']) if self.result['path'] else "None"
                path = FONT_SMALL.render(f"Path: {path_str}", True, BLUE)
                self.screen.blit(path, (820, results_y))
                results_y += 25
                
                time_text = FONT_SMALL.render(f"Time: {self.result['execution_time']:.4f} ms", True, BLACK)
                self.screen.blit(time_text, (820, results_y))
                results_y += 25
                
                visited = FONT_SMALL.render(f"Visited: {len(self.result['visit_order'])} nodes", True, BLACK)
                self.screen.blit(visited, (820, results_y))
        
        # Legend
        legend_y = 530
        legend_text = FONT_SMALL.render("Legend:", True, BLACK)
        self.screen.blit(legend_text, (820, legend_y))
        legend_y += 25
        
        pygame.draw.circle(self.screen, GREEN, (835, legend_y + 8), 8)
        legend_start = FONT_SMALL.render("Start Node", True, BLACK)
        self.screen.blit(legend_start, (855, legend_y))
        legend_y += 25
        
        pygame.draw.circle(self.screen, RED, (835, legend_y + 8), 8)
        legend_end = FONT_SMALL.render("End Node", True, BLACK)
        self.screen.blit(legend_end, (855, legend_y))
        legend_y += 25
        
        pygame.draw.circle(self.screen, BLUE, (835, legend_y + 8), 8)
        legend_path = FONT_SMALL.render("Path Node", True, BLACK)
        self.screen.blit(legend_path, (855, legend_y))
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Button events
            if self.run_button.handle_event(event):
                self.run_algorithm()
            
            if self.clear_button.handle_event(event):
                self.result = None
            
            if self.dijkstra_button.handle_event(event):
                self.algorithm = 'dijkstra'
                self.result = None
            
            if self.bellman_button.handle_event(event):
                self.algorithm = 'bellman_ford'
                self.result = None
            
            # Node selection for start/end
            if event.type == pygame.MOUSEBUTTONDOWN:
                for node_id, node in self.nodes.items():
                    if node.contains_point(event.pos[0], event.pos[1]):
                        if event.button == 1:  # Left click for start
                            self.start_node = node_id
                            self.result = None
                        elif event.button == 3:  # Right click for end
                            self.end_node = node_id
                            self.result = None
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = ShortestPathVisualizer()
    app.run()
