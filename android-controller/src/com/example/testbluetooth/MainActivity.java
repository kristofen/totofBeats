package com.example.testbluetooth;

import android.os.Bundle;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.support.v4.app.NavUtils;

public class MainActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }

    static final int REQUEST_ENABLE_BT = 1;
    
	private btManager mgr = null;
    private ClientThread cThread = null; 
	
    /** Called when the user touches the button */
    public void btn1click(View view) {
        // Do something in response to button click
    	TextView txtResult = (TextView) findViewById(R.id.txtResult);
    	txtResult.setText("btn1click");
    	
    	BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    	if (mBluetoothAdapter == null) {
    	    // Device does not support Bluetooth
    		Log.w("testBluetooth","no support");
    		txtResult.setText("Device does not support Bluetooth");
    	} else {
    		Log.w("testBluetooth","support ok");
    		this.mgr = new btManager(mBluetoothAdapter);
    		// Device supports BlueTooth
    		if (!mBluetoothAdapter.isEnabled()) {
    			Log.w("testBluetooth","bluetooth not enabled");
    		    Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
    		    startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
    		} else {
    			Log.w("testBluetooth","bluetooth enabled");
    		}
    			
    		
    	}
    	
    }
    
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_ENABLE_BT) {
            if (resultCode == RESULT_OK) {
                // A contact was picked.  Here we will just display it
                // to the user.
            	Log.w("testBluetooth","user enabled bluetooth");
            } else {
            	// request cancelled
            	Log.w("testBluetooth","user cancelled bluetooth");
            }
        }
    }
    
    /** Called when the user touches the button */
    public void btn2click(View view) {
        // Do something in response to button click
    	TextView txtResult = (TextView) findViewById(R.id.txtResult);
    	if (this.mgr!=null) {
    		
    		if (this.cThread != null) {
    			// already connected 
    			
    		} else {
        		this.mgr.listPairedDevices(); 
        		BluetoothDevice d = this.mgr.getDevice();
        		if (d!=null) {
        			Log.w("testBluetooth","device not null, will create and start thread");
        			this.cThread = new ClientThread(d,this.mgr.adap);	
    				this.cThread.start();
        		}
    		}
    		EditText et = (EditText) findViewById(R.id.txtInput);
    		
    		try{
    			this.cThread.l.lock();
    			String msg = et.getText().toString();
				Log.w("testBluetooth","Queueing ("+msg+")");    					
    			this.cThread.msgs.add(msg);
    		} catch (Exception e) {
    			
    		} finally {
    			this.cThread.l.unlock();
    		}
    		
    		
    	}
    	txtResult.setText("btn2click");
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // The activity is about to be destroyed.
        if (this.cThread != null) {
        	this.cThread.cancel();
        	this.cThread  = null;
        }
    }
    
}