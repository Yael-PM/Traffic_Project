using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

// La clase Conexion se encarga de recibir datos de un cliente a través de una conexión TCP.
// Para ello, se configura un servidor en la dirección
// Lo unico que falta es el procesamiento de los datos recibidos
// Para ello se debe implementar el metodo ProcesarDatos

public class Conexion : MonoBehaviour
{
    private TcpListener server;
    private TcpClient client;
    private NetworkStream stream;

    void Start()
    {
        // Configurar el servidor
        server = new TcpListener(IPAddress.Parse("127.0.0.1"), 65432);
        server.Start();
        Debug.Log("Servidor iniciado en 127.0.0.1:65432");
    }

    void Update()
    {
        if (server.Pending())
        {
            client = server.AcceptTcpClient();
            stream = client.GetStream();

            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);

            // Procesar los datos recibidos
            ProcesarDatos(data);

            stream.Close();
            client.Close();
        }
    }

    void ProcesarDatos(string data)
    {
        // Aquí puedes procesar los datos recibidos y actualizar la escena de Unity
        Debug.Log("Datos recibidos: " + data);
    }

    void OnApplicationQuit()
    {
        server.Stop();
    }
}