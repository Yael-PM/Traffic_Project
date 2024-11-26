from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from Modelo import ModeloTrafico
from Agentes import Vehiculo, Peaton, Celda, SemaforoVehicular, SemaforoPeatonal

matrizTotal = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]

intransitables = [(0, 10), (1, 10), (2, 10), (9, 10), (10, 10), (11, 10), (0, 9), (1, 9), (2, 9), (9, 9), (10, 9), (11, 9), (0, 8), (1, 8), (2, 8), (9, 8), (10, 8), (11, 8), (0, 1), (1, 1), (2, 1), (9, 1), (10, 1), (11, 1), (0, 0), (1, 0), (2, 0), (9, 0), (10, 0), (11, 0)]

transitables = {
    "N": {(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10)}, 
    "O": {(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4)}, 
    "S": {(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10)},
    "E": {(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6)}, 
    "D": {(3, 1), (8, 1), (8, 8), (2, 7)}
}

banquetas = [(0, 2), (1, 2), (2, 2), (3, 2), (8, 2), (9, 2), (10, 2), (11, 2), (0, 7), (1, 7), (2, 7), (3, 7), (8, 7), (9, 7), (10, 7), (11, 7), (3, 10), (3, 9), (3, 8), (3, 1), (3, 0), (8, 10), (8, 9), (8, 8), (8, 1), (8, 0)]

estacionamientos = {"A": (2, 8), "B": (9, 1), "C": (2, 1), "D": (9, 8)}

semaforosV = [(8, 5), (8, 6), (4, 7), (5, 7), (6, 7), (7, 7), (3, 3), (3, 4)]

semaforosP = [(3, 2), (8, 2), (8, 7), (3, 7),]

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
        color = "green" if agent.estado == "verde" else "red"
        return {
            "Shape":"rect",
            "Filled":"true",
            "Layer":6,
            "Color":color,
            "w":0.5,
            "h":0.5
        }


# Crear el modelo y configurar el servidor
canvas_element = CanvasGrid(agentPortrayal, 12, 11, 500, 500)
model_params = {
    "width": 12,
    "height": 11,
    "semaforosV": semaforosV,
    "semaforosP": semaforosP,
    "transitables": transitables,
    "intransitables": intransitables,
    "banquetas": banquetas,
    "estacionamientos": estacionamientos
}
server = ModularServer(ModeloTrafico, [canvas_element], "Traffic Simulation", model_params)
server.port = 8521
server.launch()