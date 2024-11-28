from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Modelo import ModeloTrafico
from ConfMapa import semaforosV, semaforosP, transitables, intransitables, banquetas, estacionamientos
from Agentes import  Peaton, Celda, SemaforoVehicular, SemaforoPeatonal, Vehiculo
#from Vehiculo import Vehiculo

def agentPortrayal(agent):
    """Función de representación de los agentes."""
    if isinstance(agent, Celda):
        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": agent.layer,  # Define la capa del agente
            "Color": agent.color,  # Utiliza el color definido en el agente
            "w": agent.width,  # Ancho de la celda
            "h": agent.height  # Alto de la celda
        }
    elif isinstance(agent, Peaton):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 7,
            "Color": "black",
            "r": 0.5  # Radio del círculo para el peatón
        }
    elif isinstance(agent, Vehiculo):
        return {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 8,
            "Color": "purple",
            "r": 0.5  # Radio del círculo para el peatón
        }
    elif isinstance(agent, SemaforoVehicular):
        color = {
            "verde":"green",
            "amarillo":"yellow",
            "rojo":"red"
        }[agent.state]
        return{
            "Shape": "rect",
            "Filled": "true",
            "Layer": 6,  
            "Color": color, 
            "w": 1, 
            "h": 1 
        }
    elif isinstance(agent, SemaforoPeatonal):
        color = "green" if agent.state == "verde" else "red"
        return {
            "Shape":"rect",
            "Filled":"true",
            "Layer":6,
            "Color":color,
            "w":0.5,
            "h":0.5
        }


# Crear el modelo y configurar el servidor
canvas_element = CanvasGrid(agentPortrayal, 24, 24, 500, 500)
model_params = {
    "width": 24,
    "height": 24,
    "semaforosV": semaforosV,
    "semaforosP": semaforosP,
    "transitables": transitables,
    "intransitables": intransitables,
    "banquetas": banquetas,
    "estacionamientos": estacionamientos
}
server = ModularServer(ModeloTrafico, [canvas_element], "Traffic Simulation", model_params)
server.port = 852
server.launch()
