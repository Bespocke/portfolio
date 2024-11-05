let indice_gauche i = 2*i +1;;

let indice_droit i = 2*i + 2;;

let indice_pere i = (i-1)/2;;

type arbre = N of arbre * int * arbre | V;;

let tableau_vers_arbre t =
	let l = Array.length t in
	let rec aux i =
		if i >= l then V
		else N(aux (indice_gauche i), t.(i), aux (indice_droit i))
	in
	aux 0;;
	
let a = tableau_vers_arbre [|23; 18; 10; 8; 14; 7; 3; 2|];;

let rec taille a =
	match a with
		V -> 0
		|N(g,c,d) -> 1 + taille g + taille d;;

let arbre_vers_tableau a =
	let l = taille a in
	let t = Array.make l 0 in
	let rec aux a i =
		match a with
			V -> ()
			|N(g, c, d) -> t.(i) <- c; aux g (indice_gauche i); aux d (indice_droit i)
	in
	aux a 0;
	t;;

let t = arbre_vers_tableau a;;

let echanger t i j = 
	let a = t.(i) in
	t.(i) <- t.(j);
	t.(j) <- a;;

let rec remonter t i =
	let p = indice_pere i in
	if i<>0 && t.(p) < t.(i)
	then begin echanger t i p; remonter t p end;;
	
t;;

t.(7) <- 20;;

remonter t 7;;

t;;

let rec entasser t i =
	let l = Array.length t in
	let ig = indice_gauche i in
	let id = indice_droit i in
	if ig >= l (* cas 0 fils *)
	then ()
	else if ig = (l-1) (* cas 1 fils *)
	then (if t.(i) < t.(ig) then echanger t i ig)
	else (* cas 2 fils *)
	if t.(ig) < t.(id) && t.(id) > t.(i)
	then begin echanger t i id; entasser t id end
	else if t.(ig) > t.(i)
	then  begin echanger t i ig; entasser t ig end;;

t;;

t.(0) <- 2;;

entasser t 0;;

t;;


type file_prio = 
	{mutable taille :int;
	tas : (int*int) array};;
	
let file1 = { taille = 4 ; tas = [| (3,1); (2,2); (1,4); (0,0); (2,6); (0,0) ; (2,6); (0,0); (2,6); (0,0)   |] };;

let creer_file_prio c =
	{taille = 0; tas = Array.make c (-1,-1)};;
	
let est_vide f =
	f.taille = 0;;
	
	


let ajouter_valeur f c v = 
	if f.taille = Array.length f.tas
	then failwith "capacité dépassée"
	else begin
	f.tas.(f.taille) <- (c,v); 
	remonter f.tas f.taille;
	f.taille <- f.taille + 1
	end;;
	
let rec entasser_file f i =
	let l = f.taille in
	let ig = indice_gauche i in
	let id = indice_droit i in
	let t = f.tas in
	if ig >= l (* cas 0 fils *)
	then ()
	else if ig = (l-1) (* cas 1 fils *)
	then (if t.(i) < t.(ig) then echanger t i ig)
	else (* cas 2 fils *)
	if t.(ig) < t.(id) && t.(id) > t.(i)
	then begin echanger t i id; entasser_file f id end
	else if t.(ig) > t.(i)
	then  begin echanger t i ig; entasser_file f ig end;;	
	
let defiler f =
	if est_vide f then failwith "defilement de file vide"
	else
	let (c,v) = f.tas.(0) in
	f.tas.(0) <- f.tas.(f.taille - 1);
	f.taille <- f.taille - 1;
	entasser_file f 0;
	v;;
	 
	