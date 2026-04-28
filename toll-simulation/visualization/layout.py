"""Simple 2D layout visualization of toll gate."""

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_toll_gate_layout(num_booths=3, queue_length=5):
    """
    Draw a simple 2D layout of the toll gate system.
    
    Args:
        num_booths: Number of toll booths
        queue_length: Current queue length (for visualization)
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Road (angled lines)
    road_width = 2
    booth_spacing = 3
    
    # Draw incoming road
    road_y_top = 8
    road_y_bottom = 2
    road_x_left = 1
    road_x_right = 4
    
    # Road as trapezoid (perspective)
    road = patches.Polygon([
        [road_x_left, road_y_top],
        [road_x_right, road_y_top],
        [road_x_right + road_width, road_y_bottom],
        [road_x_left + road_width, road_y_bottom]
    ], closed=True, fill=True, facecolor='lightgray', edgecolor='black', linewidth=2)
    ax.add_patch(road)
    
    # Draw booths
    booth_height = 0.8
    booth_width = 1.5
    booth_start_x = 6
    booth_start_y = 2.5
    
    for i in range(num_booths):
        booth_x = booth_start_x + i * (booth_width + 0.5)
        booth = patches.Rectangle(
            (booth_x, booth_start_y), booth_width, booth_height,
            fill=True, facecolor='#FF6B6B', edgecolor='darkred', linewidth=2
        )
        ax.add_patch(booth)
        
        # Booth label
        ax.text(booth_x + booth_width/2, booth_start_y + booth_height/2, 
                f'Booth {i+1}', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Draw queue (cars waiting)
    car_size = 0.4
    queue_x = 2.5
    queue_y_start = 5
    
    for i in range(min(queue_length, 8)):  # Max 8 cars shown in queue
        car_y = queue_y_start - i * (car_size + 0.1)
        car = patches.Rectangle(
            (queue_x, car_y), car_size, car_size,
            fill=True, facecolor='#4ECDC4', edgecolor='darkblue', linewidth=1.5
        )
        ax.add_patch(car)
    
    # Draw exit road
    exit_x_start = booth_start_x + num_booths * booth_width
    exit_y_top = booth_start_y + booth_height/2
    
    exit_road = patches.Polygon([
        [exit_x_start, exit_y_top - 0.4],
        [exit_x_start + 1.5, exit_y_top - 0.4],
        [exit_x_start + 3, exit_y_top - 1],
        [exit_x_start + 1.5, exit_y_top]
    ], closed=True, fill=True, facecolor='lightgray', edgecolor='black', linewidth=2)
    ax.add_patch(exit_road)
    
    # Labels
    ax.text(2.5, 9.5, 'INCOMING TRAFFIC', fontsize=12, fontweight='bold', ha='center')
    ax.text(booth_start_x + num_booths * (booth_width + 0.5) / 2, 1.2, 
            'TOLL BOOTHS', fontsize=12, fontweight='bold', ha='center')
    ax.text(exit_x_start + 2, 0.2, 'EXIT', fontsize=12, fontweight='bold', ha='center')
    
    # Queue info
    ax.text(1, 3.5, f'Queue: {queue_length}', fontsize=11, 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Set axis properties
    ax.set_xlim(-0.5, exit_x_start + 4)
    ax.set_ylim(-0.5, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Toll Gate Layout', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    fig = draw_toll_gate_layout(num_booths=3, queue_length=5)
    plt.savefig('toll_gate_layout.png', dpi=150, bbox_inches='tight')
    plt.show()
