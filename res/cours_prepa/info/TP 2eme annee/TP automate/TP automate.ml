type ('a , 'b) adc = {
	initial : 'a;
	est_final : 'a -> bool;
	delta : 'a -> 'b -> 'a };;

let ex =
	let d e l = match e,l with
		 0,'a' -> 1
		|0,'b' -> 0
		|1,'a' -> 0
		|1,'b' -> 1
		|_ -> 2
	in
	let f = function
		0 -> true
		|_ -> false
	in
	{initial = 0;
	est_final = f;
	delta = d};;


let aut1 = 
	let d e l =  match e,l with
		 0,'a' -> 2
		|0,'b' -> 1
		|0,'c' -> 3
		|1,'a'|1,'b' -> 2
		|1,'c' -> 3
		|2,'a'|2,'b' -> 2
		|2,'c' -> 3
		|_ -> 4
	in
	let f = function
		1|3 -> true
		|_ -> false
	in
	{
	initial = 0;
	est_final = f;
	delta = d
		};;

let list_of_string s = 
	let n = String.length s in
	let rec aux i =
		match i with
			0 -> []
			|_ -> s.[n-i]::(aux (i-1))
	in
	aux n;;

		
let rec delta_etoile aut q w = 
	match w with
		[] -> q
		|a::r -> delta_etoile aut (aut.delta q a) r;;
		
delta_etoile aut1 0 ['b';'a';'a';'c'];;

let reconnait aut w = aut.est_final (delta_etoile aut aut.initial w);;


let produit a1 a2 = 
   let d (q1, q2) a = (a1.delta q1 a, a2.delta q2 a) in
   let f (q1, q2) = ((a1.est_final q1) && (a2.est_final q2)) in
	{
	initial = (a1.initial, a2.initial);
	est_final = f;
	delta = d
	};;

type ('a , 'b) nda = {
	initiaux : 'a list;
	est_final_nd : 'a -> bool;
	delta_nd : 'a -> 'b -> 'a list };;
	

let rec union l1 l2 =
(* suppose que les listes sont triées *)
	match l1,l2 with
		[],_ -> l2
		|_,[] -> l1
		|a::q,b::r when a<b -> a::(union q l2)
		|a::q,b::r when a=b -> union q l2
		|a::q,b::r  -> b::(union l1 r);;


let rec delta_etoile_nd aut l w =
	match w with
		[] -> l
		|a::r -> let rec aux l2 =
						match l2 with
							[] -> []
							|q::s -> union (aux s) (aut.delta_nd q a)
					in
					delta_etoile_nd aut (aux l) r
		;;

(* variante avec List.fold_left *)

let rec delta_etoile_nd aut l w =
	match w with
		[] -> l
		|a::r -> delta_etoile_nd aut ( List.fold_left  (fun l' q -> union l' (aut.delta_nd q a))  []  l ) r;;


let reconnait_nd aut w = 
	List.exists aut.est_final_nd (delta_etoile_nd aut aut.initiaux w) ;;

let aut2 =
	let d q a = 
		match q,a with
		0,'a' -> [0;1]
		|0,_-> [0]
		|1,'b' -> [2]
		|1,_ -> [6]
		|2,'c' -> [3]
		|2,_ -> [6]
		|3,_ -> [3]
		|4,'a' -> [5]
		|_ -> [6]	
	in 
	let f = function 3|5 -> true |_ -> false in	
	{
	initiaux = [0;4];
	est_final_nd = f;
	delta_nd = d};;
	
reconnait_nd aut2 (list_of_string "b");;



	
let determinise aut_nd = 
	let q0 =  aut_nd.initiaux in
	let f p = List.exists aut_nd.est_final_nd p in	
	let d p a = delta_etoile_nd aut_nd p [a] in
	{
	initial = q0;
	est_final = f;
	delta = d	
	};;
	
let aut3 = determinise aut2;;

reconnait aut3 (list_of_string "b");;


type 'b regexp =
	Epsilon |
	Lettre of 'b |
	Plus of 'b regexp * 'b regexp |
	Concat of 'b regexp * 'b regexp |
	Etoile of 'b regexp ;;



let rec concat l1 l2 =
		match l1 with
		[] -> []
		|a::q -> 
			let rec aux l =
				match l with
					[] -> concat q l2
					|b::r -> (a,b)::aux r
			in
			aux l2;;



let rec psf e = 
	(* renvoie b , P ,S, F , où b est le booléen indiquant si epsilon est reconnu par e *)
	match e with 
		Epsilon ->  true, [] , [] ,[]
		| Lettre(a) -> false , [a] , [a] , []
		|Plus(e1,e2) -> let b1,p1,s1,f1 = psf e1 in 
						let b2,p2,s2,f2 = psf e2 in 
						b1 || b2, union p1 p2, union s1 s2, union f1 f2
		|Concat(e1,e2) -> let b1,p1,s1,f1 = psf e1 in 
						let b2,p2,s2,f2 = psf e2 in 
						(b1 && b2,(if b1 then union p1 p2 else p1),(if b2 then union s1 s2 else s2),union f1 (union f2 (concat s1 p2)))
		|Etoile(e') ->  let b',p',s',f' = psf e' in
					true, p',s',union f' (concat s' p');; 


let marquage e =
	let i = ref 0 in
	let rec aux e = 
		match e with
			Epsilon -> Epsilon
			|Lettre(a) -> incr i ; Lettre((a,!i))
			|Plus(e1,e2) -> Plus(aux e1, aux e2)
			|Concat(e1,e2) -> Concat(aux e1, aux e2)
			|Etoile(e') -> Etoile(aux e')
	in
	aux e;;


let sigma_et = Etoile( Plus(Lettre('a') , Plus(Lettre('b'),Lettre('c'))));;
					
let e = Concat(sigma_et , Concat( Lettre('a') , Concat( Lettre('b') , Concat( Lettre('c') , sigma_et  )   )  )   ) ;;

psf e;;

(* e = S*abcS* *)

let el = marquage e;;

let b,p,s,f = psf el;;



let glushkov e =
	let el = marquage e in
	let b , p,s,f = psf el in
	let q0 = 0 in
	let qf p = if p = q0 then b else List.mem p (List.map (fun (a,b) -> b) s) in
	let liste_p a =
		let rec aux l =
			match l with
				[] -> []
				|(b,i)::r when b = a -> i::(aux r)
				|_::r -> aux r
		in
		List.sort compare (aux p)
	in
	
	let liste_f i a =
		let rec aux l = 
			match l with
				[] -> []
				|((c,k),(d,j))::r when k=i && d=a -> j::(aux r)
				|_::r -> aux r
		in
	List.sort compare (aux f)
	in
	
	let d q a = 	
		if q = q0 then liste_p a 
		else liste_f q a
	in
	let nda = {
	initiaux = [q0];
	est_final_nd = qf;
	delta_nd = d	
	}
	in
	determinise nda;;


let aut4 = glushkov e;;	

reconnait aut4 (list_of_string "bcabbcb");;

delta_etoile aut4 aut4.initial (list_of_string "abcab");;


	



let rec est_prefixe u m =
	match u,m with
		[],_ -> true
		|_,[] -> false
		|a::q,b::r -> a=b && est_prefixe q r;;

	
let bordure u = 
	let rec aux s =
		if est_prefixe s u then s else aux (List.tl s)
	in
	aux (List.tl u);;	
	
bordure ['b';'a';'b';'a';'b'];;

		

let aut_occ m = 
	let d p a = 
		let pa = p@[a] in
		if est_prefixe pa m then pa
		else bordure pa
	in
	let f p = p = m in
	{initial = [];
	est_final = f;
	delta = d}
	;;
	
	
let aut = aut_occ (list_of_string "abcaba");;

	
reconnait aut (list_of_string "hgihofdabcaba");;




(* BONUS : implémentation par table de transition *)

Hashtbl.find;;

type 'a adc2 = {
	tab_alphabet : 'a array;
	hash_alphabet : ('a, int) Hashtbl.t;
	table : int array array;
	finaux : int list
	};;

(* on convient que l'état initial est toujours 0 *)


let ex2 =
	let t = [| [|1;0|] ; [|0;1|] |] in
	let h = Hashtbl.create 2 in
	Hashtbl.add h 'a' 0;
	Hashtbl.add h 'b' 1;
	{
	tab_alphabet = [|'a';'b'|];
	hash_alphabet = h;
	table = t;
	finaux = [0]};;
	
	
Hashtbl.find;;
	
let indice_lettre aut2 a = Hashtbl.find aut2.hash_alphabet a;;
	
let rec delta_etoile2 aut q w =
	match w with
		[] -> q
		|a::r -> delta_etoile2 aut (aut.table.(q).(indice_lettre aut a)) r;;

	
let reconnait2 aut w = List.mem (delta_etoile2 aut 0 w) aut.finaux;;

reconnait2 ex2 (list_of_string "aabbaababa");;

let passage_2_vers_1 aut2 =
	let f q = List.mem q aut2.finaux in
	let d q c = aut2.table.(q).(indice_lettre aut2 c) in
	{initial = 0;
	est_final = f;
	delta = d};;

(* on va utiliser un dictionnaire pour l'autre sens *)

type ('a,'b) arbre = V | N of ('a,'b) arbre * 'b * 'a * ('a,'b) arbre;;

let creer_dictionnaire () = V;;

let rec ajouter_couple a c v = 
	match a with
		V -> N(V,c,v,V)
		|N(g,n,x,d) when c<n -> N(ajouter_couple g c v , n, x, d)
		|N(g,n,x,d) when c>n -> N(g , n , x ,ajouter_couple d c v )
		|_ -> failwith "clé déjà présente";;


let rec est_present a c =
	match a with
		V -> false
		|N(g,n,v,d)  -> if c<n then est_present g c 
							else if c = n then true 
							else est_present d c;;


let rec valeur_associee a c =
	match a with
		V -> failwith "clé non présente"
		|N(g,n,v,d)  -> if c<n then valeur_associee g c 
							else if c = n then v 
							else valeur_associee d c;;


let valeurs_vers_indices tab =
	let n = Array.length tab in
	let h = Hashtbl.create n in
	for i = 0 to n-1 do
		Hashtbl.add h tab.(i) i
	done;
	h;;

	
let passage_1_vers_2 aut1 alph = 
	let dico = ref (creer_dictionnaire ()) in
	let q0 = aut1.initial in
	let numero = ref 0 in
	let n = Array.length alph in
	let rec visiter1 q =	
		dico := ajouter_couple !dico q !numero;
		incr numero;	
		for i = 0 to (n-1) do
			let p = aut1.delta q alph.(i) in
			if not (est_present !dico p)
			then 	visiter1 p
		done;
		in
	visiter1 q0;
	let table2 = Array.make_matrix !numero n 0 in
	let deja_vu = Array.make !numero false in
	let finaux2 = ref [] in
	let rec visiter2 q q' =
		(* q est le nom de l'état dans aut1, q' le nom dans aut2 *)
		deja_vu.(q') <- true;
		if aut1.est_final q then finaux2 := q'::!finaux2;
		for i = 0 to (n-1) do
			let p = aut1.delta q alph.(i) in
			let p' = valeur_associee !dico p in
			table2.(q').(i) <- p';
			if not deja_vu.(p') then visiter2 p p'
		done;
		in
	visiter2 q0 0;
	{
	tab_alphabet = alph;
	hash_alphabet = valeurs_vers_indices alph;
	table = table2;
	finaux = !finaux2};;
	
passage_1_vers_2 aut1 [|'a';'b';'c'|];;


let produit2 aut1 aut2 = 
	let alph = aut1.tab_alphabet in
	passage_1_vers_2 (produit (passage_2_vers_1 aut1) (passage_2_vers_1 aut2)) alph;;
	



let rec insere a l =
	match l with 
		[] -> [a]
		|b::q when a>b -> b::(insere a q)
		|_ -> a::l;;

let transpose aut2 = 
	let t = aut2.table in
	let n_etat = Array.length t in	
	let f p = p = 0 in
	
	let d q a = 
		let rec aux p =
			match p with
				-1 -> []
				|_ when t.(p).(indice_lettre aut2 a) = q -> insere p (aux (p-1))
				|_ -> aux (p-1)
		in
		aux (n_etat -1)
	in	
	{initiaux = List.sort compare aut2.finaux;
	est_final_nd = f;
	delta_nd = d};;

let minimalisation aut2 =
	let alph = aut2.tab_alphabet in
	let aut2' = passage_1_vers_2 (determinise (transpose aut2)) alph in
	passage_1_vers_2 (determinise (transpose aut2')) alph;;
	
let glushkov2 e alph =
	let aut1 = glushkov e in
	minimalisation (passage_1_vers_2 aut1 alph);;

let abc = glushkov2 e [|'a';'b';'c'|];;	

let aut_occ2 m alph =	
	let aut1 = aut_occ m in
	passage_1_vers_2 aut1 alph;;


let lettres_presentes t = 
	let rec insere_sans_doublons a l =
		match l with
			[] -> [a]
			|b::q when b<a-> b::(insere_sans_doublons a q)
			|b::q when b=a -> l
			|_ -> a::l
	in
	let n = String.length t in
	let l = ref [] in
	for i = 0 to (n-1) do
		l := insere_sans_doublons t.[i] !l
	done;
	Array.of_list !l;;


let construire_aut_occ m  =
	let alph = lettres_presentes m in
	aut_occ2 (list_of_string m) alph;;

construire_aut_occ "abcaabc";;


(* Une fois que l'automate des occurrences de m est construit, on peut alors trouver les occurrences du motif m dans n'importe quel texte t en O(|t|) : *)

let occurrences_motif autm t =
	let q = ref 0 in
	let f = List.hd autm.finaux in
	let r = ref [] in
	let n = Array.length autm.table.(0) in
	for i = 0 to (String.length t - 1) do
		let j = indice_lettre autm t.[i] in
		if j = n then q:= 0 
		else 	q := autm.table.(!q).(j);

		if !q = f then r:=i::!r
	done;
	List.rev !r;;	
	
let aut = construire_aut_occ "ana";;

occurrences_motif aut "ananas banane";;

let e2 = Etoile(Plus(Lettre('b'),Concat(Lettre('a'),Concat( Etoile(Lettre('b')),Lettre('a')  ))));;

let aut = glushkov2 e2 [|'a';'b'|];;

(* (b+c)*(a(e + c(b+c)* + b(b(b+c)*+e)))* *)

let bpce = Etoile(Plus(Lettre('b'),Lettre('c')));;


let e3 = Concat( bpce , Etoile( Concat(Lettre('a'), Plus( Epsilon, Plus( Concat( Lettre('c') ,
bpce )   , Concat(Lettre('b'),Plus( Epsilon, Concat( Lettre('b'), bpce  )  )   )    )     )  )  )  )
;;

glushkov2 e3 (lettres_presentes "abc");;

let autab = construire_aut_occ "ab";;

produit2 autab autab;;

let autbb = construire_aut_occ "bb";;

