package com.example.testbluetooth;

public class CommandProcessor {
	/*
	 * Class that sends command to bluetooth server 
	 * 
	 */
	private BluetoothManager mBtManager=null;
	
	public CommandProcessor(BluetoothManager btManager){
		this.mBtManager=btManager;
	}
	
	public void cmdStartEngine(){
		this.mBtManager.sendString("corestart");
	}
	public void cmdStopEngine(){
		this.mBtManager.sendString("corestop");
	}
	public void cmdPauseEngine(){
		this.mBtManager.sendString("corepause");
	}	
	public void cmdCue(int tickPos){
		this.mBtManager.sendString("corecue "+tickPos+"");
	}
	public void cmdGridWidth(int nbticks){
		this.mBtManager.sendString("gridwidth "+nbticks+"");
	}	
	public void cmdGridHeight(int nbtracks){
		this.mBtManager.sendString("gridheight "+nbtracks+"");
	}
	public void cmdGridAddRow(String file){
		this.mBtManager.sendString("gridaddrow "+file+"");
	}		
	public void cmdGridRow(int trackIndex,String file){
		this.mBtManager.sendString("gridrow "+trackIndex+","+file+"");
	}			
	public void cmdGridCell(int trackIndex,int tickIndex,boolean tickState){
		this.mBtManager.sendString("gridcell "+trackIndex+","+tickIndex+","+(tickState?"1":"0")+"");
	}			
	
	
}
