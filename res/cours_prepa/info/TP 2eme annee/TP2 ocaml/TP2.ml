(* tri rapide *)

let rec repartition p l =
	match l with
		[] -> [],[]
		|x::q -> let l1,l2 = repartition p q in
					if x<p then x::l1,l2
					else l1,x::l2;;

let rec tri_rapide l =
	match l with
		[] | [_] -> l
		|p::q -> let l1,l2 = repartition p q in
					(tri_rapide l1) @ p :: (tri_rapide l2);;

(*tri fusion *)

let rec scission l = 
	match l with
		[] -> [],[]
		|[a] -> [a],[]
		|a::b::q -> let l1,l2 = scission q in a::l1,b::l2;;
		
let rec fusion l1 l2 =
	match l1,l2 with
		[],l2 -> l2
		|l1,[] -> l1
		|a::q1, b::q2 -> if a < b then a::(fusion q1 l2) else b::(fusion l1 q2);; 
		
let rec tri_fusion l =
	match l with
		[] | [_] -> l
		|_ -> let l1,l2 = scission l in fusion (tri_fusion l1) (tri_fusion l2);;
		



let rec find rep u = 
	let p = rep.(u) in
	if p = u then p else find rep p;;
	
(* version optimisée du find *)
	
let rec find rep u = 
	let p = rep.(u) in
	if p = u then p else begin
		let r = find rep p in
		rep.(u) <- r;
		r
		end;;	

let union rep u v = rep.(find rep u) <- (find rep v);;

let kruskal g =
	let n = Array.length g in
	let liste_aretes = ref [] in
	let rec aretes u l =
		match l with
			[] -> []
			|(v,w)::q -> if u<v then (w,u,v)::(aretes u q) else aretes u q
	in
	for u = 0 to (n-1) do
		liste_aretes := (aretes u g.(u)) @ !liste_aretes
	done;
	liste_aretes := tri_rapide !liste_aretes;
	let acm = ref [] in
	let rep = Array.make n 0 in
	for u = 0 to (n-1) do
		rep.(u) <- u
	done;
	let traiter_arete (w,u,v) = 
		if (find rep u) <> (find rep v)
		then begin
			acm := (u,v,w)::!acm;
			union rep u v
		end
	in
	List.iter 	traiter_arete !liste_aretes;
	!acm;;
	

let g = [|  [(1,1.) ; (2,0.) ; (4,5.)] ; 
[(0,1.) ; (2,2.) ; (3,3.) ; (4,6.)]  ; 
[(0,0.) ; (1,2.) ; (3,10.)] ; 
[(2,10.) ; (1,3.) ; (4,0.)] ; 
[(3,0.) ; (1,6.) ; (0,5.)] |];;

kruskal g;;



(* Files de priorité *)

let gauche i = 2*i + 1;;

let droit i = 2*i + 2;;

let pere i = (i-1)/2;;


type file_prio = {mutable taille : int ; tas : ((int*float)*int) array ; position : int array};; 

let creer_file c = {taille = 0 ; tas = Array.make c ((-1,-1.),-1) ; position = Array.make c c};;


let cle f i = fst f.tas.(i);;

let valeur f i = snd f.tas.(i);;

let echange f i j = 
	f.position.(valeur f i) <- j;
	f.position.(valeur f j) <- i;
	let temp = f.tas.(i) in
	f.tas.(i) <- f.tas.(j);
	f.tas.(j) <- temp;;


let rec entasser f i =
	let g = gauche i in
	let d = droit i in
	let m =
		match g<f.taille , d<f.taille with
			false,_ -> i
			|true, false when cle f i > cle f g -> g
			|true, false -> i
			|_ -> 	let ci = cle f i in
						let cg = cle f g in
						let cd = cle f d in
						match min ci (min cg cd) with
							x when x = ci -> i
							|x when x = cg -> g
							|_ -> d
	in
	if i!=m then begin echange f i m; entasser f m end;;
	
let rec remonter f i =
	if i!=0 && cle f (pere i)>cle f i then begin echange f i (pere i); remonter f (pere i) end;;
 						
let est_vide f = f.taille = 0;;	

let defiler f = 
	let resultat = f.tas.(0) in
	echange f 0 (f.taille - 1);
	f.taille <- f.taille - 1;
	entasser f 0;
	snd resultat;;



let ajouter_valeur f c v = 
	if f.taille = Array.length f.tas then failwith "file complète";
	f.taille<-f.taille + 1;
	f.tas.(f.taille - 1)<-(c,v);
	f.position.(v)<-f.taille - 1;
	remonter f (f.taille-1);;
	


let modifier_prio f c v =
	let i = f.position.(v) in
	if i>=f.taille then () else
	begin
	let c' = cle f i in
	f.tas.(i) <- (c,v);
	if c'<c then entasser f i else remonter f i
	end;;


(* Dijkstra *)

let dijkstra g s =
	let n = Array.length g in
	let distance = Array.make n (1,0.) in
	distance.(s) <- (0,0.);
	let f = creer_file n in
	for u = 0 to (n-1) do
		ajouter_valeur f distance.(u) u;
		done;
	let p = Array.make n (-1) in
	p.(s) <- s;
	while not (est_vide f) do
		let u = defiler f in
		let rec traitement (v,w) =
						let d0,d1 = distance.(u) in
						let d' = (d0,d1+.w) in
						if d' < distance.(v) then
							begin
							distance.(v) <- d';
							modifier_prio f d' v;
							p.(v) <- u;
							end;
		in
		List.iter traitement g.(u);
		done;
	distance,p;;


let g = [| [(1,10.);(4,5.)] ; 
				[(2,1.);(4,2.)] ; 
				[(3,4.)] ; 
				[(2,6.);(0,7.)];
				[(1,3.);(2,9.);(3,2.)] |];;		
				
let d,p = dijkstra g 0;;	


let chemin p u =
	let rec aux u =
		if p.(u) = u then [u] else u::(aux p.(u))
	in
	List.rev (aux u);; 
	
chemin p 2;;

(* Bellman-Ford *)


let bellman_ford g s =
	let n = Array.length g in 
	let d = Array.make n (1,0.) in
	let p = Array.make n 0 in
	d.(s) <- (0,0.);
	for k = 1 to (n-1) do
		for u = 0 to (n-1) do
			let traitement (v,w) =
				let i,f = d.(u) in
				let d' = (i,f+.w) in
				if d' < d.(v) then begin
					d.(v) <- d';
					p.(v) <- u
					end
			in
			List.iter traitement g.(u)						
		done
	done;
	(* détection de cycles de poids négatif *)
	for u = 0 to (n-1) do
		let traitement (v,w) =
			let i,f = d.(u) in
			let d' = (i,f+.w) in
			if d' < d.(v) then 
				failwith "le graphe contient un cycle de poids négatif"
		in
		List.iter traitement g.(u)						
	done;
	(d,p);;
			
let g = [| [(1,1.);(2,2.);(3,3.)] ; [] ; [(1,-10.)] ; [(2,-10.)] |];;


bellman_ford g 0;;




(* Floyd-Warshall *)	

let mat_adj g = 
	let n = Array.length g in
	let m = Array.make_matrix n n (1,0.) in
	for u = 0 to (n-1) do
		let traitement (v,p) =
			m.(u).(v) <- (0,p)
		in
		List.iter traitement g.(u)
	done;
	m;;

let floyd_warshall g =
	let n = Array.length g in
	let m = mat_adj g in
	for k = 1 to n do
		for u = 0 to (n-1) do
			for v = 0 to (n-1) do
				let a1,b1 = m.(u).(k-1) in
				let a2,b2 = m.(k-1).(v) in
				let d' = (a1 + a2 , b1 +. b2) in
				m.(u).(v) <- min d' m.(u).(v)
			done
		done
	done;
	m;;


floyd_warshall g;;	

let (++) x y = let a,b = x in let c,d = y in let m = max a c in m, if m=0 then (b+.d) else 0.;;

let h u c = (0,0.);;


let a_star g h s c =
	let n = Array.length g in
	let distance = Array.make n (1,0.) in
	distance.(s) <- (0,0.);
	let marque = Array.make n false in
	marque.(s) <- true;
	let f = creer_file n in
	ajouter_valeur f (h s c) s;
	let p = Array.make n (-1) in
	p.(s) <- s;
	let rec aux () =
		if est_vide f 
		then failwith "le sommet cible n'a pas été atteint"
		else let u = defiler f in
		if u = c 
		then distance.(u), chemin p u
		else begin
			let du = distance.(u) in
			marque.(u) <- false;
			let rec traitement (v,w) =
				let d' = du ++ (0,w) in
				if d' < distance.(v)
				then begin
					distance.(v) <- d';
					p.(v) <- u;
					let prio_v = d' ++ h v c in
					if marque.(v) then modifier_prio f prio_v v else ajouter_valeur f prio_v v;
					marque.(v) <- true
				end;
			in
			List.iter traitement g.(u);
			aux ()
		end 
	in
	aux ();;

let pos = [| (0. , 0.) ; (1. , 2.) ; (-3. , -1.) ; (4. , -1.) ; (2. , 2.  )|];;

let h u c = 
	let x1,y1 = pos.(u) in
	let x2,y2 = pos.(c) in
	0, ((x2 -. x1) **2. +.  (y2 -. y1) **2.)**0.5;;
	
let g = [| [(1,10.);(4,5.)] ; 
				[(2,1.);(4,2.)] ; 
				[(3,4.)] ; 
				[(2,6.);(0,7.)];
				[(1,3.);(2,9.);(3,2.)] |];;	
				
a_star g h 0 3;;