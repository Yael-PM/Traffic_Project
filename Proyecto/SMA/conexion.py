import socket
import json
from Model import ModeloTrafico
from Agentes import Vehiculo, Semaforo, Celda

# Configuración del socket
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto del servidor

"""
La manera de usar este script es ejecutarlo en paralelo con la simulación en Mesa.
El script se encarga de enviar el estado actual del modelo a Unity.
Para ello, se conecta a un servidor en Unity y envía el estado en formato JSON.
"""

def enviar_estado(model):
    """
    Envía el estado actual del modelo a Unity.
    Esto incluye la posición y estado de los agentes.
    Los agentes son de tres tipos: Vehiculo, Semaforo y Celda.
    """
    estado = []
    for agent in model.schedule.agents:
        if isinstance(agent, Vehiculo):
            estado.append({
                "type": "Vehiculo",
                "id": agent.unique_id,
                "pos": agent.pos,
                "direccion": agent.direccion,
                "estado": agent.estado
            })
        elif isinstance(agent, Semaforo):
            estado.append({
                "type": "Semaforo",
                "id": agent.unique_id,
                "pos": agent.pos,
                "state": agent.state,
                "direccion": agent.direccion
            })
        elif isinstance(agent, Celda):
            estado.append({
                "type": "Celda",
                "id": agent.unique_id,
                "pos": agent.pos,
                "direccion": agent.direccion
            })
    
    # Convertir el estado a JSON
    estado_json = json.dumps(estado)
    
    # Enviar el estado a Unity
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(estado_json.encode('utf-8'))

# Inicializar el modelo
model = ModeloTrafico()

# Ejecutar la simulación y enviar el estado a Unity
for _ in range(100):  # Número de pasos de la simulación
    model.step()
    enviar_estado(model)