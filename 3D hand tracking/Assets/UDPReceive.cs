
/*
Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry[url]https://github.com/Siliconifier/Python-Unity-Socket-Communication/blob/master/UdpSocket.cs]
Modified by: 
Julian Hom 02/2023 (removed obsolete calls to make this script suitable for just receiving data)
Youssef Elashry 12/2020 (replaced obsolete functions and improved further - works with Python as well)
Based on older work by Sandra Fang 2016 - Unity3D to MATLAB UDP communication - [url]http://msdn.microsoft.com/de-de/library/bb979228.aspx#ID0E3BAC[/url]
*/
using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class UDPReceive : MonoBehaviour
{
    public string data;
    [SerializeField] int rxPort = 2020; // port to receive data from Python on
    // Create necessary UdpClient objects
    UdpClient client;
    Thread receiveThread; // Receiving Thread
    public bool printToConsole = false;

    public void Start()
    {

        // Create local client
        client = new UdpClient(rxPort);

        // local endpoint define (where messages are received)
        // Create a new thread for reception of incoming messages
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
        // Initialize (seen in comments window)
        print("UDP Comms Initialised");
    }


    // receive thread
    private void ReceiveData()
    {
        while (true)
        {

            try
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] bytes = client.Receive(ref anyIP);
                data = Encoding.UTF8.GetString(bytes);
                if (printToConsole)
                {
                    print(data);
                }
            }
            catch (Exception err)
            {
                print(err.ToString());
            }
        }
    }
    //Prevent crashes - close clients and threads properly!
    void OnDisable()
    {
        if (receiveThread != null)
            receiveThread.Abort();

        client.Close();
    }

}