let sound;
let imageCanary;
let analyzer;
let nvalue = 3000;
let cutnum = 60;
let vecLocation = [];
let baseLocation = [];
let vecVelocity = [];
let colorr = [];
let colorg = [];
let colorb = [];
let speed = [];
let speedne = [];
let size = [];
let spsize =[];
let speedSlider;
let lightIndex = 0;
let offsetY = 0;
let runCount = 0;

function preload(){
	sound = loadSound('./sound.mp3');
	imageCanary = loadImage('./polkadot.png');
}

function setup() {
	sound.loop();
	analyzer = new p5.Amplitude();
	analyzer.setInput(sound);
	createCanvas(1000, 1000);
	speedSlider = createSlider(0, 100, 50);
	speedSlider.position(25, 25);
	button = createButton('reset');
	button.position(30,60);
	button.mousePressed(reset);
	fft = new p5.FFT();
	frameRate(15);
	for (let i = 0; i < nvalue; i++) {
    vecLocation[i] = createVector(random(-10,width+10), i%cutnum*height/(cutnum-1));
		baseLocation[i] = createVector(random(-10,width+10), i%cutnum*height/(cutnum-1));
    vecVelocity[i] = createVector(0, 0);
		colorr[i] = 253;
    colorg[i] = 63;
    colorb[i] = 185;
		size[i] = 10;
  }
	//loadPixes();
	//img.resize(pw, ph);
  // Only need to load the pixels[] array once, because we're only
  // manipulating pixels[] inside draw(), not drawing shapes.
  loadPixels();
  // We must also call loadPixels() on the PImage since we are going to read its pixels.
  imageCanary.loadPixels();
	//imageCanaryr = loadImage('./canary500r.png');
}

function draw() {
	background(255, 255, 0);
	noStroke();
	let speedslide = 50 / 100;
	let spectrum = fft.analyze();
	let len = spectrum.length-150;
	for (let i = 0; i < nvalue; i++){
			fill(colorr[i], colorg[i], colorb[i], 180);
			vecVelocity[i].x = speed[i%(cutnum)]*speedslide-(speedne[cutnum-(i%(cutnum))-1]*(1-speedslide));
		if(pow(vecLocation[i].x -(width/2),2)+pow(vecLocation[i].y -(height/2),2)<=76500){
			vecLocation[i].add(vecVelocity[i]);
			if(baseLocation[i].y-(height/2) > 0){
				vecLocation[i].y = height- baseLocation[i].y ;
				ellipse(vecLocation[i].x, (height/2)+ sqrt(76500-pow(vecLocation[i].x-(width/2),2)), size[i], size[i]);
				ellipse(vecLocation[i].x, (height/2)- sqrt(76500-pow(vecLocation[i].x-(width/2),2)), size[i], size[i]);
			}else{
				vecLocation[i].y = height- baseLocation[i].y ;
				ellipse(vecLocation[i].x, (height/2)+ sqrt(76500-pow(vecLocation[i].x-(width/2),2)), size[i], size[i]);
				ellipse(vecLocation[i].x, (height/2)- sqrt(76500-pow(vecLocation[i].x-(width/2),2)), size[i], size[i]);
			}
		}
		else{
			vecLocation[i].add(vecVelocity[i]);
			ellipse(vecLocation[i].x, vecLocation[i].y, size[i], size[i]);
			if(vecLocation[i].y != baseLocation[i].y ){
					if(pow(vecLocation[i].x -(width*2/3),2)+pow(baseLocation[i].y -(height/5),2)>=10000){
						if(pow(vecLocation[i].x -(width/3),2)+pow(baseLocation[i].y -(height*4/5),2)>=10000){
							ellipse(vecLocation[i].x, baseLocation[i].y, size[i], size[i]);   
						}
					}
			}
		} 
		if (vecLocation[i].x <  - 10 || vecLocation[i].y > height + 10) {
			vecLocation[i].x = width;
			vecLocation[i].y = baseLocation[i].y;
			vecVelocity[i].y = 0;
			size[i] = map(spsize[i%(cutnum)], 50, 255, 3, 50);
			//colorr[i] = random(0, 127);
    	//colorg[i] = map(spsize[i%(cutnum)], 50, 255, 127, 255);
    	//colorb[i] = map(spsize[i%(cutnum)], 50, 225, 127, 255);
			colorr[i] = map(spsize[i%(cutnum)], 50, 225, 127, 255);
    	colorg[i] = random(0, 127);
    	colorb[i] = map(spsize[i%(cutnum)], 50, 225, 127, 255);
		}
		if (vecLocation[i].x > width + 10 || vecLocation[i].y < -10) {
			vecLocation[i].x = 0;
			vecLocation[i].y = baseLocation[i].y;
			vecVelocity[i].y = 0;
			size[i] = map(spsize[cutnum-(i%(cutnum))-1], 50, 255, 3, 50);
			colorr[i] = map(spsize[cutnum-(i%(cutnum))-1], 50, 255, 127, 255);
			//colorr[i] = random(0, 127);
    	colorg[i] = random(0, 127);
			//colorg[i] = map(spsize[cutnum-(i%(cutnum))-1], 50, 255, 127, 255);
    	colorb[i] = map(spsize[cutnum-(i%(cutnum))-1], 50, 255, 127, 255);
		}
	}
	
	//tint(255, 0);
	
	//drawLightImage(imageCanary, width/2-300, height/2-300, 500, 500,510);
	image(imageCanary, width/2-155, height/2-200+offsetY, imageCanary.width, imageCanary.height);
	if(runCount > 300)
		drawLight(imageCanary, width/2-155, height/2-200+offsetY, imageCanary.width, imageCanary.height, lightIndex);
	//image(imageCanaryr, width*3/4-150, height/5-150, 300, 300);
	
  //drawwave();
	stroke(255);
	fill(50,255);
	let n = 0;
	beginShape();
	//curveVertex(width+10,0);
	//curveVertex(width+10,0);
  for (let i = 0; i < len; i+=floor((len/(cutnum-1)))){
    let y = map(i, 0, floor((len/(cutnum-1)))*(cutnum-1), 0, height);
    let x = map(spectrum[i], 0, 255, width, width-(width*speedslide)*0.9);
		speed[n] = map(spectrum[i], 0, 255, 0, -45);
		spsize[n] = spectrum[i];
    //curveVertex(x,y);
		n = n + 1;
  }
	//curveVertex(width+10,height);
	//curveVertex(width+10,height);
  endShape();
	n = 0;
	beginShape();
	//curveVertex(-10,height);
	//curveVertex(-10,height);
  for (let i = 0; i < len; i+=floor((len/(cutnum-1)))){
    let y = map(i, 0, floor((len/(cutnum-1)))*(cutnum-1), height, 0);
    let x = map(spectrum[i], 0, 255, 0, width*(1-speedslide)*0.9);
		speedne[n] = map(spectrum[i], 0, 255, 0, -45);
    //curveVertex(x,y);
		n = n + 1;
  }
	//curveVertex(-10,0);
	//curveVertex(-10,0);
  endShape();
	if(lightIndex > 13) {
		lightIndex = 0;
		//noLoop();
	} else {
		lightIndex += 1;
	}
	if(offsetY = 0) {
		offsetY = 5;
	} else {
		offsetY = 0;
	}
	if(runCount < 999999) runCount += 1;
}

function drawLightImage(img, px, py, pw, ph, li) {
	var lightLines = 30;
	var checkY = 30*li;
	img.resize(pw, ph);
  // Only need to load the pixels[] array once, because we're only
  // manipulating pixels[] inside draw(), not drawing shapes.
  loadPixels();
  // We must also call loadPixels() on the PImage since we are going to read its pixels.
  img.loadPixels();
  for (let x = 0; x < img.width; x++) {
    for (let y = 0; y < img.height; y++ ) {
			if(y > checkY - 15 && y < checkY + 15) {
				//let loc = (x + y * img.width) * 4;
				// Get the R,G,B values from image
				//let r, g, b;
				//r = img.pixels[loc];
				let c = img.get(x,y);
				drawString(100, 100, "brightness lines:" + checkY);
				if(c[3] > 127 && c[0] > 230) {
					c[0] += 150;
					if(c[0] > 255) c[0]=255;
					c[1] += 150;
					if(c[1] > 255) c[0]=255;
					c[2] += 150;
					if(c[2] > 255) c[0]=255;
				}
				let loc = (x + y * img.width) * 4
				img.pixels[loc] = c[0];
				img.pixels[loc+1] = c[1];
				img.pixels[loc+2] = c[2];
				img.pixels[loc+3] = c[3];
			}
    }
  }
  updatePixels();
	image(img, px, py, pw, ph);
}

function drawLight(img, px, py, pw, ph, li) {
	var lightLines = 30;
	var checkY = 30*li;
	//img.resize(pw, ph);
  // Only need to load the pixels[] array once, because we're only
  // manipulating pixels[] inside draw(), not drawing shapes.
  //loadPixels();
  // We must also call loadPixels() on the PImage since we are going to read its pixels.
  //img.loadPixels();
  for (let x = 0; x < img.width; x++) {
    for (let y = 0; y < img.height; y++ ) {
			if(y > checkY - 15 && y < checkY + 15) {
				//let loc = (x + y * img.width) * 4;
				// Get the R,G,B values from image
				//let r, g, b;
				//r = img.pixels[loc];
				let c = img.get(x,y);
				//drawString(100, 100, "brightness lines:" + checkY);
				//print("brightness lines:" + checkY);
				if(c[3] > 127 && c[0] >= 220) {
					c[0] += 150;
					if(c[0] > 255) c[0]=255;
					c[1] += 100;
					if(c[1] > 255) c[1]=255;
					c[2] += 100;
					if(c[2] > 255) c[2]=255;
					c[3] = 180;
					noStroke();
					fill(c);
					rect(px + x, py+y, 1,1);
				}
				else if(c[3] > 127 && c[0] < 220) {
					c[0] = 250;
					c[1] = 204;
					c[2] = 51;
					c[3] = 180;
					noStroke();
					fill(c);
					rect(px + x, py+y, 1,1);
				}
				else {
					//c[0] = 0;
					//c[1] = 255;
					//c[2] = 0;
					//c[3] = 255;
					;
				}
				//noStroke();
				//fill(c);
				//rect(px + x, py+y, 2,2);
			}
    }
  }
  //updatePixels();
	//image(img, px, py, pw, ph);
}

function drawLight2(img, px, py, pw, ph, lightIndex) {
	var lightLines = 30;
	var checkY = 30*lightIndex;
	noStroke();
	fill(255);
	rect(width/2, height/2, 100,100);
}


function drawString(x, y, showStr) {
  // The text() function needs three parameters:
  // the text to draw, the horizontal position,
  // and the vertical position
	stroke(175);
  fill(255);
	textSize(20);
	textStyle(BOLD);
	textAlign(CENTER);
	text(showStr, x, y);
	//text("this text is centered.",width/2,60);
}

function reset(){
		for (let i = 0; i < nvalue; i++) {
		colorr[i] = 255;
    colorg[i] = 255;
    colorb[i] = 255;
		size[i] = 3;
  }
}


