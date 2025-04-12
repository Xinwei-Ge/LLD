from datetime import datetime


SPOT_COMPATIBILITY = {
    "bike": ["bike", "car", "truck"],
    "car": ["car", "truck"],
    "truck": ["truck"]
}

VEHICLE_PRICING = {
    "bike": 1,
    "car": 2,
    "truck": 3
}


class ParkingLot:
    def __init__(self, id):
        self.id = id
        self.floors = []
        self.vehicle_spot_map = {}

    def get_floors(self):
        return self.floors

    def add_floor(self, floor):
        self.floors.append(floor)
    def park_vehicle(self, vehicle):
        for floor in self.floors:
            spot = floor.find_available_spot(vehicle.vehicle_type)
            if spot:
                spot.add_vehicle(vehicle)
                vehicle.entry_time = datetime.now()
                self.vehicle_spot_map[vehicle.license_plate] = (floor, spot)
                print(f"Vehicle parked at spot {spot.spot_id} on floor {floor.floor_number}")
                return True
        print("No available spot for this vehicle type.")
        return False
    
    def exit_vehicle(self, vehicle):
        if vehicle.license_plate not in self.vehicle_spot_map:
            print("Vehicle not found.")
            return None
        floor, spot = self.vehicle_spot_map[vehicle.license_plate]
        duration = datetime.now() - vehicle.entry_time
        hours = int(duration.total_seconds() // 3600) + 1
        rate = vehicle.get_hourly_rate()
        charge = hours * rate

        spot.remove_vehicle()
        del self.vehicle_spot_map[vehicle.license_plate]

        print(f"Vehicle exited. Total charge: ${charge}")
        return charge

class Floor:
    def __init__(self, floor_number, rows, cols):
        self.floor_number = floor_number
        self.rows = rows
        self.cols = cols
        self.spots = [[None for _ in range(cols)] for _ in range(rows)]
    
    def add_spot(self, spot, row, col):
        self.spots[row][col] = spot
    
    def find_available_spot(self, vehicle_type):
        for row in range(self.rows):
            for col in range(self.cols):
                spot = self.spots[row][col]
                if spot and not spot.is_occupied and spot.spot_type.lower() in SPOT_COMPATIBILITY[vehicle_type.lower()]:
                    return spot
            
        return None
        
class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.is_occupied = False
        self.vehicle = None
    
    def add_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.is_occupied = True
    
    def remove_vehicle(self):
        self.is_occupied = False
        self.vehicle = None

class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type
        self.entry_time = None

    def get_hourly_rate(self):
        return VEHICLE_PRICING.get(self.vehicle_type, 0)
                


        

if __name__ == "__main__":
    lot = ParkingLot("LotA")

    floor1 = Floor(1, 2, 3)
    floor1.add_spot(ParkingSpot("1A", "bike"), 0,0)
    floor1.add_spot(ParkingSpot("1B", "CAR"),0,1)
    floor1.add_spot(ParkingSpot("1C", "truck"),0,2)
    lot.add_floor(floor1)

    bike = Vehicle("BIKE123", "bike")
    car = Vehicle("CAR123", "car")
    truck = Vehicle("TRUCK123", "truck")
    lot.park_vehicle(bike)


    import time
    time.sleep(2)

    lot.exit_vehicle(bike)