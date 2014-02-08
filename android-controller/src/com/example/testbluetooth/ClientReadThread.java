package com.example.testbluetooth;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import android.bluetooth.BluetoothSocket;
import android.util.Log;

public class ClientReadThread extends Thread {

	InputStream is = null;
	boolean mustRun = false;
	
	public ClientReadThread(InputStream is){
		this.is=is;
	}
	
	 public void run() {
		 	Log.w("testBluetooth","ClientReadThread run");
		 	this.mustRun=true;
		 			
	        // Cancel discovery because it will slow down the connection
	        // mmAdap.cancelDiscovery();
	
	 
	        // Do work to manage the connection (in a separate thread)
	        doWork();
	    }
	 
	 private void doWork() {
		 try {
			 Log.w("testBluetooth","ClientReadThread start");
			 byte[] buffer = new byte[4*1024]; // 4K buffer
			 int ptrwrite=0;
			 
			 while(this.mustRun){
				 // is there enough buffer remaining ?
				 if (buffer.length-ptrwrite<100){
					 byte[] newbuf = new byte[buffer.length*2]; // redim
					 System.arraycopy(buffer,0,newbuf,0,ptrwrite);
					 buffer = newbuf;
				 }
				int nbread = this.is.read(buffer,ptrwrite,buffer.length-ptrwrite );
				if (nbread>0) {
					ptrwrite += nbread;
					int i=0;
					while (i<ptrwrite){
						if (buffer[i]=='\r'){
							if (i<ptrwrite-1 && buffer[i+1]=='\n'){
								// new command
								String s = new String(buffer,0,i);
								Log.w("testBluetooth","NEW RESPONSE resp="+s);
								System.arraycopy(buffer,i+2,buffer,0,ptrwrite-(i+2));
								ptrwrite-=(i+2);
								i = 0;
								Log.w("testBluetooth","newptrwrite="+ptrwrite);
							} else {
								i += 1;
							}
						} else {
							i += 1;
						}
					}
					Log.w("testBluetooth","read nb bytes="+nbread+", bufferlength="+buffer.length);
				} else {
					this.mustRun=false;
				}
			 	Thread.sleep(500);
			 }
		 } catch (InterruptedException ie) {
			 Log.w("testBluetooth","ClientReadThread interrupted");
		 } catch (Exception e) {
			 Log.w("testBluetooth","ClientReadThread  exception: "+e.getMessage());
		 }
		 Log.w("testBluetooth","ClientReadThread end");

	 }
	 
	 public void Close() {
		 Log.w("testBluetooth","ClientReadThread Close");
	   this.mustRun=false;
	   int nbretry=0;
	   while (nbretry<25 && this.isAlive()){
		   try {
			   Thread.sleep(500);
		   } catch (InterruptedException e) {
				// TODO Auto-generated catch block
			   e.printStackTrace();
		   }
		   nbretry+=1;
	   }
	   
	   if (this.isAlive()){
		   Log.w("testBluetooth","ClientReadThread interrupt");
		   this.interrupt();
	   }
	   Log.w("testBluetooth","ClientReadThread Close end");
			   
	 }
	 
}
