using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Conexion : MonoBehaviour
{
    [SerializeField]
    private List<GameObject> carPrefabs; // Lista de prefabs de vehículos

    private List<GameObject> activeCars; // Lista de vehículos activos
    private List<Vector3> vehiclePositions;
    private List<Vector3> pedestrianPositions;
    private List<Vector3> cellPositions;

    private float timeToUpdate = 1.0f;
    private float timer;

    private void Start()
    {
        timer = timeToUpdate;

        vehiclePositions = new List<Vector3>();
        pedestrianPositions = new List<Vector3>();
        cellPositions = new List<Vector3>();
        activeCars = new List<GameObject>();

        StartCoroutine(RequestPositions());
    }

    private IEnumerator RequestPositions()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/datos";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError || www.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string msg = www.downloadHandler.text;
                SimulationData data = SimulationData.CreateFromJSON(msg);

                UpdatePositions(data);
                UpdateVehicles();
            }
        }
    }

    private void UpdatePositions(SimulationData data)
    {
        if (vehiclePositions == null) vehiclePositions = new List<Vector3>();
        if (pedestrianPositions == null) pedestrianPositions = new List<Vector3>();
        if (cellPositions == null) cellPositions = new List<Vector3>();

        vehiclePositions.Clear();
        pedestrianPositions.Clear();
        cellPositions.Clear();

        foreach (Point pos in data.vehiculos)
        {
            Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
            vehiclePositions.Add(myP);
        }

        foreach (Point pos in data.peatones)
        {
            Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
            pedestrianPositions.Add(myP);
        }

        foreach (Point pos in data.celdas)
        {
            Vector3 myP = new Vector3(pos.x, 0.0f, pos.z);
            cellPositions.Add(myP);
        }
    }

    private void UpdateVehicles()
    {
        // Si hay menos vehículos activos que posiciones, crear nuevos
        while (activeCars.Count < vehiclePositions.Count)
        {
            GameObject newCar = Instantiate(GetRandomCarPrefab());
            newCar.transform.localScale = new Vector3(0.08f, 0.08f, 0.08f); // Establece la escala del carro
            activeCars.Add(newCar);
        }

        // Si hay más vehículos activos que posiciones, destruir los extras
        while (activeCars.Count > vehiclePositions.Count)
        {
            GameObject carToRemove = activeCars[activeCars.Count - 1];
            activeCars.RemoveAt(activeCars.Count - 1);
            Destroy(carToRemove);
        }

        // Actualizar las posiciones de los vehículos activos
        for (int i = 0; i < activeCars.Count; i++)
        {
            activeCars[i].transform.position = vehiclePositions[i];
        }
    }

    private GameObject GetRandomCarPrefab()
    {
        if (carPrefabs.Count == 0)
        {
            Debug.LogError("No car prefabs assigned in the inspector!");
            return null;
        }

        int randomIndex = Random.Range(0, carPrefabs.Count);
        return carPrefabs[randomIndex];
    }

    private void Update()
    {
        timer -= Time.deltaTime;
        if (timer <= 0)
        {
            timer = timeToUpdate;
            StartCoroutine(RequestPositions());
        }
    }
}

[System.Serializable]
public class SimulationData
{
    public List<Point> celdas;
    public List<Point> peatones;
    public List<Point> vehiculos;

    public static SimulationData CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<SimulationData>(jsonString);
    }
}
