/*
 * @author Julian Hom
 * script to provide 3-DPositional vecotrs to Gameobject by receiveing data from python
 * concept from cv-zone 3d-handtracking' - course [URL]https://www.computervision.zone/courses/3d-hand-tracking/
 */
using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class HandPoints : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] handPoints;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        // receive Data from Python
        string data = udpReceive.data;
        // remove Brackets
        if (data.Length > 0)
        {
            data = data.Remove(0, 1);
            data = data.Remove(data.Length - 1, 1);
            string[] points = data.Split(',');

            // Points are received in format x1,y1,z1,x2,y2,z2 ...
            for (int i = 0; i < 21; i++)
            {
                float x = float.Parse(points[i * 3]) / 8;
                float y = float.Parse(points[i * 3 + 1]) / 8;
                float z = float.Parse(points[i * 3 + 2]) / 8;
                
                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
        }
    }
}
