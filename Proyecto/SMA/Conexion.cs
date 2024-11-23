using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Conexion : MonoBehaviour
{
    // Start is called before the first frame update

    const int NUM_OBJECTS = 20;
    List<GameObject> cars;
    [SerializeField]
    List<List<Vector3>> positions;

    float timeToUpdate = 1.0f;
    private float timer;
    public float dt;

    IEnumerator RequestPositions()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/datos";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {

            www.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
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
                    //GameObject car = GameObject.Find("Eduardo_Car");
                    List<Vector3> p = new List<Vector3>();
                    foreach (Point pos in step.points)
                    {
                        //GameObject car = GameObject.Find("Eduardo_Car");
                        GameObject car = GameObject.CreatePrimitive(PrimitiveType.Cube);
                        Vector3 myP = new Vector3(pos.x, 0, pos.z);
                        car.transform.position = myP;
                        p.Add(myP);
                        cars.Add(car);
                    }
                    positions.Add(p);
                }
                else
                {
                    List<Vector3> p = new List<Vector3>();
                    for (int i = 0; i < step.points.Count; i++)
                    {
                        //GameObject car = GameObject.Find("Eduardo_Car");
                        GameObject car = cars[i];
                        Point pos = step.points[i];
                        Vector3 myP = new Vector3(pos.x, 0, pos.z);
                        car.transform.position = myP;
                        p.Add(myP);
                        cars.Add(car);
                    }
                    positions.Add(p);
                }
            }
        }
    }

    void Start()
    {
        timer = timeToUpdate;
        positions = new List<List<Vector3>>();
        cars = new List<GameObject>();
        StartCoroutine(RequestPositions());
    }

    // Update is called once per frame
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
