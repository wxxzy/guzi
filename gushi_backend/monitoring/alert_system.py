"""
Alert System
Responsible for sending system alerts and notifications
"""
import smtplib
import logging
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, List
import json

from monitoring.config import MonitoringConfig

class AlertSystem:
    """Alert System Class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_history = []
        self.suppressed_alerts = set()
    
    def send_alert(self, alert_type: str, message: str, severity: str = 'medium'):
        """Send Alert"""
        # Check if this alert should be suppressed
        alert_key = f"{alert_type}:{message}"
        if alert_key in self.suppressed_alerts:
            self.logger.debug(f"Alert suppressed: {alert_key}")
            return
        
        # Record alert
        alert_record = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'message': message,
            'severity': severity
        }
        
        self.alert_history.append(alert_record)
        
        # Limit history size
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
        
        # Send alert based on configuration
        try:
            if MonitoringConfig.ENABLE_ALERTS:
                # Send email alert
                if MonitoringConfig.ALERT_EMAIL_RECIPIENTS and any(MonitoringConfig.ALERT_EMAIL_RECIPIENTS):
                    self._send_email_alert(alert_type, message, severity)
                
                # Send webhook alert
                if MonitoringConfig.ALERT_WEBHOOK_URL:
                    self._send_webhook_alert(alert_type, message, severity)
                
                self.logger.info(f"Alert sent: {alert_type} - {severity}")
            else:
                self.logger.debug(f"Alert system disabled, alert not sent: {alert_type}")
        except Exception as e:
            self.logger.error(f"Error sending alert: {e}")
    
    def _send_email_alert(self, alert_type: str, message: str, severity: str):
        """Send Email Alert"""
        try:
            # Here should configure actual email sending service
            # For demonstration, we only log
            self.logger.info(f"Simulating email alert sending: type={alert_type}, severity={severity}, message={message}")
            
            # Actual implementation should be similar to this:
            """
            msg = MIMEMultipart()
            msg['From'] = 'alerts@gushi-system.com'
            msg['To'] = ', '.join(MonitoringConfig.ALERT_EMAIL_RECIPIENTS)
            msg['Subject'] = f"[Gushi System Alert] {severity.upper()}: {alert_type}"
            
            body = f"""
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Type: {alert_type}
            Severity: {severity}
            Message: {message}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')
            text = msg.as_string()
            server.sendmail('your_email@gmail.com', MonitoringConfig.ALERT_EMAIL_RECIPIENTS, text)
            server.quit()
            """
        except Exception as e:
            self.logger.error(f"Error sending email alert: {e}")
    
    def _send_webhook_alert(self, alert_type: str, message: str, severity: str):
        """Send Webhook Alert"""
        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'type': alert_type,
                'severity': severity,
                'message': message
            }
            
            response = requests.post(
                MonitoringConfig.ALERT_WEBHOOK_URL,
                json=payload,
                timeout=10
            )
            
            if response.status_code not in [200, 201, 204]:
                self.logger.error(f"Webhook alert sending failed, status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error sending webhook alert: {e}")
    
    def suppress_alerts(self, alert_keys: List[str], duration_minutes: int = 60):
        """Temporarily suppress alerts"""
        for key in alert_keys:
            self.suppressed_alerts.add(key)
        
        # Set timer to unsuppress after specified time
        # In actual implementation, should use scheduler
        self.logger.info(f"Suppressed {len(alert_keys)} alerts for {duration_minutes} minutes")
    
    def get_alert_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get alert history"""
        return self.alert_history[-limit:] if self.alert_history else []
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get active alerts"""
        # In this simplified implementation, return recent alerts
        # Actual implementation should track unresolved alerts
        recent_alerts = []
        if self.alert_history:
            # Get alerts from last hour
            one_hour_ago = datetime.now().timestamp() - 3600
            for alert in reversed(self.alert_history[-100:]):  # Check last 100 alerts
                try:
                    alert_time = datetime.fromisoformat(alert['timestamp']).timestamp()
                    if alert_time > one_hour_ago:
                        recent_alerts.append(alert)
                except Exception:
                    # Time parsing failed, skip
                    continue
        
        return recent_alerts
    
    def clear_alert_history(self):
        """Clear alert history"""
        self.alert_history.clear()
        self.logger.info("Alert history cleared")

# Create global alert system instance
alert_system = AlertSystem()