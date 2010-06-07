/**
    Copyright (C) 2010 Mattia Monga

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
**/

function init(){
    for (var i=0; i<2 ; i++){
	input_floats(1, " Latitudine" + (i+1));
	input_floats(1, " Longitudine" + (i+1));
    }
}




function main(input) {
    output(pyth1(input[0], input[1], input[2], input[3]).toFixed(), 
	   "d = R*sqrt(deltaLat^2 + deltaLong^2) (in radianti): ");
    output(pyth2(input[0], input[1], input[2], input[3]).toFixed(), 
	   "d = R*sqrt(deltaLat^2 + cos(latMedia)*deltaLong^2) (in radianti): ");
    output(gcircle(input[0], input[1], input[2], input[3]).toFixed(), "Greater circle:  ");
}

const R = 6371009;
const torad = Math.PI/180;
const a = 6378137;
const b = 6356752;

function Rphi(phi){
    phi *= torad;
    return Math.sqrt((Math.pow(a*a*Math.cos(phi),2)
		      +Math.pow(b*b*Math.sin(phi),2))
		     /(Math.pow(a*Math.cos(phi),2)
		       +Math.pow(b*Math.sin(phi),2)));

}


function pyth1(phiA, lambdaA, phiB, lambdaB){
    var deltaPhi = (phiB - phiA)*torad;
    var deltaLambda = (lambdaB - lambdaA)*torad;

    return Rphi((phiB+phiA)/2)
	*Math.sqrt(deltaPhi*deltaPhi + deltaLambda*deltaLambda);
}    

function pyth2(phiA, lambdaA, phiB, lambdaB){
    var cosMeanPhi = Math.cos((phiA + phiB)*torad/2);
    return pyth1(phiA, cosMeanPhi*lambdaA, phiB, cosMeanPhi*lambdaB);
}

function gcircle(phiA, lambdaA, phiB, lambdaB){
    return Rphi((phiB+phiA)/2)
	*Math.acos(Math.sin(phiA*torad)*Math.sin(phiB*torad) 
		   + Math.cos(phiA*torad)*Math.cos(phiB*torad)
		   *Math.cos((lambdaB-lambdaA)*torad));
}
