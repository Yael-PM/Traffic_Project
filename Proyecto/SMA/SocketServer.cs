using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class SocketServer : MonoBehaviour
{
    private TcpListener server;
    private Thread serverThread;

    public int port = 65432;

    void Start()
    {
        serverThread = new Thread(new ThreadStart(StartServer));
        serverThread.IsBackground = true;
        serverThread.Start();
    }

    void StartServer()
    {
        server = new TcpListener(IPAddress.Parse("127.0.0.1"), port);
        server.Start();
        Debug.Log("Server started on port " + port);

        while (true)
        {
            try
            {
                TcpClient client = server.AcceptTcpClient();
                NetworkStream stream = client.GetStream();

                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                Debug.Log("Received data: " + data);

                // Process the data here

                client.Close();
            }
            catch (Exception e)
            {
                Debug.LogError("Server error: " + e.Message);
            }
        }
    }

    void OnApplicationQuit()
    {
        server.Stop();
        serverThread.Abort();
    }
}