package com.example.testbluetooth;

import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class TickButtonClick implements OnClickListener {

	public void onClick(View v) {
		// TODO Auto-generated method stub
		TickButtonTemp btn = (TickButtonTemp) v;
		MainActivity context = (MainActivity)btn.getContext();
		CommandProcessor cmd = context.getCmdProcessor();
		Log.w("testBluetooth","Tick Click track="+btn.trackIndex+", tick="+btn.tickIndex);
		btn.isOn = ! btn.isOn;
		if (cmd!=null){
			cmd.cmdGridCell(btn.trackIndex, btn.tickIndex, btn.isOn);
		}
	}

}
