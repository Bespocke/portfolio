let indice_gauche i = 2*i +1;;

let indice_droit i = 2*i + 2;;

let indice_pere i = (i-1)/2;;

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

max_float;;

let dijkstra g s =
	let n = Array.length g in
	let d = Array.make n max_float in
	d.(s) <- 0.;
	let f = creer_file_prio n in
	for u = 0 to (n-1) do enfiler f (-.d.(u)) u done;
	let p = Array.make n 0 in
	for u = 0 to (n-1) do p.(u) <- u done;
	while not (est_vide f) do
		let u = defiler f in
		let aux (v, w) =
			(* w est le poids w(u,v) *)
			let d' = d.(u) +. w in
			if d' < d.(v) then begin
				d.(v) <- d';
				p.(v) <- u;
				modifier_prio f (-.d') v
			end
		in
		List.iter aux g.(u)
	done; 
	p, d;;
	
let g = [| [(1, 10.); (2, 3.); (3, 5.)]; [(2, -.11.)]; [(3, 2.)]; []|];;


dijkstra g 0;;	
