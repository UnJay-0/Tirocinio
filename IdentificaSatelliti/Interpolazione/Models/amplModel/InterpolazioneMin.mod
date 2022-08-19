#DATI
param nOss;
set indice := 1 .. nOss;
param tempo {indice};
param y {indice};
param minW;
param maxW;
param minA;
param maxA;

#VARIABILI

var a >= minA, <= maxA;
var w >= minW, <= maxW;
var p;
var err {indice};

#VINCOLI

subject to sinusoide {i in indice}:
	 y[i] = a * sin(w * tempo[i] + p) + err[i];

#OBIETTIVO

minimize z: (sum {i in indice} (err[i]^2)) / nOss;  


