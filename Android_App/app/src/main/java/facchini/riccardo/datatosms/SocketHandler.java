package facchini.riccardo.datatosms;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetSocketAddress;
import java.net.Socket;

public class SocketHandler implements Runnable
{
    
    private Socket socket;
    private BufferedReader inputStream;
    InetSocketAddress socketAddress;
    
    public SocketHandler(String serverIp, int serverPort) throws IOException
    {
        this.socket = new Socket();
        this.socketAddress = new InetSocketAddress(serverIp, serverPort);
    }
    
    public void connect()
    {
        try
        {
            this.socket.connect(socketAddress);
            this.inputStream = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        } catch (IOException e)
        {
            e.printStackTrace();
        }
    }
    
    public BufferedReader getInputStream()
    {
        
        return inputStream;
    }
    
    public void closeAll()
    {
        try
        {
            
            socket.close();
            inputStream.close();
        } catch (Exception e)
        {
            e.printStackTrace();
        }
    }
    
    @Override
    public void run()
    {
    
    }
}
