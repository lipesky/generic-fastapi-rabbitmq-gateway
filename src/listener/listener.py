from src.infra.circuitbreaker.app_circuit import AppCuircuit
from src.infra.rabbitmq.broker import rpc

@AppCuircuit
@rpc("handler")
async def handler(**kargs):
    print('handler called with kargs=',kargs)
    pass

print('🟢 Listener *handler* set')