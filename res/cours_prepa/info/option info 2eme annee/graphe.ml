let gauche i = 2*i + 1;;

let droit i = 2*i + 2;;

let pere i = (i-1)/2;;



type file_prio = {mutable taille : int ; tas : (int*int) array ; position : int array};; 

let creer_file c = {taille = 0 ; tas = Array.make c (-1,-1) ; position = Array.make c c};;


let cle f i = fst f.tas.(i);;

let valeur f i = snd f.tas.(i);;

let echanger f i j = 
	f.position.(valeur f i) <- j;
	f.position.(valeur f j) <- i;
	let temp = f.tas.(i) in
	f.tas.(i) <- f.tas.(j);
	f.tas.(j) <- temp;;



let max3 a b c = max a (max b c);;


let indice_max t i j k =
	let max3 i j k = max (max i j ) k in
	let m = max3 t.(i) t.(j) t.(k) in
	if m = t.(i) then i
	else if m = t.(j) then j
	else k;;


let rec entasser f i =
	let g = gauche i in
	let d = droit i in
	let n = f.taille in
	if d<n then
		begin
		let k = indice_max t i g d in
		if k!=i then 
			begin
			echanger f i k;
			entasser f k			
			end
		end
	else if d = n && t.(g) > t.(i) then 
		echanger f i g
	;;

let rec remonter f i =
	if i!=0 && cle f (pere i)<cle f i then begin echanger f i (pere i); remonter f (pere i) end;;
 						
let est_vide f = f.taille = 0;;	

let defiler f = 
	let resultat = f.tas.(0) in
	echanger f 0 (f.taille - 1);
	f.taille <- f.taille - 1;
	entasser f 0;
	resultat;;



let ajouter_valeur f c v = 
	if f.taille = Array.length f.tas then failwith "file complète";
	f.taille<-f.taille + 1;
	f.tas.(f.taille - 1)<-(c,v);
	f.position.(v)<-f.taille - 1;
	remonter f (f.taille-1);;
	


let modifier_prio f c v =
	let i = f.position.(v) in
	if i>=f.taille then failwith "valeur non présente";
	let c' = cle f i in
	f.tas.(i) <- (c,v);
	if c'>c then entasser f i else remonter f i;;