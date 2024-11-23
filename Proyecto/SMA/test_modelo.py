import pytest
from Modelo import ModeloTrafico
from Agentes import Vehiculo, SemaforoVehicular, Celda, SemaforoPeatonal

def test_modelo_inicializacion():
    width = 25
    height = 25
    semaforosV = [(1, 7, 'H'), (7, 3, 'H')]
    semaforosP = [(3, 3)]
    transitables = [(1, 24, 'S'), (2, 24, 'O')]
    intransitables = [(3, 3, 'I'), (3, 4, 'I')]
    banquetas = [(4, 4, 'B')]
    estacionamientos = [(4, 22, 'P')]
    direcciones = {
        "N": (0, 1),
        "S": (0, -1),
        "E": (1, 0),
        "O": (-1, 0),
        "P": (0, 0)
    }

    modelo = ModeloTrafico(width, height, semaforosV, semaforosP, transitables, intransitables, banquetas, estacionamientos)
    
    assert modelo.grid.width == width
    assert modelo.grid.height == height
    assert len(modelo.schedule.agents) == len(transitables) + len(intransitables) + len(banquetas) + len(semaforosV) + len(semaforosP)

def test_semaforo_vehicular():
    modelo = ModeloTrafico(25, 25, [], [], [], [], [], [])
    semaforo = SemaforoVehicular(1, modelo, 'N')
    
    assert semaforo.state == "red"
    semaforo.step()
    # Aquí puedes agregar más aserciones dependiendo de la lógica de cambio de estado del semáforo

def test_celda():
    modelo = ModeloTrafico(25, 25, [], [], [], [], [], [])
    celda = Celda(1, modelo, direction='N', color="green", layer=1)
    
    assert celda.color == "green"
    assert celda.layer == 1

def test_enviar_estado():
    from conexion import enviar_estado
    modelo = ModeloTrafico(25, 25, [], [], [], [], [], [])
    celda = Celda(1, modelo, direction='N', color="green", layer=1)
    modelo.grid.place_agent(celda, (1, 1))
    modelo.schedule.add(celda)
    
    estado = enviar_estado(modelo)
    assert isinstance(estado, str)
    assert "Celda" in estado

if __name__ == "__main__":
    pytest.main()