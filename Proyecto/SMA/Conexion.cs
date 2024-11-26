using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Conexion : MonoBehaviour
{
    const int NUM_OBJECTS = 5;
    GameObject activeCar; // Solo este carro será usado
    [SerializeField]
    List<Vector3> positions;

    float timeToUpdate = 1.0f;
    private float timer;

    public float dt;

    // Lista de nombres de GameObjects posibles
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
            if (www.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string msg = www.downloadHandler.text;
                Points step = Points.CreateFromJSON(msg);

                if (positions.Count == 0)
                {
                    // Inicialización de posiciones
                    positions = new List<Vector3>();
                }

                positions.Clear();
                foreach (Point pos in step.points)
                {
                    Vector3 myP = new Vector3(pos.x, 0.5f, pos.z);
                    positions.Add(myP);
                }

                // Mover el carro activo a las posiciones actualizadas
                if (activeCar != null && positions.Count > 0)
                {
                    for (int i = 0; i < positions.Count; i++)
                    {
                        activeCar.transform.position = positions[i];
                    }
                }
            }
        }
    }

    void Start()
    {
        timer = timeToUpdate;
        positions = new List<Vector3>();

        // Selección aleatoria de un GameObject para ser el único activo
        string randomCarName = carNames[Random.Range(0, carNames.Length)];
        activeCar = GameObject.Find(randomCarName);

        if (activeCar == null)
        {
            Debug.LogError($"GameObject with name {randomCarName} not found in the scene!");
        }
        else
        {
            Debug.Log($"Selected active car: {randomCarName}");
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
