"""
Webhook system for external service integration
Allows third-party services to subscribe to simulation events
"""

import requests
from datetime import datetime
from typing import Dict, List, Callable
from enum import Enum
import json
import threading
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebhookEvent(Enum):
    """Available webhook events"""
    SIMULATION_COMPLETE = "simulation.complete"
    ENERGY_CALCULATED = "energy.calculated"
    TUNNELING_STARTED = "tunneling.started"
    WAVEFUNCTION_UPDATED = "wavefunction.updated"
    ERROR_OCCURRED = "error.occurred"
    CONVERGENCE_REACHED = "convergence.reached"


class WebhookRegistry:
    """Manages webhook registrations and event dispatch"""
    
    def __init__(self):
        self.webhooks: Dict[WebhookEvent, List[str]] = {
            event: [] for event in WebhookEvent
        }
        self.webhook_metadata: Dict[str, Dict] = {}
        self.event_queue = Queue()
        self.event_thread = threading.Thread(
            target=self._process_events, daemon=True
        )
        self.event_thread.start()
        self.max_retries = 3
        self.timeout = 5
    
    def register(self, event: WebhookEvent, webhook_url: str,
                 metadata: Dict = None) -> bool:
        """
        Register a webhook endpoint for an event
        
        Args:
            event: Event type to subscribe to
            webhook_url: URL to POST to when event occurs
            metadata: Optional metadata (name, description, etc.)
        
        Returns:
            True if registered, False if already registered
        """
        if webhook_url not in self.webhooks[event]:
            self.webhooks[event].append(webhook_url)
            self.webhook_metadata[webhook_url] = {
                'url': webhook_url,
                'event': event.value,
                'registered_at': datetime.now().isoformat(),
                'active': True,
                'retry_count': 0,
                'last_triggered': None,
                **(metadata or {})
            }
            logger.info(f"Webhook registered: {webhook_url} for {event.value}")
            return True
        return False
    
    def unregister(self, event: WebhookEvent, webhook_url: str) -> bool:
        """Unregister a webhook"""
        if webhook_url in self.webhooks[event]:
            self.webhooks[event].remove(webhook_url)
            if webhook_url in self.webhook_metadata:
                del self.webhook_metadata[webhook_url]
            logger.info(f"Webhook unregistered: {webhook_url}")
            return True
        return False
    
    def unregister_all(self, webhook_url: str) -> int:
        """Unregister webhook from all events"""
        count = 0
        for event in WebhookEvent:
            if self.unregister(event, webhook_url):
                count += 1
        return count
    
    def get_webhooks(self, event: WebhookEvent = None) -> Dict:
        """Get registered webhooks"""
        if event:
            return {
                'event': event.value,
                'webhooks': self.webhooks[event],
                'count': len(self.webhooks[event])
            }
        
        return {
            event.value: self.webhooks[event]
            for event in WebhookEvent
        }
    
    def trigger(self, event: WebhookEvent, payload: Dict) -> None:
        """
        Queue event for webhook dispatch
        
        Args:
            event: Event type
            payload: Event data to send
        """
        self.event_queue.put({
            'event': event,
            'payload': payload,
            'timestamp': datetime.now().isoformat()
        })
    
    def _process_events(self) -> None:
        """Process queued events and dispatch to webhooks"""
        while True:
            try:
                event_data = self.event_queue.get(timeout=1)
                event = event_data['event']
                payload = event_data['payload']
                
                for webhook_url in self.webhooks[event]:
                    self._dispatch_webhook(webhook_url, event, payload)
            
            except Exception as e:
                logger.debug(f"Event processing: {e}")
    
    def _dispatch_webhook(self, webhook_url: str, event: WebhookEvent,
                          payload: Dict) -> None:
        """Dispatch event to webhook with retries"""
        headers = {
            'Content-Type': 'application/json',
            'X-Webhook-Event': event.value,
            'X-Webhook-Timestamp': datetime.now().isoformat()
        }
        
        full_payload = {
            'event': event.value,
            'timestamp': datetime.now().isoformat(),
            'data': payload
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    webhook_url,
                    json=full_payload,
                    headers=headers,
                    timeout=self.timeout
                )
                
                # Update metadata
                if webhook_url in self.webhook_metadata:
                    self.webhook_metadata[webhook_url]['last_triggered'] = \
                        datetime.now().isoformat()
                    self.webhook_metadata[webhook_url]['last_status'] = \
                        response.status_code
                    self.webhook_metadata[webhook_url]['retry_count'] = 0
                
                logger.info(
                    f"Webhook delivered: {webhook_url} -> {response.status_code}"
                )
                return
            
            except requests.exceptions.Timeout:
                logger.warning(
                    f"Webhook timeout (attempt {attempt+1}/{self.max_retries}): "
                    f"{webhook_url}"
                )
            except requests.exceptions.ConnectionError:
                logger.warning(
                    f"Webhook connection error (attempt {attempt+1}/"
                    f"{self.max_retries}): {webhook_url}"
                )
            except Exception as e:
                logger.error(f"Webhook error: {webhook_url} -> {e}")
        
        # Mark as failed after retries
        if webhook_url in self.webhook_metadata:
            self.webhook_metadata[webhook_url]['retry_count'] += 1
            if self.webhook_metadata[webhook_url]['retry_count'] >= self.max_retries:
                self.webhook_metadata[webhook_url]['active'] = False
                logger.error(f"Webhook deactivated after {self.max_retries} retries: "
                            f"{webhook_url}")
    
    def get_status(self) -> Dict:
        """Get webhook system status"""
        return {
            'total_webhooks': sum(len(urls) for urls in self.webhooks.values()),
            'active_webhooks': len([m for m in self.webhook_metadata.values()
                                   if m.get('active', True)]),
            'events': self.get_webhooks(),
            'metadata': self.webhook_metadata,
            'queue_size': self.event_queue.qsize()
        }


class WebhookEventBuilder:
    """Helper class to build standardized webhook payloads"""
    
    @staticmethod
    def simulation_complete(sim_type: str, parameters: Dict,
                           results: Dict) -> Dict:
        """Build simulation complete event payload"""
        return {
            'simulation_type': sim_type,
            'parameters': parameters,
            'results': results,
            'completion_time': datetime.now().isoformat()
        }
    
    @staticmethod
    def energy_calculated(energies: List[float], labels: List[str] = None) -> Dict:
        """Build energy calculation event payload"""
        return {
            'energies': energies,
            'labels': labels or [f"E_{i}" for i in range(len(energies))],
            'count': len(energies),
            'ground_state': min(energies) if energies else None
        }
    
    @staticmethod
    def tunneling_started(barrier_height: float, particle_energy: float,
                         coefficients: Dict) -> Dict:
        """Build tunneling event payload"""
        return {
            'barrier_height': barrier_height,
            'particle_energy': particle_energy,
            'classically_forbidden': particle_energy < barrier_height,
            'transmission': coefficients.get('transmission', 0),
            'reflection': coefficients.get('reflection', 0)
        }
    
    @staticmethod
    def error_occurred(error_message: str, error_type: str = "unknown",
                      context: Dict = None) -> Dict:
        """Build error event payload"""
        return {
            'error_message': error_message,
            'error_type': error_type,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def convergence_reached(iterations: int, tolerance: float,
                           final_error: float) -> Dict:
        """Build convergence event payload"""
        return {
            'iterations': iterations,
            'tolerance': tolerance,
            'final_error': final_error,
            'converged': final_error < tolerance
        }


# Global registry instance
webhook_registry = WebhookRegistry()
