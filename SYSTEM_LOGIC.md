# System Logic and Algorithm Documentation

This document explains the core algorithms and logic behind the Smart Traffic Management System.

## Traffic Management Algorithm

The system uses a dynamic timing algorithm that adjusts green light duration based on real-time vehicle density.

### Dynamic Timing Formula

```
Green Time = MAX(5, 15 + (Density × 10))
```

Where:
- Minimum green time: 5 seconds
- Base green time: 15 seconds
- Additional time per vehicle: 10 seconds
- Density: Number of vehicles detected in a lane (0-3)

### Example Calculations

| Density | Green Time |
|---------|------------|
| 0       | 15 seconds |
| 1       | 25 seconds |
| 2       | 35 seconds |
| 3       | 45 seconds |

## State Machine

The system operates using a state machine with the following states:

### 1. ALL_RED State
- All traffic lights show red
- System determines which lane to activate next
- Calculates green time for the selected lane

### 2. GREEN State
- Selected lane shows green
- Other lanes show red
- Counts down the allocated green time

### 3. YELLOW State
- Selected lane shows yellow (caution)
- Other lanes remain red
- Fixed 5-second duration

### State Transitions

```
ALL_RED → GREEN → YELLOW → ALL_RED → ...
```

## Traffic Light Control Logic

### Normal Cycle
1. System starts in ALL_RED state
2. Determines lane with highest density
3. Sets that lane to GREEN for calculated duration
4. When green time expires, switches to YELLOW for 5 seconds
5. Returns to ALL_RED and repeats

### Manual Override
1. User presses "Force Green" for a specific lane
2. System interrupts normal cycle
3. Clears active lane with yellow transition (if applicable)
4. Sets requested lane to GREEN for 30 seconds
5. Transitions to YELLOW for 5 seconds
6. Returns to ALL_RED and resumes smart mode

## Data Flow and Processing

### Sensor Data Processing
1. Sensor Arduino reads IR sensors every 200ms
2. Calculates density for each lane (0-3 vehicles)
3. Sends data to Raspberry Pi via serial:
   ```
   LANE0:2;LANE1:0;LANE2:1;LANE3:3;
   ```
4. Raspberry Pi parses and stores density data

### Decision Making
1. Every cycle iteration checks for:
   - Manual mode activation
   - Timer expiration
   - State transitions
2. Updates traffic light states accordingly
3. Sends commands to LED Arduino:
   ```
   LANE0:G  (Lane 0 Green)
   LANE1:Y  (Lane 1 Yellow)
   ALL:R    (All Red)
   ```

### Timing Precision
- Uses delta-time calculation for accurate timing
- Updates timers every 50ms
- Maintains synchronization despite processing delays

## Safety Mechanisms

### All-Red Transitions
- Between any green/yellow to another green/yellow
- Ensures intersection clearing
- Prevents cross-traffic collisions

### Manual Override Safety
- Interrupts automatic cycle cleanly
- Clears active lanes before forcing new green
- Automatically returns to smart mode

### Error Handling
- Serial reconnection for disconnected Arduinos
- Graceful degradation if components fail
- Non-blocking Firebase data logging

## Performance Optimization

### Threading Model
- Main thread: Flask web server
- Background thread: Sensor processing and traffic logic
- Separate threads: Firebase data pushing
- Manual control: Dedicated sequence threads

### Resource Management
- Efficient serial communication
- Minimal memory footprint
- Non-blocking operations

### Timing Accuracy
- Delta-time based calculations
- Fast 50ms update loop
- Precise timer management

## Extensibility Points

### Algorithm Modification
Easy to adjust:
- Green time formula
- Minimum/maximum times
- Weight factors for density

### State Machine Expansion
Can add states like:
- Flashing caution
- Pedestrian crossing
- Emergency vehicle priority

### Data Integration
Supports:
- Historical analysis
- Predictive modeling
- Remote configuration

## Edge Cases Handled

### Tie Scenarios
When multiple lanes have equal density:
- Priority given to next sequential lane
- Prevents starvation of any lane

### Zero Density
When no vehicles detected:
- Maintains minimum green time (15 seconds)
- Ensures fair rotation

### High Density
When all lanes have maximum density:
- Provides maximum green time (45 seconds)
- Rotates fairly between lanes

### System Startup
- Waits for first sensor data before starting cycle
- Initializes all lights to red
- Establishes serial connections

## Future Enhancements

### Predictive Analytics
- Learning from historical patterns
- Anticipating traffic flow
- Proactive light adjustment

### Multi-intersection Coordination
- City-wide traffic optimization
- Wave progression for arterial roads
- Centralized control system

### Advanced Sensing
- Camera-based vehicle detection
- Vehicle classification
- Pedestrian and cyclist detection

### Communication Protocols
- MQTT for distributed systems
- REST API for remote management
- WebSocket for real-time updates