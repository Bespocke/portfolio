let rec insere x u =
	match u with
		[] -> [x]
		|a::q when x>a -> a::(insere x q)
		|_ -> x::u;;
		
let rec tri_insertion l =
	match l with
		[] -> []
		|a::q -> insere a (tri_insertion q);;

type arbre = Vide | Noeud of int *arbre * arbre;;
		
let min_tas t =
	match t with
		Vide -> failwith "minimum d'un tas vide"
		|Noeud(x,g,d) -> x;;
	
let min_quasi t = 
	match t with
		Vide -> failwith "minimum d'un quasi-tas vide"
		|Noeud(x,Vide,Vide) ->  x
  		|Noeud(x,g,d) -> min x (min (min_tas g) (min_tas d));;
  		
let rec percole a =
	match a with
		Vide -> a
		|Noeud(x,_,_) when x = min_quasi a -> a
		|Noeud(x,Noeud(x1,g1,d1),Noeud(x2,g2,d2)) ->
				if x1 = min_quasi a then
					let g = percole (Noeud(x,g1,d1)) in
					let d =  Noeud(x2,g2,d2) in
					Noeud(x1,g,d)
				else  let g = Noeud(x1,g1,d1) in
						let d = percole (Noeud(x,g2,d2)) in
						Noeud(x2,g,d);;
						
let rec decomp_parf n =
	match n with
		0 -> []
		|_ -> match decomp_parf (n-1) with
					mk1::mk2::q when mk1 = mk2 -> (2*mk1 + 1)::q
					|l -> 1::l;;
					
let ajoute x h = 
	match h with
		(a1,t1)::(a2,t2)::q when t1=t2 -> (percole (Noeud(x,a1,a2)),2*t1 +1)::q
		|_ -> (Noeud(x,Vide,Vide),1)::h;;
		
let echange_racines a1 a2 =
	match a1,a2 with
		Noeud(x1,g1,d1),Noeud(x2,g2,d2) -> Noeud(x2,g1,d1),Noeud(x1,g2,d2)
		|_ -> failwith"racine non existente";;
		
let rec insere_quasi a t h = 
	match h with
		[] -> [(percole a ,t)]
		|(a1,t1)::q when min_quasi a <= min_tas a1 -> (percole a , t)::h
		|(a1,t1)::q -> let b,b1 = echange_racines a a1 in 
								(b,t)::(insere_quasi b1 t1 q);;
								
let rec tri_racines h = 
	match h with
		[] -> []
		|(a1,t1)::q ->  insere_quasi a1 t1 (tri_racines q);; 

let rec constr_liste_tas l = match l with
	| [] -> []
		| x::r -> ajoute x (constr_liste_tas r) ;;
		
let rec extraire h =
	match h with
		[] -> []
		|(Noeud(x,Vide,Vide),t)::h' -> x::(extraire h')
		|(Noeud(x,a1,a2),t)::h' -> 
									let h'' = insere_quasi a1 (t/2) (insere_quasi a2 (t/2) h') in
									x::(extraire h'')
		|_ -> failwith "bug dans extraire";;
		
let tri_lisse l =
   extraire (tri_racines (constr_liste_tas l));;
   
type tasbin = {donnees : int array ; pos : int ; taille : int} ;;

let fg t =
	{donnees = t.donnees ; pos = t.pos+1 ; taille = t.taille/2};;
	
let fd t =
	let k = t.taille/2 in
	{donnees = t.donnees ; pos = t.pos+1+k ; taille = k};;
	
let min_tas_array t =
	t.donnees.(t.pos);;
									
let min_quasi_array t =
    if t.taille=1 then t.donnees.(t.pos)
    else min t.donnees.(t.pos) (min t.donnees.(t.pos+1) t.donnees.((fd t).pos));;

		
		
		
let rec percole_array t =
	if t.taille > 1 then
		let m = min_quasi_array t in
		let r = t.donnees.(t.pos) in
		match m with
			x when x = min_tas_array (fg t) ->
												t.donnees.(t.pos) <- m;
												t.donnees.(t.pos + 1) <- r;
												percole_array (fg t); 
			|x when x = min_tas_array (fd t) ->
												t.donnees.(t.pos) <- m;
												t.donnees.((fd t).pos) <- r;
												percole_array (fd t); 
			|_ -> ();;


		
let ajoute_array d p h = 
	match h with
		a1::a2::q when a1.taille=a2.taille -> let a = {donnees = d; pos = p ; taille = a1.taille * 2 + 1} in
															percole_array a;
															a::q
		|_ -> let a = {donnees = d; pos = p ; taille = 1} in a::h;;

let rec constr_liste_tas_aux d p h =
	if p = 0 then h
	else let hi = ajoute_array d (p-1) h in constr_liste_tas_aux d (p-1) hi ;;


let constr_liste_tas_array d = constr_liste_tas_aux d (Array.length d) [] ;;

let echange_racines_array a1 a2 =
	let d = a1.donnees in
	let x = d.(a1.pos) in
	d.(a1.pos) <- d.(a2.pos);
	d.(a2.pos) <- x;;

let rec insere_quasi_array a h = 
	match h with
		[] -> percole_array a; [a]
		|a1::q when min_quasi_array a <= min_tas_array a1 -> percole_array a;a::h
		|a1::q -> echange_racines_array a a1;
						a::(insere_quasi_array a1 q);;
						

let rec tri_racines_array h = 
	match h with
		[] -> []
		|a1::q ->  insere_quasi_array a1 (tri_racines_array q);; 
		

let rec extraire_array h =
	match h with
		[] -> ()
		|a::h' when a.taille = 1 -> extraire_array h'
		|a::h' -> let h'' = insere_quasi_array (fg a) (insere_quasi_array (fd a) h') in
						extraire_array h'';;
						
let tri_lisse_array l =
   extraire_array (tri_racines_array (constr_liste_tas_array l));;
   
