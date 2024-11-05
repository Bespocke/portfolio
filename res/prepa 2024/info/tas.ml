let indice_gauche i = 2*i +1;;

let indice_droit i = 2*i + 2;;

let indice_pere i = (i-1)/2;;

(* traductions avec la forme d'arbre *)

type arbre = N of arbre * int * arbre | V;;

let tableau_vers_arbre t =
	let l = Array.length t in
	let rec aux i =
		if i >= l then V
		else N(aux (indice_gauche i), t.(i), aux (indice_droit i))
	in
	aux 0
;;
	
let a = tableau_vers_arbre [|23; 18; 10; 8; 14; 7; 3; 2|];;

let rec taille a =
	match a with
		V -> 0
		|N(g,c,d) -> 1 + taille g + taille d
;;

let arbre_vers_tableau a =
	let l = taille a in
	let t = Array.make l 0 in
	let rec aux a i =
		match a with
			V -> ()
			|N(g, c, d) -> t.(i) <- c; aux g (indice_gauche i); aux d (indice_droit i)
	in
	aux a 0;
	t
;;

let t = arbre_vers_tableau a;;

(* op�rations des tas *)

let echanger t i j = 
	let a = t.(i) in
	t.(i) <- t.(j);
	t.(j) <- a
;;

let rec remonter t i =
	let p = indice_pere i in
	if i<>0 && t.(p) < t.(i) then begin echanger t i p; remonter t p end
;;
	

let rec entasser t i k =
	let ig = indice_gauche i in
	let id = indice_droit i in
	if ig >= k (* cas 0 fils *)
	then ()
	else if ig = (k-1) (* cas 1 fils *)
	then (if t.(i) < t.(ig) then echanger t i ig)
	else (* cas 2 fils *) 
	if t.(ig) < t.(id) && t.(id) > t.(i)
	then begin echanger t i id; entasser t id k end
	else if t.(ig) > t.(i)
	then  begin echanger t i ig; entasser t ig k end
;;


(* Tri par tas *)

let tri_par_tas t =
	let n = Array.length t in
	let taille = ref n in
	for i = 1 to n do entasser t (n-i) !taille done;
	for i = 1 to (n-1) do 
		echanger t 0 (n-i) ;
		decr taille;
		entasser t 0 !taille;
	done
;;


(* Files de priorit� simples *)

type ('a,'b) file_prio = 
	{mutable taille :int;
	tas : ('a*'b) option array}
;;
	

let creer_file_prio c =
	{taille = 0; tas = Array.make c None}
;;
	
let est_vide f =
	f.taille = 0
;;
	
	
let enfiler f c v = 
	if f.taille = Array.length f.tas
	then failwith "capacit� d�pass�e"
	else begin
		f.tas.(f.taille) <- Some (c,v); 
		remonter f.tas f.taille;
		f.taille <- f.taille + 1
	end
;;
	

	
let defiler f =
	if est_vide f then failwith "defilement de file vide" else
	let c,v = Option.get f.tas.(0) in
	f.tas.(0) <- f.tas.(f.taille - 1);
	f.taille <- f.taille - 1;
	entasser f.tas 0 f.taille;
	v
;;


	 
(* Files de priorit� avec changement de priorit� *)

type ('a,'b) file_prio = 
	{mutable taille :int;
	tas : ('a*'b) option array;
	position : ('b,int) Hashtbl.t }
;;
	

let creer_file_prio c =
	{taille = 0; tas = Array.make c None ; position = Hashtbl.create c}
;;
	
let est_vide f =
	f.taille = 0
;;
	
	
let echanger f i j =
   let t = f.tas and h = f.position in 
	let ci, vi = Option.get t.(i) in
	let cj, vj = Option.get t.(j) in
	Hashtbl.replace h vi j;
	Hashtbl.replace h vj i;
	t.(i) <- t.(j);
	t.(j) <- Some(ci, vi)
;;

let rec remonter f i =
	let t = f.tas in 
	let p = indice_pere i in
	if i<>0 && t.(p) < t.(i) then begin echanger f i p; remonter f p end
;;
	

let rec entasser f i =
	let t = f.tas and l = f.taille in
	let ig = indice_gauche i in
	let id = indice_droit i in
	if ig >= l (* cas 0 fils *)
	then ()
	else if ig = (l-1) (* cas 1 fils *)
	then (if t.(i) < t.(ig) then echanger f i ig)
	else (* cas 2 fils *)
	if t.(ig) < t.(id) && t.(id) > t.(i)
	then begin echanger f i id; entasser f id end
	else if t.(ig) > t.(i)
	then  begin echanger f i ig; entasser f ig end
;;
	
	
let enfiler f c v = 
	if f.taille = Array.length f.tas
	then failwith "capacit� d�pass�e"
	else begin
		f.tas.(f.taille) <- Some (c,v); 
		Hashtbl.add f.position v f.taille;
		remonter f f.taille;
		f.taille <- f.taille + 1;
	end
;;
	

	
let defiler f =
	if est_vide f then failwith "defilement de file vide" else
	let c,v = Option.get f.tas.(0) in
	f.tas.(0) <- f.tas.(f.taille - 1);
	f.taille <- f.taille - 1;
	entasser f 0;
	v
;;
	

let modifier_prio f c v =
	let i = Hashtbl.find f.position v in
	let c' = fst (Option.get f.tas.(i)) in
	f.tas.(i) <- Some (c,v);
	if c'>c then entasser f i else remonter f i
;;

￼