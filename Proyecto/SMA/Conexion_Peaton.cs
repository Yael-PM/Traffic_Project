using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class PedestrianManager : MonoBehaviour
{
    [SerializeField]
    private List<GameObject> activePedestrians; // Lista de peatones activos
    [SerializeField]
    private List<Vector3> pedestrianPositions;

    float timeToUpdate = 1.0f;
    private float timer;

    // Nombres de los GameObjects de peatones en la escena
    string[] pedestrianNames = { "Alex", "Steve"};

    IEnumerator RequestPedestrianPositions()
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
                Debug.LogError(www.error);
            }
            else
            {
                string msg = www.downloadHandler.text;
                SimulationData data = SimulationData.CreateFromJSON(msg);

                if (pedestrianPositions == null) pedestrianPositions = new List<Vector3>();
                pedestrianPositions.Clear();

                // Procesar las posiciones de los peatones
                foreach (Point pos in data.peatones)
                {
                    Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
                    pedestrianPositions.Add(myP);
                }

                // Mover los peatones activos a las posiciones actualizadas
                if (activePedestrians != null && activePedestrians.Count > 0 && pedestrianPositions.Count > 0)
                {
                    for (int i = 0; i < Mathf.Min(activePedestrians.Count, pedestrianPositions.Count); i++)
                    {
                        activePedestrians[i].transform.position = pedestrianPositions[i];
                    }
                }
            }
        }
    }

    void Start()
    {
        timer = timeToUpdate;
        pedestrianPositions = new List<Vector3>();
        activePedestrians = new List<GameObject>();

        // Selección de varios GameObjects para ser activos
        foreach (string pedestrianName in pedestrianNames)
        {
            GameObject pedestrian = GameObject.Find(pedestrianName);
            if (pedestrian != null)
            {
                activePedestrians.Add(pedestrian);
                Debug.Log($"Pedestrian added to active list: {pedestrianName}");
            }
            else
            {
                Debug.LogWarning($"GameObject with name {pedestrianName} not found in the scene!");
            }
        }

        if (activePedestrians.Count == 0)
        {
            Debug.LogError("No active pedestrians found in the scene!");
        }
        else
        {
            Debug.Log($"{activePedestrians.Count} pedestrians added to active list.");
        }

        StartCoroutine(RequestPedestrianPositions());
    }

    void Update()
    {
        timer -= Time.deltaTime;
        if (timer <= 0)
        {
            timer = timeToUpdate;
            StartCoroutine(RequestPedestrianPositions());
        }
    }
}
