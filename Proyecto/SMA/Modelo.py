"""
Este módulo es el encargado de definir el modelo del sistema de tráfico, 
el cual contiene la lógica del sistema y los agentes que interactúan en él.
"""
from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from Agentes import Vehiculo, Celda, SemaforoVehicular, SemaforoPeatonal, Peaton
import random

class ModeloTrafico(Model):
    """
    Clase Modelo:
    
    La clase Modelo representa el sistema de tráfico, el cual contiene la lógica del sistema y los agentes que interactúan en él.
    
    Atributos:
        grid (MultiGrid): Grid que contiene a los agentes.
        schedule (SimultaneousActivation): Programa de activación de los agentes.
        semaforos (list): Lista de semáforos en el sistema.
        vehiculos (list): Lista de vehículos en el sistema.
        celdas (list): Lista de celdas en el sistema.
    
    Métodos:
        __init__(self, n, m, semaforos, vehiculos, celdas): Constructor de la clase Modelo.
        step(self): Realiza un paso de la simulación.
    """
    
    def __init__(self, width, height, semaforosV, semaforosP, transitables, intransitables, banquetas, estacionamientos):
        """
        Constructor de la clase Modelo.
        
        Parámetros:
            n (int): Número de columnas del grid.
            m (int): Número de filas del grid.
            semaforosV (list): Lista de semáforos vehiculares en el sistema.
            semaforosP (list): Lista de semáforos peatonales en el sistema.
            transitables (list): Lista de celdas transitables en el sistema.
            intransitables (list): Lista de celdas intransitables en el sistema.
            banquetas (list): Lista de banquetas en el sistema.
            estacionamientos (list): Lista de estacionamientos en el sistema.
        """
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.semaforosV = semaforosV
        self.semaforosP = semaforosP
        self.transitables = transitables
        self.intransitables = intransitables
        self.banquetas = banquetas
        self.estacionamientos = estacionamientos

        # Crear agentes para las celdas transitables
        for direction, celdas in transitables.items():
            for x, y in celdas:
                # Crear el agente Celda para cada coordenada (x, y)
                celda = Celda((x, y), self, direction, color="green", layer=1, width=1, height=1)  # Definir color, capa y dimensiones
                self.grid.place_agent(celda, (x, y))  # Colocar la celda en el grid
                self.schedule.add(celda)  # Añadir el agente al planificador

        # Crear agentes para las celdas intransitables
        for x, y in intransitables:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="blue", layer=2, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para las banquetas
        for x, y in banquetas:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="gray", layer=3, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para los semáforos de vehículos
        for x, y in semaforosV:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="red", layer=4, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para los semáforos de peatones
        for x, y in semaforosP:
            # Crear el agente Celda para cada coordenada (x, y)
            celda = Celda((x, y), self, None, color="red", layer=5, width=0.5, height=0.5)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))
            self.schedule.add(celda)

        # Crear agentes para los estacionamientos
        for nombre, (x, y) in estacionamientos.items():
            # Usamos el nombre como dirección (esto puede ser modificado según tu necesidad)
            direction = nombre  # La dirección podría ser el nombre del estacionamiento (A, B, C, D)
            
            # Crear el agente Celda para cada estacionamiento con las coordenadas (x, y)
            celda = Celda((x, y), self, direction, color="yellow", layer=6, width=1, height=1)  # Definir color, capa y dimensiones
            self.grid.place_agent(celda, (x, y))  # Colocar la celda en el grid
            self.schedule.add(celda)  # Añadir el agente al planificador

        # Inicializar peatones en el modelo
        for i in range(1):  # Cambia el rango según el número de peatones deseado
            origen = random.choice(banquetas)
            destino = random.choice(banquetas)

            # Asegurarse de que el destino no sea igual al origen
            while destino == origen:
                destino = random.choice(banquetas)

            peaton = Peaton(i, self, origen, destino)
            self.grid.place_agent(peaton, origen)
            self.schedule.add(peaton)

        # Crear agentes para los vehículos
        for i in range(1):  # Cambia el rango según el número de vehículos deseado
            origen = random.choice(list(estacionamientos.values()))  # Coordenada (x, y)
            destino = random.choice(list(estacionamientos.values()))  # Coordenada (x, y)

            # Asegurarte de que el destino no sea igual al origen
            while destino == origen:
                destino = random.choice(list(estacionamientos.values()))

            # Crear y colocar el vehículo
            vehiculo = Vehiculo(i, self, origen, destino, self.semaforosV, self.transitables, self.estacionamientos)
            self.grid.place_agent(vehiculo, origen)  # Coloca el vehículo en el origen
            self.schedule.add(vehiculo)  # Añade el vehículo al planificador


    
    def step(self):
        """
        Realiza un paso de la simulación.
        """
        self.schedule.step()  # Ejecutar el planificador