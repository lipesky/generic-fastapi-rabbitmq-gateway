from circuitbreaker import CircuitBreaker
from src.settings import get_settings

settings = get_settings()

class AppCuircuit(CircuitBreaker):
    FAILURE_THRESHOLD = settings.circuitbreaker_failure_threshold
    RECOVERY_TIMEOUT = settings.circuitbreaker_recovery_timeout