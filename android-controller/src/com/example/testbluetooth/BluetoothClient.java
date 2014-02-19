package com.example.testbluetooth;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.UUID;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

import android.R.string;
import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.util.Log;

public class BluetoothClient extends Thread {
	
	//private static final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
	//94f39d29-7d6d-437d-973b-fba39e49d4ee
	//private static final UUID MY_UUID = UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee");
	private final BluetoothSocket mmSocket;
	//private final BluetoothDevice mmDevice;
	//private final BluetoothAdapter mmAdap;
	
	protected Lock l = new ReentrantLock();
	protected List<String> msgs = null;
	
	@SuppressLint("NewApi")
	public BluetoothClient(BluetoothDevice device,BluetoothAdapter adap) {
		 	this.msgs = new ArrayList<String>(10);
	        // Use a temporary object that is later assigned to mmSocket,
	        // because mmSocket is final
	        BluetoothSocket tmp = null;
	       // mmDevice = device;
	        //mmAdap = adap;
	        // Get a BluetoothSocket to connect with the given BluetoothDevice
	        try {
	            // MY_UUID is the app's UUID string, also used by the server code
	            //tmp = device.createRfcommSocketToServiceRecord(MY_UUID);
	        	//tmp = device.createInsecureRfcommSocketToServiceRecord(MY_UUID);
	        	Method m = device.getClass().getMethod("createRfcommSocket", new Class[] {int.class});
	            tmp = (BluetoothSocket) m.invoke(device, 1);
	        	
	        } catch (NoSuchMethodException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalArgumentException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (InvocationTargetException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	        mmSocket = tmp;
	    }
	 	 
	 public void run() {
		 	Log.w("testBluetooth","thread run");
	        // Cancel discovery because it will slow down the connection
	        // mmAdap.cancelDiscovery();
	 
	        try {
	            // Connect the device through the socket. This will block
	            // until it succeeds or throws an exception
	        	Log.w("testBluetooth","thread run connect...");
	            mmSocket.connect();
	            Log.w("testBluetooth","thread run connect ok");
	        } catch (IOException connectException) {
	            // Unable to connect; close the socket and get out
	            try {
	            	Log.w("testBluetooth","thread run close exception:"+connectException.getMessage());
	                mmSocket.close();
	            } catch (IOException closeException) { }
	            return;
	        }
	 
	        // Do work to manage the connection (in a separate thread)
	        doWork(mmSocket);
	    }
	 
	 private void doWork(BluetoothSocket s) {
		 ClientReadThread clientread = null;
		 try {
			 Log.w("testBluetooth","DoWork start");
			 OutputStream os = s.getOutputStream();
			 InputStream is = s.getInputStream();
			 clientread = new ClientReadThread(is);
			 clientread.start();
			 while(true){
				 // will lock because we process message stack
				 this.l.lock();  // block until condition holds
			     try {
			       // ... method body
					 if (this.msgs.size()>0) {
							 int i;
							 for (i=0; i<this.msgs.size(); i++) {
								String a =  this.msgs.get(i);
								a += "\r\n";
								byte[] buffer = a.getBytes();
								os.write(buffer);					 
							 }
							 this.msgs.clear();
					 }
			     } finally {
				       this.l.unlock(); // unlock msg stack
			     }				 
			 	Thread.sleep(50);
			 }
		 } catch (Exception e) {
			 Log.w("testBluetooth","Exception:"+e.getMessage());
		 }
		 if (clientread!=null){
			 clientread.Close();
		 }
		 Log.w("testBluetooth","DoWork end");

	 }
	 
	 public void cancel() {
	        try {
	            mmSocket.close();
	        } catch (IOException e) { }
	    }
	
	 public void send(String s){
		 this.l.lock();  // block until condition holds
		 try {
			 Log.w("testBluetooth","must send command="+s);
			 this.msgs.add(s);
		 } finally {
		       this.l.unlock(); // unlock msg stack
	     }	
	 }
	 
}
