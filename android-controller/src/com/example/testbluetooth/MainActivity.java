package com.example.testbluetooth;

import android.os.Bundle;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.util.Log;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.support.v4.app.NavUtils;

public class MainActivity extends Activity {
	
/* Properties */
    private boolean isStart=false;
    private GridLayout baseGrid = null;
    static final int REQUEST_ENABLE_BT = 1;
	//private btManager mgr = null;
    //private ClientThread cThread = null; 
    private BluetoothManager btManager=null;
    
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        this.baseGrid = (GridLayout) findViewById(R.id.grid1);
        createGrid();
        btManager = new BluetoothManager();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }

    private void createGrid(){
    	// add play button
    	LinearLayout lin = (LinearLayout) findViewById(R.id.linLayout1);
    	Button playbtn = new Button(this);
    	playbtn.setId(1);
    	playbtn.setText("Play/Stop");
    	playbtn.setOnClickListener(new Button.OnClickListener() {  
	        public void onClick(View v)
	            {
	        		Button btn = (Button) v;
	        		MainActivity context = (MainActivity)btn.getContext();
	        		if (context.isStart==true){
	        			
	        		} else {
	        			
	        		}
	
	            }
	         });
    	lin.addView(playbtn,new LayoutParams(LayoutParams.WRAP_CONTENT,LayoutParams.WRAP_CONTENT));
    	
    	GridLayout.LayoutParams param = null;
        
    	for (int i=0;i<8;i++){
    		for (int j=0;j<16;j++){
	    		
    			Button newbtn = new Button(this); // using standard buttons because i'm not able to do a decent custom tickbutton
    			//TickButton newbtn = new TickButton(this);
	    		//newbtn.setText("a"+i+"_"+j);
	    		newbtn.setId(((i+1)*100)+j); // ids from 100 to 816 (xyy with x=track index+1 and y=tick nb)
	    		param =new GridLayout.LayoutParams();
	            param.height = LayoutParams.WRAP_CONTENT;
	            param.width = LayoutParams.WRAP_CONTENT;
	            //param.rightMargin = 5;
	            //param.topMargin = 5;
	            param.setGravity(Gravity.CENTER);
	            param.columnSpec = GridLayout.spec(j+1);
	            param.rowSpec = GridLayout.spec(i+1);
	    		newbtn.setLayoutParams(param);
	    		this.baseGrid.addView(newbtn); 

    		}    		
    	}
    }
    
    /** Called when the user touches the button isBluetooth Enabled */
    public void btnBluetoothEnabledClick(View view) {
    	/* ENABLE BLUETOOTH */
    	
    	if (!this.btManager.isSupported()) {
    	    // Device does not support Bluetooth
    		Log.w("testBluetooth","no support");
    	} else {
    		Log.w("testBluetooth","support ok");
    		if (!this.btManager.isEnabled()) {
    			// ask for activation
    			askForBluetooth();
    		} else {
    			// already enabled
    		}
    	}
    }
    
    private void askForBluetooth(){
	    Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
	    startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
    }
    
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    	/* RESULT OF REQUEST */
        if (requestCode == REQUEST_ENABLE_BT) {
            if (resultCode == RESULT_OK) {
            	Log.w("testBluetooth","user enabled bluetooth");
            } else {
            	Log.w("testBluetooth","user cancelled bluetooth");
            }
        }
    }
    
    /** Called when the user touches the button Send Bluetooth */
    public void btnSendBluetoothClick(View view) {
    	/* SEND TEXTBOX CONTENT TO BLUETOOTH SERVER */

		EditText et = (EditText) findViewById(R.id.txtInput);
		this.btManager.sendString(et.getText().toString());
		
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (this.btManager!=null){
        	this.btManager.stopClient();
        }
    }
    
}
