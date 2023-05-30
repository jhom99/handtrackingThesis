/*
@author Julian Hom
collision detection script, that sends data to arduino for haptic feedback
*/
using System.IO;
using System.IO.Ports;
using UnityEngine;

public class CollisionDetection : MonoBehaviour
{

    private static SerialPort serial;

    void Start()
    {
        try
        {
            // try to establish connection on Serial Port with haptic device
            serial = new SerialPort("COM5", 9600);

            serial.Open();
            print("Collisionscript initialized");
        }
        catch (IOException e)
        {
            print($"Serial Port could not be opened: {e.Message}");
        }

    }
    void OnDestroy()
    {
        if (serial != null && serial.IsOpen)
        {
            serial.Close();
        }
    }

    void OnTriggerStay(Collider other)
    {
         if (other.gameObject.CompareTag("index"))
        {
            //change color of Object back to blue to indicate ongoing collision
            GetComponent<MeshRenderer>().material.color = Color.blue;
            //write 1 to indicate ongoing collision
            serial.Write("1");
        }

    }

    void OnTriggerExit(Collider other)
    {
      if (other.gameObject.CompareTag("index"))
        {
            //change color of Object back to white to indicate finsihed collision
            GetComponent<MeshRenderer>().material.color = Color.white;
            //write 0 to toindicate collision is finsihed
            serial.Write("0");
        }
    }
}