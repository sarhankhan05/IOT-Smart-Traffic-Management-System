# Web Dashboard Documentation

The web dashboard provides a real-time interface for monitoring and controlling the Smart Traffic Management System.

## Overview

The dashboard is built with React.js and displays:
- Vehicle density for each lane
- Current traffic light status with countdown timers
- Manual control buttons
- System status information

## Features

### Real-time Monitoring
- Updates every 500ms to show current system status
- Visual representation of traffic light states (Red, Yellow, Green)
- Countdown timers for active lights
- Vehicle density indicators

### Manual Control
- Individual "Force Green" buttons for each lane
- Global "Resume Smart Mode" button
- Visual feedback for system state

### Responsive Design
- Adapts to different screen sizes
- Mobile-friendly layout
- Clear visual hierarchy

## Technical Details

### Framework
- Built with React.js using Create React App
- Uses Axios for API communication
- Styled with inline CSS

### File Structure
```
traffic-dashboard/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── App.js          # Main application component
│   ├── App.css         # Application styles
│   ├── index.js        # Entry point
│   └── ...
├── package.json        # Dependencies and scripts
└── README.md           # Standard CRA documentation
```

### Main Component ([App.js](traffic-dashboard/src/App.js))

#### State Management
```javascript
const [data, setData] = useState({
  densities: { lane0: 0, lane1: 0, lane2: 0, lane3: 0 },
  light: { lane0: 'Red', lane1: 'Red', lane2: 'Red', lane3: 'Red' },
  timer: { lane0: 0, lane1: 0, lane2: 0, lane3: 0 },
  timer_state: { lane0: '', lane1: '', lane2: '', lane3: '' },
  green_time: { lane0: 15, lane1: 15, lane2: 15, lane3: 15 }
});
```

#### API Integration
- Fetches data from `/api/status` endpoint every 500ms
- Sends commands to `/api/manual` endpoint for control

#### Styling
- Modern, clean design with cards for each lane
- Color-coded traffic lights (Green: #2ecc71, Yellow: #f1c40f, Red: #e74c3c)
- Responsive grid layout using CSS Grid

## API Integration

### Status Endpoint
```javascript
const res = await axios.get(`${API}/status`);
setData(res.data);
```

Response format:
```json
{
  "densities": {"lane0": 2, "lane1": 0, "lane2": 1, "lane3": 3},
  "light": {"lane0": "Green", "lane1": "Red", "lane2": "Red", "lane3": "Red"},
  "timer": {"lane0": 25.3, "lane1": 0, "lane2": 0, "lane3": 0},
  "timer_state": {"lane0": "Green", "lane1": "", "lane2": "", "lane3": ""},
  "green_time": {"lane0": 35, "lane1": 15, "lane2": 25, "lane3": 45}
}
```

### Manual Control Endpoints
```javascript
// Force green for a specific lane
axios.post(`${API}/manual`, { lane: laneIndex });

// Resume smart mode
axios.post(`${API}/manual`, { lane: null });
```

## Customization

### Changing API Endpoint
Modify the API constant in [App.js](traffic-dashboard/src/App.js):
```javascript
const API = 'http://YOUR_PI_IP_ADDRESS:5000/api';
```

### Styling Modifications
All styling is done with inline CSS in [App.js](traffic-dashboard/src/App.js). You can modify:
- Colors (colors object)
- Layout (grid properties)
- Typography (font sizes, weights)
- Spacing (padding, margins)

### Adding New Features
To extend functionality:
1. Add new state variables as needed
2. Extend the API endpoints on the Raspberry Pi
3. Update the data fetching logic
4. Add new UI components

## Building and Deployment

### Development
```bash
npm start
```
Runs the app in development mode on http://localhost:3000

### Production Build
```bash
npm run build
```
Creates an optimized production build in the `build/` folder.

The Flask server serves the built files automatically.

## Troubleshooting

### Common Issues

1. **Dashboard Not Loading**
   - Check if the Flask server is running
   - Verify the API endpoint URL in App.js
   - Ensure network connectivity between browser and Raspberry Pi

2. **Stale Data**
   - Check if the Raspberry Pi is sending data
   - Verify serial connections to Arduinos
   - Confirm API endpoint is returning current data

3. **Buttons Not Working**
   - Check browser console for JavaScript errors
   - Verify POST requests are reaching the API
   - Confirm Raspberry Pi is processing commands

4. **Layout Issues**
   - Check browser compatibility
   - Verify CSS is loading correctly
   - Test on different screen sizes

### Debugging Tips

1. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for JavaScript errors
   - Check network tab for failed API requests

2. **Verify API Response**
   - Directly access `http://PI_IP:5000/api/status` in browser
   - Check if data is being returned correctly

3. **Test Network Connectivity**
   - Ping the Raspberry Pi
   - Verify firewall settings
   - Check if port 5000 is accessible

## Future Enhancements

Possible improvements to the dashboard:
- Historical data charts
- System statistics and analytics
- User authentication for secure control
- Mobile app integration
- Alert notifications for system issues
- Multi-language support