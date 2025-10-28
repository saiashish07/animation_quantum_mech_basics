"""
WebSocket service for real-time quantum simulation streaming
Handles client connections, subscriptions, and live parameter updates
"""

from flask_socketio import emit, join_room, leave_room
import numpy as np
from datetime import datetime
from threading import Thread
import time


class WebSocketService:
    """Manages WebSocket connections and real-time data streaming"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_rooms = {}
        self.simulation_streams = {}
    
    def register_handlers(self):
        """Register all WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            client_id = self.socketio.request.sid
            emit('connection_established', {
                'client_id': client_id,
                'timestamp': datetime.now().isoformat()
            })
            print(f"[WebSocket] Client {client_id} connected")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            client_id = self.socketio.request.sid
            self.cleanup_client(client_id)
            print(f"[WebSocket] Client {client_id} disconnected")
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            room = data.get('room', 'default')
            client_id = self.socketio.request.sid
            join_room(room)
            
            if room not in self.active_rooms:
                self.active_rooms[room] = []
            self.active_rooms[room].append(client_id)
            
            emit('subscribed', {
                'room': room,
                'active_subscribers': len(self.active_rooms.get(room, []))
            })
            print(f"[WebSocket] Client {client_id} subscribed to {room}")
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            room = data.get('room', 'default')
            client_id = self.socketio.request.sid
            leave_room(room)
            
            if room in self.active_rooms and client_id in self.active_rooms[room]:
                self.active_rooms[room].remove(client_id)
            
            emit('unsubscribed', {'room': room})
            print(f"[WebSocket] Client {client_id} unsubscribed from {room}")
        
        @self.socketio.on('request_live_update')
        def handle_live_update(data):
            """Request real-time updates as parameters change"""
            simulation_type = data.get('simulation_type')
            parameters = data.get('parameters', {})
            room = data.get('room', simulation_type)
            
            self.stream_simulation(
                room, simulation_type, parameters
            )
    
    def cleanup_client(self, client_id):
        """Clean up client connections"""
        for room in list(self.active_rooms.keys()):
            if client_id in self.active_rooms[room]:
                self.active_rooms[room].remove(client_id)
            
            if not self.active_rooms[room]:
                del self.active_rooms[room]
    
    def stream_simulation(self, room, simulation_type, parameters):
        """Stream simulation updates to subscribed clients"""
        # This would be connected to real-time parameter updates
        pass
    
    def broadcast_energy_levels(self, room, energies):
        """Broadcast energy level updates"""
        self.socketio.emit('energy_update', {
            'energies': energies.tolist() if isinstance(energies, np.ndarray) else energies,
            'timestamp': datetime.now().isoformat()
        }, room=room)
    
    def broadcast_probability(self, room, probability, state_id):
        """Broadcast probability density updates"""
        self.socketio.emit('probability_update', {
            'state_id': state_id,
            'values': probability.tolist() if isinstance(probability, np.ndarray) else probability,
            'timestamp': datetime.now().isoformat()
        }, room=room)
    
    def broadcast_wavefunction(self, room, psi, state_id):
        """Broadcast wavefunction updates"""
        self.socketio.emit('wavefunction_update', {
            'state_id': state_id,
            'real': np.real(psi).tolist(),
            'imag': np.imag(psi).tolist(),
            'timestamp': datetime.now().isoformat()
        }, room=room)
    
    def broadcast_statistics(self, room, stats):
        """Broadcast quantum statistics"""
        self.socketio.emit('statistics_update', {
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }, room=room)
    
    def get_active_subscriptions(self):
        """Get info about active subscriptions"""
        return {
            room: {
                'subscribers': len(clients),
                'client_ids': clients
            }
            for room, clients in self.active_rooms.items()
        }
