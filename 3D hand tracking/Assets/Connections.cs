/*
 * @author Julian Hom
 * script to render Lines betwenn handpoints
 * concept from cv-zone 3d-handtracking' - course [URL]https://www.computervision.zone/courses/3d-hand-tracking/
 */
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Connections : MonoBehaviour
{
    LineRenderer lineRenderer;

    public Transform startPoint;
    public Transform endPoint;

    // Start is called before the first frame update

    void Start()
    {
        //set line - thickness on start and end point
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.startWidth = 0.2f;
        lineRenderer.endWidth = 0.2f;
    }

    // Update is called once per frame
    void Update()
    {
        //position line between two given handpoints
        lineRenderer.SetPosition(0, startPoint.position);
        lineRenderer.SetPosition(1, endPoint.position);
    }
}
