package com.example.testbluetooth;

import java.util.Set;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.util.Log;

public class btManager {

	protected BluetoothAdapter adap = null;
	
    public btManager(BluetoothAdapter adap) {
		super();
		this.adap = adap;
	}
	
	public void listPairedDevices() {
		
		Set<BluetoothDevice> pairedDevices = this.adap.getBondedDevices();
		// If there are paired devices
		if (pairedDevices.size() > 0) {
		    // Loop through paired devices
		    for (BluetoothDevice device : pairedDevices) {
		        // Add the name and address to an array adapter to show in a ListView
		    	Log.w("testBluetooth","BT Device Name=" + device.getName() + ", Address=" + device.getAddress());
		        //mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
		    }
		}
		
	}

	public BluetoothDevice getDevice() {
		// TODO Auto-generated method stub
		Set<BluetoothDevice> pairedDevices = this.adap.getBondedDevices();
		// If there are paired devices
		BluetoothDevice d = null;
		if (pairedDevices.size() > 0) {
		    // Loop through paired devices
		    for (BluetoothDevice device : pairedDevices) {
		        // Add the name and address to an array adapter to show in a ListView
		    	Log.w("testBluetooth","BT Device Name=" + device.getName() + ", Address=(" + device.getAddress() + ")");
		    	String ds = device.getAddress();
		    	//String test = "13:FA:5D:C9:10:9A";
		    	String test = "BC:85:56:34:85:BC";
		    	if (ds.equals(test)) {
		    		d = device;
		    		Log.w("testBluetooth","device found");
		    	} else {
		    		Log.w("testBluetooth","not matching");
		    	}
		    	
		        //mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
		    }
		}
		return d;
	}
	
}


//
//private class ConnectThread extends Thread {
//private final BluetoothSocket mmSocket;
//private final BluetoothDevice mmDevice;
//public ConnectThread(BluetoothDevice device) {
//// Use a temporary object that is later assigned to mmSocket,
//// because mmSocket is final
//BluetoothSocket tmp = null;
//mmDevice = device;
//// Get a BluetoothSocket to connect with the given BluetoothDevice
//try {
//// MY_UUID is the app's UUID string, also used by the server code
//tmp = device.createRfcommSocketToServiceRecord(MY_UUID);
//} catch (IOException e) { }
//mmSocket = tmp;
//}
//public void run() {
//// Cancel discovery because it will slow down the connection
//mBluetoothAdapter.cancelDiscovery();
//try {
//// Connect the device through the socket. This will block
//// until it succeeds or throws an exception
//mmSocket.connect();
//} catch (IOException connectException) {
//// Unable to connect; close the socket and get out
//try {
//mmSocket.close();
//} catch (IOException closeException) { }
//return;
//}
//05/03/13 Bluetooth | Android Developers
//developer.android.com/guide/topics/connectivity/bluetooth.html 11/15
//// Do work to manage the connection (in a separate thread)
//manageConnectedSocket(mmSocket);
//}
///** Will cancel an in-progress connection, and close the socket */
//public void cancel() {
//try {
//mmSocket.close();
//} catch (IOException e) { }