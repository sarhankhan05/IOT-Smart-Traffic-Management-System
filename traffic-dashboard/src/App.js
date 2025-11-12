import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://10.32.14.84:5000/api';

function App() {
  const [data, setData] = useState({
    densities: { lane0: 0, lane1: 0, lane2: 0, lane3: 0 },
    light: { lane0: 'Red', lane1: 'Red', lane2: 'Red', lane3: 'Red' },
    timer: { lane0: 0, lane1: 0, lane2: 0, lane3: 0 },
    timer_state: { lane0: '', lane1: '', lane2: '', lane3: '' },
    green_time: { lane0: 15, lane1: 15, lane2: 15, lane3: 15 }
  });

  const lanes = ['North', 'East', 'South', 'West'];
  const colors = { Green: '#2ecc71', Yellow: '#f1c40f', Red: '#e74c3c' };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`${API}/status`);
        setData(res.data);
      } catch (err) {
        console.error("API Error:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 500); 
    return () => clearInterval(interval);
  }, []);

  const forceGreen = (lane) => {
    axios.post(`${API}/manual`, { lane });
  };

  const resumeSmart = () => {
    axios.post(`${API}/manual`, { lane: null });
  };

  return (
    <div style={{
      fontFamily: 'Arial, sans-serif',
      background: '#f0f2f5',
      minHeight: '100vh',
      padding: '20px'
    }}>
      <h1 style={{
        textAlign: 'center',
        color: '#2c3e50',
        marginBottom: '30px',
        fontSize: '2.5rem'
      }}>
        Smart Traffic Dashboard
      </h1>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '25px',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {lanes.map((name, i) => {
          const laneKey = `lane${i}`;
          const light = data.light[laneKey] || 'Red';
          const timer = data.timer[laneKey] || 0;
          const state = data.timer_state[laneKey] || '';
          const greenTime = data.green_time[laneKey] || 15;
          const vehicles = data.densities[laneKey] || 0;

          return (
            <div key={i} style={{
              background: 'white',
              borderRadius: '16px',
              padding: '20px',
              boxShadow: '0 8px 20px rgba(0,0,0,0.1)',
              textAlign: 'center',
              border: '3px solid #34495e'
            }}>
              <h2 style={{ margin: '0 0 15px', color: '#2c3e50', fontSize: '1.6rem' }}>
                {name} Lane
              </h2>

              <div style={{ marginBottom: '15px' }}>
                <p style={{ margin: '8px 0', fontSize: '1.1rem' }}>
                  Vehicles: <strong style={{ color: '#e74c3c', fontSize: '1.4rem' }}>{vehicles}</strong>
                </p>
                <p style={{ margin: '8px 0', fontSize: '1rem', color: '#7f8c8d' }}>
                  Green Time: <strong>{greenTime}s</strong>
                </p>
              </div>

              {/* TRAFFIC LIGHT WITH TIMER */}
              <div style={{
                width: 100,
                height: 100,
                margin: '20px auto',
                background: colors[light],
                borderRadius: '50%',
                border: '6px solid #2c3e50',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '2rem',
                fontWeight: 'bold',
                color: 'white',
                textShadow: '2px 2px 4px rgba(0,0,0,0.5)',
                boxShadow: '0 0 20px rgba(0,0,0,0.3)'
              }}>
                {state ? Math.ceil(timer) : ''}
              </div>

              <p style={{
                fontSize: '0.9rem',
                color: '#7f8c8d',
                margin: '10px 0'
              }}>
                {state === 'Green' ? 'Green Active' : state === 'Yellow' ? 'Caution' : 'Waiting'}
              </p>

              <button
                onClick={() => forceGreen(i)}
                style={{
                  padding: '12px 24px',
                  fontSize: '1rem',
                  background: '#3498db',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  marginTop: '10px',
                  boxShadow: '0 4px 10px rgba(52,152,219,0.3)'
                }}
              >
                Force Green
              </button>
            </div>
          );
        })}
      </div>

      {/* RESUME BUTTON */}
      <div style={{ textAlign: 'center', marginTop: '40px' }}>
        <button
          onClick={resumeSmart}
          style={{
            padding: '16px 40px',
            fontSize: '1.3rem',
            background: '#27ae60',
            color: 'white',
            border: 'none',
            borderRadius: '12px',
            cursor: 'pointer',
            boxShadow: '0 6px 15px rgba(39,174,96,0.4)',
            fontWeight: 'bold'
          }}
        >
          Resume Smart Mode
        </button>
      </div>

      <footer style={{
        textAlign: 'center',
        marginTop: '50px',
        color: '#95a5a6',
        fontSize: '0.9rem'
      }}>
        Real-time Smart Traffic System • Powered by Raspberry Pi + Arduino
      </footer>
    </div>
  );
}

export default App;