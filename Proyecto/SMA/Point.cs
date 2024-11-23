using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class Point
{
    public float x;
    public float z;

    public static Point FromJson(string jsonString)
    {
        return JsonUtility.FromJson<Point>(jsonString);
    }
}
