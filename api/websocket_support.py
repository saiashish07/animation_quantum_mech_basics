"""
WebSocket Support for Real-time Updates
Enables live data streaming for tunneling animations
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import numpy as np
import threading
from quantum_playground.solvers import TimeDependentSolver, GaussianWavePacket
from quantum_playground.potentials import RectangularBarrier

socketio = SocketIO(cors_allowed_origins="*")

class TunnelingStreamManager:
    """Manages real-time tunneling simulation streaming"""
    
    def __init__(self):
        self.simulations = {}
        self.threads = {}
    
    def start_streaming(self, client_id, params):
        """Start streaming tunneling simulation"""
        if client_id in self.simulations:
            return {'error': 'Simulation already running'}
        
        # Extract parameters
        barrier_height = params.get('barrier_height', 30.0)
        barrier_width = params.get('barrier_width', 2.0)
        particle_energy = params.get('particle_energy', 20.0)
        packet_sigma = params.get('packet_sigma', 0.5)
        
        # Create simulation context
        sim_context = {
            'barrier_height': barrier_height,
            'barrier_width': barrier_width,
            'particle_energy': particle_energy,
            'packet_sigma': packet_sigma,
            'running': True,
            'frame': 0
        }
        
        self.simulations[client_id] = sim_context
        
        # Start streaming thread
        thread = threading.Thread(
            target=self._stream_simulation,
            args=(client_id,),
            daemon=True
        )
        thread.start()
        self.threads[client_id] = thread
        
        return {'status': 'started', 'client_id': client_id}
    
    def stop_streaming(self, client_id):
        """Stop streaming simulation"""
        if client_id in self.simulations:
            self.simulations[client_id]['running'] = False
            del self.simulations[client_id]
        return {'status': 'stopped'}
    
    def _stream_simulation(self, client_id):
        """Run simulation and emit frames"""
        context = self.simulations[client_id]
        
        # Setup simulation (simplified)
        from api.quantum_api import GRID_POINTS, X_MIN, X_MAX
        from quantum_playground.solvers import QuantumGrid, StationarySolver
        
        grid = QuantumGrid(X_MIN, X_MAX, GRID_POINTS)
        potential = RectangularBarrier(
            context['barrier_height'],
            context['barrier_width'],
            center=0.0
        )
        V = potential(grid.x)
        
        # Initial wavepacket
        psi0 = GaussianWavePacket.create(
            grid.x,
            x0=-5.0,
            sigma=context['packet_sigma'],
            k0=np.sqrt(2.0 * context['particle_energy']),
            amplitude=1.0
        )
        psi0 = GaussianWavePacket.normalize(psi0, grid.dx)
        
        # Time evolution
        solver = TimeDependentSolver(grid, V, mass=1.0, dt=0.01)
        
        frame_count = 0
        while context['running']:
            try:
                # Step simulation
                psi0 = solver.step(psi0)
                
                # Emit frame
                frame_data = {
                    'frame': frame_count,
                    'wavefunction': np.abs(psi0).tolist(),
                    'probability': (np.abs(psi0)**2).tolist()
                }
                
                socketio.emit('tunneling_frame', frame_data, room=client_id)
                
                frame_count += 1
                
                # Emit every ~50ms
                threading.Event().wait(0.05)
                
            except Exception as e:
                print(f"Error in simulation: {e}")
                break

# Global manager
tunnel_manager = TunnelingStreamManager()


def init_websocket(app):
    """Initialize WebSocket support"""
    socketio.init_app(app)
    
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected: {flask.request.sid}')
        emit('response', {'data': 'Connected'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        client_id = flask.request.sid
        tunnel_manager.stop_streaming(client_id)
        print(f'Client disconnected: {client_id}')
    
    @socketio.on('start_tunneling')
    def handle_start_tunneling(data):
        client_id = flask.request.sid
        result = tunnel_manager.start_streaming(client_id, data)
        emit('simulation_status', result)
    
    @socketio.on('stop_tunneling')
    def handle_stop_tunneling():
        client_id = flask.request.sid
        result = tunnel_manager.stop_streaming(client_id)
        emit('simulation_status', result)
    
    return socketio
