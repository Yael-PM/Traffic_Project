using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Conexion : MonoBehaviour
{
    [SerializeField]
    List<GameObject> activeCars; // Lista de carros activos
    [SerializeField]
    List<Vector3> vehiclePositions;
    [SerializeField]
    List<Vector3> pedestrianPositions;
    [SerializeField]
    List<Vector3> cellPositions;

    float timeToUpdate = 1.0f;
    private float timer;

    public float dt;

    // Lista de nombres de GameObjects posibles para vehículos
    string[] carNames = { "Eduardo_Car", "Emiliano_Car", "Carro_Yael", "Carro_Olmos" };

    IEnumerator RequestPositions()
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

                if (vehiclePositions == null) vehiclePositions = new List<Vector3>();
                if (pedestrianPositions == null) pedestrianPositions = new List<Vector3>();
                if (cellPositions == null) cellPositions = new List<Vector3>();

                vehiclePositions.Clear();
                pedestrianPositions.Clear();
                cellPositions.Clear();

                // Procesar las posiciones de los vehículos
                foreach (Point pos in data.vehiculos)
                {
                    Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
                    vehiclePositions.Add(myP);
                }

                // Procesar las posiciones de los peatones
                foreach (Point pos in data.peatones)
                {
                    Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
                    pedestrianPositions.Add(myP);
                }

                // Procesar las posiciones de las celdas
                foreach (Point pos in data.celdas)
                {
                    Vector3 myP = new Vector3(pos.x, 0.0f, pos.z);
                    cellPositions.Add(myP);
                }

                // Mover todos los carros activos a las posiciones actualizadas
                if (activeCars != null && activeCars.Count > 0 && vehiclePositions.Count > 0)
                {
                    for (int i = 0; i < Mathf.Min(activeCars.Count, vehiclePositions.Count); i++)
                    {
                        activeCars[i].transform.position = vehiclePositions[i];
                    }
                }
            }
        }
    }

    void Start()
    {
        timer = timeToUpdate;
        vehiclePositions = new List<Vector3>();
        pedestrianPositions = new List<Vector3>();
        cellPositions = new List<Vector3>();
        activeCars = new List<GameObject>();

        // Selección de varios GameObjects para ser activos
        foreach (string carName in carNames)
        {
            GameObject car = GameObject.Find(carName);
            if (car != null)
            {
                activeCars.Add(car);
                Debug.Log($"Car added to active list: {carName}");
            }
            else
            {
                Debug.LogWarning($"GameObject with name {carName} not found in the scene!");
            }
        }

        if (activeCars.Count == 0)
        {
            Debug.LogError("No active cars found in the scene!");
        }
        else
        {
            Debug.Log($"{activeCars.Count} cars added to active list.");
        }

        StartCoroutine(RequestPositions());
    }

    void Update()
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
