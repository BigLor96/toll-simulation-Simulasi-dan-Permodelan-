"""Animated visualization of toll gate simulation using pygame."""

import pygame
import math
from typing import List, Dict


class Car2D:
    """Representation of a car for 2D animation."""

    def __init__(self, car_id, x, y):
        self.car_id = car_id
        self.x = x
        self.y = y
        self.width = 26
        self.height = 14
        self.state = 'arriving'  # arriving, queuing, serving, exiting, done
        self.target_x = x
        self.target_y = y
        self.speed = 180  # pixels per second (in simulation-time)
        self.booth_id = None
        self.queue_pos = 0  # index in the booth queue (0 = head)

    def update(self, dt):
        """Move car toward its target. dt is in (scaled) seconds."""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.hypot(dx, dy)
        if distance < 0.5:
            self.x = self.target_x
            self.y = self.target_y
            return

        move_dist = self.speed * dt
        if move_dist >= distance:
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += (dx / distance) * move_dist
            self.y += (dy / distance) * move_dist

    def draw(self, surface, color):
        rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2,
                           self.width, self.height)
        pygame.draw.rect(surface, color, rect, border_radius=3)
        pygame.draw.rect(surface, (40, 40, 40), rect, 1, border_radius=3)
        # Wheels
        wheel_color = (30, 30, 30)
        pygame.draw.circle(surface, wheel_color,
                           (int(self.x - self.width / 3), int(self.y + self.height / 2)), 2)
        pygame.draw.circle(surface, wheel_color,
                           (int(self.x + self.width / 3), int(self.y + self.height / 2)), 2)


class TollGateAnimation:
    """Animated visualization of toll gate with horizontal flow layout."""

    def __init__(self, num_booths=2, simulation_duration=60):
        self.num_booths = num_booths
        self.simulation_duration = simulation_duration

        # Window setup
        self.width = 1100
        self.height = 700
        self.screen = None
        self.clock = None

        # Horizontal flow layout (left -> right)
        self.arrive_x = 40           # cars spawn here
        self.split_x = 320           # incoming lane splits to per-booth lanes
        self.queue_tail_x = 360      # last spot in queue (farthest from booth)
        self.queue_head_x = 540      # closest to booth (where serving begins)
        self.booth_x = 620           # booth structure x
        self.merge_x = 760           # exit lanes merge back
        self.exit_x = 1080           # cars leave screen here

        self.queue_slot_spacing = 32  # px between queued cars
        self.max_visible_queue = 8

        # Centerline + per-booth lanes
        self.center_y = self.height // 2 + 20
        self.booth_spacing = 90 if num_booths > 1 else 0
        self.booths = self._create_booth_positions()

        # Per-booth queues: list of car_ids waiting (head = index 0 = being served)
        self.booth_queues: Dict[int, List[int]] = {i: [] for i in range(num_booths)}
        self.booth_occupied: Dict[int, bool] = {i: False for i in range(num_booths)}

        # Cars on screen
        self.active_cars: Dict[int, Car2D] = {}

        # Timeline
        self.timeline: List[Dict] = []
        self.current_event_idx = 0
        self.elapsed_time = 0.0  # in simulation minutes
        self.playback_speed = 1.0  # 1.0 = 1 sim-minute per real-second

    def _create_booth_positions(self):
        booths = []
        n = self.num_booths
        start_y = self.center_y - (n - 1) * self.booth_spacing / 2
        for i in range(n):
            booths.append({
                'id': i,
                'x': self.booth_x,
                'y': start_y + i * self.booth_spacing,
                'width': 70,
                'height': 56,
            })
        return booths

    def _booth_y(self, booth_id):
        return self.booths[booth_id]['y']

    def load_timeline(self, timeline_events):
        self.timeline = sorted(timeline_events, key=lambda e: e['time'])
        self.current_event_idx = 0
        self.elapsed_time = 0.0

    # ------------------------------------------------------------------ events

    def _pick_booth_for_arrival(self):
        """Send car to the booth with the shortest queue (round-robin tiebreak)."""
        return min(range(self.num_booths),
                   key=lambda b: (len(self.booth_queues[b]), b))

    def _queue_position_xy(self, booth_id, slot):
        """XY coordinates for a queue slot in front of a booth.
        slot 0 = at the booth (being served).
        """
        slot = min(slot, self.max_visible_queue)
        x = self.queue_head_x - slot * self.queue_slot_spacing
        y = self._booth_y(booth_id)
        return x, y

    def _refresh_queue_targets(self, booth_id):
        """Re-target every car in this booth's queue to its current slot."""
        for slot, cid in enumerate(self.booth_queues[booth_id]):
            if cid not in self.active_cars:
                continue
            car = self.active_cars[cid]
            tx, ty = self._queue_position_xy(booth_id, slot)
            car.target_x = tx
            car.target_y = ty
            car.queue_pos = slot
            if slot == 0 and self.booth_occupied[booth_id]:
                car.state = 'serving'
            elif slot == 0:
                car.state = 'queuing'
            else:
                car.state = 'queuing'

    def _handle_event(self, event):
        event_type = event['type']
        car_id = event['car_id']

        if event_type == 'arrive':
            booth_id = self._pick_booth_for_arrival()
            car = Car2D(car_id, self.arrive_x, self.center_y)
            car.booth_id = booth_id
            car.state = 'arriving'
            self.active_cars[car_id] = car
            self.booth_queues[booth_id].append(car_id)
            self._refresh_queue_targets(booth_id)

        elif event_type == 'start_service':
            if car_id not in self.active_cars:
                return
            car = self.active_cars[car_id]
            booth_id = car.booth_id
            if booth_id is None:
                return
            self.booth_occupied[booth_id] = True
            car.state = 'serving'
            tx, ty = self._queue_position_xy(booth_id, 0)
            car.target_x = tx
            car.target_y = ty

        elif event_type == 'depart':
            if car_id not in self.active_cars:
                return
            car = self.active_cars[car_id]
            booth_id = car.booth_id
            car.state = 'exiting'
            if booth_id is not None:
                self.booth_occupied[booth_id] = False
                if self.booth_queues[booth_id] and self.booth_queues[booth_id][0] == car_id:
                    self.booth_queues[booth_id].pop(0)
                else:
                    # Defensive: remove if present anywhere
                    if car_id in self.booth_queues[booth_id]:
                        self.booth_queues[booth_id].remove(car_id)
                self._refresh_queue_targets(booth_id)
            # Route through the merge point, then off-screen right
            car.target_x = self.merge_x
            car.target_y = self.center_y

    def _process_events(self):
        while (self.current_event_idx < len(self.timeline) and
               self.timeline[self.current_event_idx]['time'] <= self.elapsed_time):
            self._handle_event(self.timeline[self.current_event_idx])
            self.current_event_idx += 1

    # ------------------------------------------------------------------ update

    def update(self, dt_real):
        """dt_real is wall-clock seconds since last frame."""
        # Advance simulation time
        dt_sim = dt_real * self.playback_speed
        self.elapsed_time += dt_sim
        self._process_events()

        # Cars move in scaled time so they keep up with playback speed.
        # Cap the per-frame motion to avoid huge jumps when speed is very high.
        motion_dt = min(dt_sim, 0.1) * 6.0  # tuning factor

        cars_to_remove = []
        for car_id, car in self.active_cars.items():
            # Two-stage exit: first reach merge_x, then go to exit_x
            if car.state == 'exiting' and abs(car.x - self.merge_x) < 2 and abs(car.y - self.center_y) < 2:
                car.target_x = self.exit_x + 40
                car.target_y = self.center_y

            car.update(motion_dt)

            if car.state == 'exiting' and car.x >= self.exit_x:
                cars_to_remove.append(car_id)

        for cid in cars_to_remove:
            del self.active_cars[cid]

    # ------------------------------------------------------------------ draw

    def draw(self, surface):
        surface.fill((235, 240, 235))
        self._draw_road(surface)
        self._draw_booths(surface)

        # Draw cars (sorted by y so closer ones render last)
        for car in sorted(self.active_cars.values(), key=lambda c: c.y):
            if car.state == 'serving':
                color = (220, 60, 60)
            elif car.state == 'queuing':
                color = (90, 110, 200)
            elif car.state == 'exiting':
                color = (70, 170, 80)
            else:  # arriving
                color = (240, 180, 60)
            car.draw(surface, color)

        self._draw_hud(surface)

    def _draw_road(self, surface):
        road_color = (90, 90, 95)
        edge_color = (50, 50, 55)
        line_color = (240, 220, 80)

        # Incoming trunk: arrive_x -> split_x at center_y
        trunk_h = max(60, self.num_booths * 28)
        pygame.draw.rect(surface, road_color,
                         (self.arrive_x - 20, self.center_y - trunk_h / 2,
                          self.split_x - self.arrive_x + 20, trunk_h))
        pygame.draw.rect(surface, edge_color,
                         (self.arrive_x - 20, self.center_y - trunk_h / 2,
                          self.split_x - self.arrive_x + 20, trunk_h), 2)

        # Per-booth lanes from split_x through merge_x
        lane_h = 40
        for booth in self.booths:
            by = booth['y']
            # Lane segment under the queue/booth
            pygame.draw.rect(surface, road_color,
                             (self.split_x, by - lane_h / 2,
                              self.merge_x - self.split_x, lane_h))
            pygame.draw.rect(surface, edge_color,
                             (self.split_x, by - lane_h / 2,
                              self.merge_x - self.split_x, lane_h), 2)

            # Connector polygon from trunk to this lane
            connector = [
                (self.split_x, self.center_y - trunk_h / 2),
                (self.split_x, self.center_y + trunk_h / 2),
                (self.split_x + 30, by + lane_h / 2),
                (self.split_x + 30, by - lane_h / 2),
            ]
            # Only draw connector once (covers all)
        # Single trapezoid from trunk to spread of lanes
        if self.num_booths > 1:
            top_y = self.booths[0]['y'] - lane_h / 2
            bot_y = self.booths[-1]['y'] + lane_h / 2
            spread = [
                (self.split_x, self.center_y - trunk_h / 2),
                (self.split_x + 40, top_y),
                (self.split_x + 40, bot_y),
                (self.split_x, self.center_y + trunk_h / 2),
            ]
            pygame.draw.polygon(surface, road_color, spread)
            pygame.draw.polygon(surface, edge_color, spread, 2)

        # Exit trunk
        pygame.draw.rect(surface, road_color,
                         (self.merge_x, self.center_y - trunk_h / 2,
                          self.exit_x - self.merge_x, trunk_h))
        pygame.draw.rect(surface, edge_color,
                         (self.merge_x, self.center_y - trunk_h / 2,
                          self.exit_x - self.merge_x, trunk_h), 2)

        # Merge trapezoid
        if self.num_booths > 1:
            top_y = self.booths[0]['y'] - lane_h / 2
            bot_y = self.booths[-1]['y'] + lane_h / 2
            merge = [
                (self.merge_x, self.center_y - trunk_h / 2),
                (self.merge_x - 40, top_y),
                (self.merge_x - 40, bot_y),
                (self.merge_x, self.center_y + trunk_h / 2),
            ]
            pygame.draw.polygon(surface, road_color, merge)
            pygame.draw.polygon(surface, edge_color, merge, 2)

        # Center dashed line on incoming trunk
        for x in range(self.arrive_x, self.split_x, 24):
            pygame.draw.line(surface, line_color,
                             (x, self.center_y), (x + 12, self.center_y), 2)
        # Center dashed line on exit trunk
        for x in range(self.merge_x + 10, self.exit_x, 24):
            pygame.draw.line(surface, line_color,
                             (x, self.center_y), (x + 12, self.center_y), 2)

        # Stop line for each booth (just before booth)
        for booth in self.booths:
            by = booth['y']
            sx = self.queue_head_x + 18
            pygame.draw.line(surface, (255, 255, 255),
                             (sx, by - lane_h / 2 + 2),
                             (sx, by + lane_h / 2 - 2), 2)

    def _draw_booths(self, surface):
        font = pygame.font.SysFont(None, 20, bold=True)
        for booth in self.booths:
            x, y = booth['x'], booth['y']
            w, h = booth['width'], booth['height']

            # Roof / canopy
            roof = [
                (x - w / 2 - 8, y - h / 2),
                (x + w / 2 + 8, y - h / 2),
                (x + w / 2, y - h / 2 - 14),
                (x - w / 2, y - h / 2 - 14),
            ]
            pygame.draw.polygon(surface, (180, 60, 40), roof)
            pygame.draw.polygon(surface, (90, 30, 20), roof, 2)

            # Booth body (offset to side of lane so car visibly passes through)
            body_rect = pygame.Rect(x + w / 2 - 14, y - h / 2, 28, h)
            pygame.draw.rect(surface, (220, 200, 160), body_rect)
            pygame.draw.rect(surface, (90, 70, 40), body_rect, 2)
            # Window
            pygame.draw.rect(surface, (140, 200, 230),
                             (body_rect.x + 4, body_rect.y + 8, 20, 18))

            # Barrier gate (above lane), color by occupancy
            gate_y = y - 22
            gate_color = (220, 40, 40) if self.booth_occupied[booth['id']] else (40, 180, 60)
            pygame.draw.rect(surface, gate_color,
                             (x - w / 2 - 10, gate_y, w + 20, 5))
            pygame.draw.line(surface, (30, 30, 30),
                             (x - w / 2 - 10, gate_y - 4),
                             (x - w / 2 - 10, gate_y + 9), 3)

            # Booth label
            label = font.render(f"Booth {booth['id'] + 1}", True, (20, 20, 20))
            surface.blit(label, (x - label.get_width() / 2,
                                 y - h / 2 - 32))

            # Queue length indicator
            qlen = len(self.booth_queues[booth['id']])
            qlabel = font.render(f"Q={qlen}", True, (40, 40, 80))
            surface.blit(qlabel, (self.split_x + 8, y - 8))

    def _draw_hud(self, surface):
        font_small = pygame.font.SysFont(None, 20)
        font_large = pygame.font.SysFont(None, 28, bold=True)

        # Time display: simulation minutes:seconds
        total_seconds = self.elapsed_time * 60.0
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        time_text = font_large.render(
            f"Sim time: {minutes:02d}:{seconds:02d}  /  {self.simulation_duration:.0f}m",
            True, (20, 20, 20))
        surface.blit(time_text, (12, 10))

        active_text = font_small.render(
            f"Cars on screen: {len(self.active_cars)}", True, (20, 20, 20))
        surface.blit(active_text, (12, 42))

        progress = (self.current_event_idx / len(self.timeline)) if self.timeline else 0
        prog_text = font_small.render(
            f"Events: {self.current_event_idx}/{len(self.timeline)} ({progress*100:.0f}%)",
            True, (20, 20, 20))
        surface.blit(prog_text, (12, 62))

        speed_text = font_small.render(
            f"Speed: {self.playback_speed:.1f}x", True, (20, 20, 20))
        surface.blit(speed_text, (12, 82))

        # Legend
        legend = [
            ((240, 180, 60), "arriving"),
            ((90, 110, 200), "queuing"),
            ((220, 60, 60), "serving"),
            ((70, 170, 80), "exiting"),
        ]
        lx = self.width - 160
        ly = 10
        for color, label in legend:
            pygame.draw.rect(surface, color, (lx, ly + 3, 14, 10))
            t = font_small.render(label, True, (20, 20, 20))
            surface.blit(t, (lx + 22, ly))
            ly += 18

        # Instructions
        inst_font = pygame.font.SysFont(None, 18)
        instructions = [
            "Space: Play/Pause   |   Left/Right: -/+ 0.5x   |   Up/Down: -/+ 0.1x",
            "R: Reset   |   Q / Esc: Quit",
        ]
        for i, inst in enumerate(instructions):
            text = inst_font.render(inst, True, (80, 80, 80))
            surface.blit(text, (12, self.height - 44 + i * 18))

    # ------------------------------------------------------------------ run

    def _reset(self):
        self.elapsed_time = 0.0
        self.current_event_idx = 0
        self.active_cars.clear()
        self.booth_queues = {i: [] for i in range(self.num_booths)}
        self.booth_occupied = {i: False for i in range(self.num_booths)}

    def run(self, timeline_events):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Toll Gate Animation")
        self.clock = pygame.time.Clock()

        self.load_timeline(timeline_events)

        running = True
        paused = False
        target_fps = 60

        while running:
            dt = self.clock.tick(target_fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.playback_speed = max(0.1, self.playback_speed - 0.5)
                    elif event.key == pygame.K_RIGHT:
                        self.playback_speed = min(20.0, self.playback_speed + 0.5)
                    elif event.key == pygame.K_UP:
                        self.playback_speed = min(20.0, self.playback_speed + 0.1)
                    elif event.key == pygame.K_DOWN:
                        self.playback_speed = max(0.1, self.playback_speed - 0.1)
                    elif event.key == pygame.K_r:
                        self._reset()

            if not paused:
                self.update(dt)

            self.draw(self.screen)
            pygame.display.flip()

            # Exit only when timeline is exhausted AND all cars have left
            if (self.current_event_idx >= len(self.timeline)
                    and not self.active_cars):
                # keep window open briefly so user sees final state
                pygame.time.wait(800)
                running = False

        pygame.quit()


def animate_scenario(sim_env, num_booths, simulation_duration=60):
    """Create and run animation for a simulation scenario."""
    animation = TollGateAnimation(num_booths=num_booths,
                                  simulation_duration=simulation_duration)
    animation.run(sim_env.timeline)
