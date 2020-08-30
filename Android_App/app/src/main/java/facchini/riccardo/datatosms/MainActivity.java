package facchini.riccardo.datatosms;

import android.Manifest;
import android.app.Activity;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity
{
    //Constants
    private static final int MY_PERMISSIONS_REQUEST_SEND_SMS = 0;
    private static final String SHARED_NAME = "Local";
    
    //UI
    EditText etIP, etPort;
    TextView messagesView;
    ScrollView messageScrollView;
    //Button btnSend;
    
    //Variables
    //Thread Thread1 = null;
    String SERVER_IP;
    int SERVER_PORT;
    //private PrintWriter output;
    SocketHandler socketHandler;
    private BufferedReader input;
    private SharedPreferences sharedPreferences;
    private int index;
    private String lastNumber;
    private List<String> successful; // TODO: use to send back the information to the pc before closing the connection
    private List<String> errors; // TODO: use to send back the information to the pc before closing the connection
    private boolean isJobEnded;
    private boolean interrupt;
    private Thread sending;
    
    
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        
        // Set items in view
        setContentView(R.layout.activity_main);
        etIP = findViewById(R.id.etIP);
        etPort = findViewById(R.id.etPort);
        messagesView = findViewById(R.id.messagesView);
        messageScrollView = findViewById(R.id.messageScrollView);
        final Button btnConnect = findViewById(R.id.btnConnect);
        final Button btnDisconnect = findViewById(R.id.btnDisconnect);
        
        //Variables
        successful = new ArrayList<>();
        errors = new ArrayList<>();
        
        btnConnect.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                setText("");
                interrupt = false;
                SERVER_IP = etIP.getText().toString().trim();
                String serverPortString = etPort.getText().toString().trim();
                SERVER_PORT = Integer.parseInt(serverPortString);
                
                updatePreferences(SERVER_IP, serverPortString);
                
                sending = new Thread(new ConnectionSetter());
                sending.start();
                btnDisconnect.setEnabled(true);
                btnConnect.setEnabled(false);
            }
        });
        
        
        btnDisconnect.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                socketHandler.closeAll();
                sending.interrupt();
                endJob("Invio interrotto!");
                btnDisconnect.setEnabled(false);
                btnConnect.setEnabled(true);
                interrupt = true;
            }
        });
        
        setupPreferences();
        checkPermissions();
    }
    
    private void setupPreferences()
    {
        sharedPreferences = getSharedPreferences(SHARED_NAME, MODE_PRIVATE);
        etIP.setText(sharedPreferences.getString(getString(R.string.addressShared), ""));
        etPort.setText(sharedPreferences.getString(getString(R.string.portShared), ""));
    }
    
    private void updatePreferences(String address, String port)
    {
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString(getString(R.string.addressShared), address);
        editor.putString(getString(R.string.portShared), port);
        
        editor.apply();
    }
    
    
    class ConnectionSetter implements Runnable
    {
        
        @Override
        public void run()
        {
            socketHandler = null;
            try
            {
                socketHandler = new SocketHandler(SERVER_IP, SERVER_PORT);
                socketHandler.connect();
                if (Thread.currentThread().isInterrupted())
                    return;
                input = socketHandler.getInputStream();
                setText("Connessione riuscita\n");
                sendMessages();
            } catch (Exception e)
            {
                setText(String.format("Errore: %s\n", e.toString()));
                e.printStackTrace();
            }
        }
    }
    
    private void setText(final String text)
    {
        runOnUiThread(new Runnable()
        {
            @Override
            public void run()
            {
                messagesView.setText(text);
            }
        });
    }
    
    private void appendText(final String text)
    {
        runOnUiThread(new Runnable()
        {
            @Override
            public void run()
            {
                messagesView.append(text + "\n");
            }
        });
    }
    
    private BroadcastReceiver sendSMS;
    
    private void sendMessages()
    {
        successful.clear();
        errors.clear();
        index = 0;
        lastNumber = "";
        isJobEnded = false;
        try
        {
            final SmsManager smsManager = SmsManager.getDefault();
            String SENT = "SMS_SENT";
            final PendingIntent sentPI = PendingIntent.getBroadcast(this, 0, new Intent(SENT), 0);
            
            final JSONArray messages = new JSONArray(waitForInputLine());
            
            sendSMS = new BroadcastReceiver()
            {
                @Override
                public void onReceive(Context arg0, Intent arg1)
                {
                    if (isJobEnded || index < 0 || Thread.currentThread().isInterrupted())
                    {
                        unregisterReceiver(sendSMS);
                        return;
                    }
                    
                    if (getResultCode() == Activity.RESULT_OK)
                    {
                        appendText(index + "- Inviato messaggio a " + lastNumber);
                        successful.add(lastNumber);
                        
                        if (index >= messages.length())
                        {
                            isJobEnded = true;
                            sentPI.cancel();
                            unregisterReceiver(sendSMS);
                            endJob("Invio terminato!");
                            return;
                        }
                        
                    } else
                    {
                        appendText(index + "- Errore invio a " + lastNumber);
                        errors.add(lastNumber);
                    }
                    sendMessage(messages, smsManager, sentPI);
                }
            };
            
            registerReceiver(sendSMS, new IntentFilter(SENT));
            sendMessage(messages, smsManager, sentPI);
        } catch (JSONException e)
        {
            if (interrupt)
                return;
            setText(String.format("Errore: %s\n", e.toString()));
            e.printStackTrace();
        }
    }
    
    private void sendMessage(JSONArray messages, SmsManager smsManager, PendingIntent sentPI)
    {
        try
        {
            JSONObject item = messages.getJSONObject(index);
            lastNumber = item.getString("Cellulare");
            String content = item.getString("Messaggio");
            smsManager.sendTextMessage(lastNumber, null, content, sentPI, null);
            index++;
        } catch (JSONException e)
        {
            setText(String.format("Errore: %s\n", e.toString()));
            e.printStackTrace();
        }
    }
    
    private String waitForInputLine()
    {
        String inputText = "";
        try
        {
            inputText = input.readLine();
        } catch (Exception e)
        {
            setText(String.format("Errore: %s\n", e.toString()));
            e.printStackTrace();
        }
        return inputText;
    }
    
    private void endJob(String message) // TODO: before closing the connection this should send back the numbers that gave an error (or not sent) to the PC
    {
        index = -1;
        appendText(String.format("%s\nInviati: %d\nErrori: %d", message, successful.size(), errors.size()));
        socketHandler.closeAll();
    }


//    class Thread3 implements Runnable
//    {
//        private String message;
//
//        Thread3(String message)
//        {
//            this.message = message;
//        }
//
//        @Override
//        public void run()
//        {
//            output.write(message);
//            output.flush();
//            runOnUiThread(new Runnable()
//            {
//                @Override
//                public void run()
//                {
//                    tvMessages.append("client: " + message + "\n");
//                    etMessage.setText("");
//                }
//            });
//        }
//    }
    
    
    protected void checkPermissions()
    {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) != PackageManager.PERMISSION_GRANTED)
            if (!ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.SEND_SMS))
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.SEND_SMS}, MY_PERMISSIONS_REQUEST_SEND_SMS);
    }
    
}