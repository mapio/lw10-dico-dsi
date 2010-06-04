function distanza(){
    var form = document.forms['coordinate'];

    form['ris-pyth1'].value = pyth1(parseFloat(form['latA'].value),
				    parseFloat(form['longA'].value),
				    parseFloat(form['latB'].value),
				    parseFloat(form['longB'].value)).toFixed();

    form['ris-pyth2'].value = pyth2(parseFloat(form['latA'].value),
				    parseFloat(form['longA'].value),
				    parseFloat(form['latB'].value),
				    parseFloat(form['longB'].value)).toFixed();


    form['ris-gcircle'].value = gcircle(parseFloat(form['latA'].value),
				    parseFloat(form['longA'].value),
				    parseFloat(form['latB'].value),
				    parseFloat(form['longB'].value)).toFixed();


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
