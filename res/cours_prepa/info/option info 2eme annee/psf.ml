type exp = 
  Epsilon 
| Lettre of char 
| Plus of (exp * exp) 
| Concat of (exp * exp) 
| Etoile of exp;;

let rec produit l1 l2 = 
	match l1 with
		[] -> []
		|[a] -> 
			let rec aux q =
				match q with
					[] -> []
					|b::r -> (a,b)::(aux r)
			in
			aux l2
		|a::r -> (produit [a] l2)@(produit r l2);;
		
(* Version légèrement optimisée *)
let rec produit l1 l2 =
		match l1 with
		[] -> []
		|a::q -> 
			let rec aux l =
				match l with
					[] -> produit q l2
					|b::r -> (a,b)::aux r
			in
			aux l2;;
		

produit ['a';'b'] ['a'; 'c'; 'd'];;

let rec psf e =
	match e with
		Epsilon -> [], [], [], true
		| Lettre(c) -> [c], [c], [], false
		|Plus(e1, e2) -> 
				let p1, s1, f1, b1 = psf e1 in
				let p2, s2, f2, b2 = psf e2 in
				p1@p2, s1@s2, f1@f2, b1 || b2
		|Concat(e1, e2) ->
				let p1, s1, f1, b1 = psf e1 in
				let p2, s2, f2, b2 = psf e2 in
				let f = f1@f2@(produit s1 p2) in
				let p = (if b1 then p1@p2 else p1) in
				let s = (if b2 then s1@s2 else s2) in
				p, s, f, b1 && b2
		|Etoile(e') ->
				let p', s', f', b' = psf e' in
				p', s', f'@(produit s' p'), true;;
				
		
let e = Concat(Concat( Etoile(Plus( Lettre 'a' , Lettre 'b' )) , Etoile( Lettre('c') )), Lettre('d'))	;;

psf e;;