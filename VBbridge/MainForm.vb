Imports System.Text
Imports MQTTnet
Imports MQTTnet.Client
Imports MQTTNet.Client.Disconnecting
Imports MQTTnet.Extensions.ManagedClient
Imports MQTTnet.Protocol

Module MQTTBridge
    Private mClient As IManagedMqttClient

    ''' <summary>
    ''' Synchronous entry point.  
    ''' Blocks on the async startup loop.
    ''' </summary>
    Sub Main()
        Console.WriteLine("VB Side")
        ' Call the real async startup method and wait for it.
        MainAsync().GetAwaiter().GetResult()

    End Sub

    ''' <summary>
    ''' async MQTT setup + loop
    ''' </summary>
    Private Async Function MainAsync() As Task
        mClient = New MqttFactory().CreateManagedMqttClient()

        mClient.UseApplicationMessageReceivedHandler(AddressOf OnMessage)
        mClient.UseDisconnectedHandler(AddressOf OnDisconnected)

        Dim opts = New ManagedMqttClientOptionsBuilder() _
                       .WithClientOptions(Function(b) b.
                           WithTcpServer("localhost", 1883). 'default Local host and port ******************************************
                           WithCleanSession().
                           WithKeepAlivePeriod(TimeSpan.FromSeconds(30)).
                           Build()) _
                       .WithAutoReconnectDelay(TimeSpan.FromSeconds(5)).
                       Build()

        Await mClient.StartAsync(opts)
        Await mClient.SubscribeAsync("py_to_vb")

        While True
            'Await SendToPython($"VB tick {DateTime.Now:T}")
            Await SendToPython(Message)

            Await Task.Delay(11000)
        End While
    End Function

    Private Function OnMessage(e As MqttApplicationMessageReceivedEventArgs) As Task
        Dim payload = If(e.ApplicationMessage?.Payload IsNot Nothing,
                         Encoding.UTF8.GetString(e.ApplicationMessage.Payload),
                         "[no payload]")
        Console.WriteLine($"Python says: {payload}")
        Return Task.CompletedTask
    End Function

    Private Function OnDisconnected(e As MqttClientDisconnectedEventArgs) As Task
        Dim reasonText = e.Reason.ToString()
        Dim errorText = If(e.Exception IsNot Nothing,
                           $" Error: {e.Exception.Message}",
                           String.Empty)
        Console.WriteLine($"⚠ Disconnected ({reasonText}){errorText}. Reconnecting in 5 s…")
        Return Task.CompletedTask
    End Function

    'Topic is vb_to_py ******************************************************************************************
    Public Async Function SendToPython(text As String) As Task
        Await mClient.PublishAsync("vb_to_py",
                                   text,
                                   MqttQualityOfServiceLevel.AtLeastOnce)
    End Function
    '****************************************************************************************************************
    ''' <summary>
    ''' Returns str to publish to be called
    ''' Change this so this to get and read graph malformed and send instructions to python
    ''' </summary>
    Public Function Message()
        Dim text = "Graph is malformed!!!"
        Return text

    End Function

End Module

