using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[System.Serializable]
public class Points
{
    public List<Point> points;

    public static Points CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Points>(jsonString);
    }
}
