type arbre = N of arbre list * bool
| F of bool;;

let rec backtracking a =
(* prend un arbre de config et teste s'il contient une feuille avec True *)
	match a with
		|F b -> b
		|N(l, b) -> 
			if not b then false
			else begin
				let rec aux l =
					match l with
						|[] -> false
						|f::q -> (backtracking f) || (aux q)
				in
				aux l	
			end;;
			
let a = N([N([F false; F false; F false ], false); N([F true; F false], true); N([F false; F true], true)], true);;


backtracking a;;



let nb a = 
	let c = ref 0 in
	let rec backtracking2 a =
	(* prend un arbre de config et teste s'il contient une feuille avec True *)
		match a with
			|F true -> incr c
			|F false -> ()
			|N(l, b) -> 
				if not b then ()
				else begin
					let rec aux l =
						match l with
							|[] -> ()
							|f::q -> (backtracking2 f) ; (aux q)
					in
					aux l	
				end
	in
	backtracking2 a;
	!c;;
	
nb a;;

let rec backtracking2 a =
(* prend un arbre de config et teste s'il contient une feuille avec True *)
	match a with
		|F b -> if b then 1 else 0
		|N(l, b) -> 
			if not b then 0
			else begin
				let rec aux l =
					match l with
						|[] -> 0
						|f::q -> (backtracking2 f) + (aux q)
				in
				aux l	
			end;;
			
backtracking2 a;;

let rec contraintes_verifiees config x1 dec = 
		match config with
			[] -> true
			|x2::q -> (x1 <> x2) 
						&& ((x1 + dec) <> x2) 
						&& ((x1 - dec) <> x2) 
						&& contraintes_verifiees q x1 (dec +1);;

let n_dames n =
	let res = ref [] in
	let c = ref 0 in
	let rec aux config len =
		if len = n
		then res := config :: !res
		else begin
		for x = 0 to (n-1) do
			incr c;
			if contraintes_verifiees config x 1
			then aux (x::config) (len+1) 
		done
		end
	in
	aux [] 0;
	!res;;
	
List.length (n_dames 8);;


	
	
	