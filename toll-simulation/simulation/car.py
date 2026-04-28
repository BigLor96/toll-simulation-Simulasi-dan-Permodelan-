"""Car entity for toll gate simulation."""


class Car:
    """Represents a car arriving at the toll gate."""
    
    def __init__(self, car_id, arrival_time):
        """
        Initialize a car.
        
        Args:
            car_id: Unique identifier for the car
            arrival_time: Time when car arrived at the gate
        """
        self.car_id = car_id
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.departure_time = None
    
    @property
    def waiting_time(self):
        """Calculate waiting time (from arrival to service start)."""
        if self.service_start_time is None:
            return None
        return self.service_start_time - self.arrival_time
    
    @property
    def time_in_system(self):
        """Calculate total time in system (from arrival to departure)."""
        if self.departure_time is None:
            return None
        return self.departure_time - self.arrival_time
    
    def __repr__(self):
        return f"Car(id={self.car_id}, arrival={self.arrival_time:.2f})"
