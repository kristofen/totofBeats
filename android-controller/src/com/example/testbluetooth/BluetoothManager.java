package com.example.testbluetooth;

import java.util.Set;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.util.Log;

public class BluetoothManager {
	
/** PROPERTIES **/
	static final String BTSERVERMAC = "BC:85:56:34:85:BC"; // << define here the MAC address of bluetooth server 
	private BluetoothAdapter mAdapter=null;
	private boolean mIsClientUp=false;
	public boolean isClientUp(){
		return this.mIsClientUp;
	}
	
	private BluetoothClient client=null;
	
/** CONSTRUCTOR **/	
	public BluetoothManager(){
		getAdapter();
	}

/** METHODS **/	
	
	public boolean isSupported(){
		if (this.mAdapter!=null){
			return true;
		} else {
			return false;
		} 
	}	
	
	public boolean isEnabled(){
		if (this.mAdapter!=null){
			return this.mAdapter.isEnabled();
		} else {
			return false;
		}
	}
	
	private void getAdapter(){
		this.mAdapter = BluetoothAdapter.getDefaultAdapter();
	}
	
	public BluetoothDevice getDevice() {

		Set<BluetoothDevice> pairedDevices = this.mAdapter.getBondedDevices();
		// If there are paired devices
		BluetoothDevice d = null;
		if (pairedDevices.size() > 0) {
		    // Loop through paired devices
		    for (BluetoothDevice device : pairedDevices) {
		        // Add the name and address to an array adapter to show in a ListView
		    	Log.w("testBluetooth","BT Device Name=" + device.getName() + ", Address=(" + device.getAddress() + ")");
		    	String ds = device.getAddress();
		    	if (ds.equals(BTSERVERMAC)) {
		    		d = device;
		    		Log.w("testBluetooth","device found");
		    	} else {
		    		Log.w("testBluetooth","not matching");
		    	}
		    }
		}
		return d;
	}

	public void startClient(){
		// if client already up no need to start it
		if (this.isClientUp()) { return ;}
		if (!this.isSupported()) { return ;}
		
		//this.mgr.listPairedDevices(); 
		BluetoothDevice d = this.getDevice();
		if (d!=null) {
			Log.w("testBluetooth","device not null, will create and start thread");
			this.client = new BluetoothClient(d,this.mAdapter);	
			this.client.start();
			this.mIsClientUp=true;
		} else {
			Log.w("testBluetooth","Failed to get default device. Client not started.");
		}
		
	}
	
	public void stopClient(){
		// if client already stopped no need to stop it
		if (!this.isClientUp()) { return; }
        // The activity is about to be destroyed.
        if (this.client != null) {
        	this.client.cancel();
        	this.client  = null;
        	this.mIsClientUp=false;
        }  
	}
	
	public void sendString(String msg){
		if (!this.isClientUp()){
			this.startClient();
		}
		if (this.client!=null){
			this.client.send(msg);
		}
		/*try{
			this.cThread.l.lock();
			String msg = et.getText().toString();
			Log.w("testBluetooth","Queueing ("+msg+")");    					
			this.cThread.msgs.add(msg);
		} catch (Exception e) {
			
		} finally {
			this.cThread.l.unlock();
		}*/
	}
	
}
