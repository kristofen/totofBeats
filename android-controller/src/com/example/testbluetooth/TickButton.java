package com.example.testbluetooth;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.BlurMaskFilter;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.View;
import android.widget.Button;

public class TickButton extends Button {

	public int trackIndex=-1;
	public int tickIndex=-1;
	
	public TickButton(Context context) {
		super(context);
		// TODO Auto-generated constructor stub
		init();
	}
	
	private boolean pIsOn=false;
	public boolean getIsOn() {
		return pIsOn;
	}
	public void setIsOn(boolean value) {
	   pIsOn = value;
	   refreshColor();
	   invalidate();
	   requestLayout();
	}
		
	public TickButton(Context context,AttributeSet attrs){
		super(context,attrs);
		 TypedArray a = context.getTheme().obtainStyledAttributes(
			        attrs,
			        R.styleable.TickButton,
			        0, 0);
		 try {
			 this.pIsOn = a.getBoolean(R.styleable.TickButton_isOn, false); 
		 } finally {
			 a.recycle();
		 }
		 init();

	}

	private Paint backPaint=null;
	
	private void init(){
		this.backPaint = new Paint(0);
		refreshColor();
	}
	
	private void refreshColor(){
		if (this.pIsOn==true){
			this.backPaint.setColor(0xff00ff00);
		} else {
			this.backPaint.setColor(0xffff0000);
		}
	}
	
	
	private int pW=0;
	private int pH=0;
	private RectF bounds=null;
	
	@Override
	protected void onSizeChanged (int w, int h, int oldw, int oldh) {
		super.onSizeChanged(w, h, oldw, oldh);
		
		this.pW=w;
		this.pH=h;
		
		this.maxW = Math.max(this.maxW, this.pW);
		this.maxH = Math.max(this.maxH, this.pH);
		this.minW = Math.min(this.minW, this.pW);
		this.minH = Math.min(this.minH, this.pH);
		
		this.bounds=new RectF(2,2,this.pW-4,this.pH-4);
	}
	private int minW;
	private int maxW;
	private int minH;
	private int maxH;	
	protected void onDraw(Canvas canvas){
		//super.onDraw(canvas);
		if (this.bounds!=null && this.backPaint!=null){
			canvas.drawRect(this.bounds, backPaint);	
		}
	}
	public void toggle() {
		// TODO Auto-generated method stub
		this.pIsOn = ! this.pIsOn; 
		refreshColor();
		invalidate();
		requestLayout();
	}
	
	
}
