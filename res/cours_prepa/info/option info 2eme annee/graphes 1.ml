let creer_file() =
  let f1 = ref [] in
  let f2 = ref [] in
  (f1,f2);;

let est_vide f = 
  let l1,l2 = f in
  (!l1,!l2) = ([],[]);;
  

let file = creer_file();;
est_vide file;;

let enfiler file elem = let l1,l2 = file in
  l2 := elem::!l2;;
  

let rev_list l =
  let rec rev_acc acc = function
    | [] -> acc
    | hd::tl -> rev_acc (hd::acc) tl
  in 
  rev_acc [] l;;


let defiler file = 
  let f1,f2 = file in 
  match !f1,!f2 with
    [],[] -> failwith(" rien a defiler ") 
  |[],_ -> f1 := rev_list !f2; f2 := [];  let a::q = !f1 in f1 := q; a
  |_,_ -> let a::q = !f1 in f1 := q; a;;



let tete file = let f1,f2 = file in 
  match !f1,!f2 with
    [],[] -> failwith(" pas de tete ") 
  |[],_ -> f1 := rev_list !f2; f2 := [];  let a::q = !f1 in a
  |_,_ -> let a::q = !f1 in  a;;

List.iter;;
  
let parcours_largeur g = 
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do
		pere.(i) <- i
	done;
	let f = creer_file () in
	for s = 0 to (n-1) do
		if not marque.(s) then begin
			marque.(s) <- true;
			enfiler f s;
			while not (est_vide f) do
				let u = defiler f in
				let traitement v =
					if not marque.(v) then begin
						marque.(v) <- true;
						pere.(v) <- u;
						enfiler f v
					end
				in
				List.iter traitement g.(u);
			done;
		end
	done;
	pere;;
	
let g = [| [1;3] ; [2 ; 3] ; [0] ; [] ; [5;6] ; [] ; [5] |]
;;	


parcours_largeur g;;


(*let rec iteration p l =
	match l with
		[] -> ()
		|a::q -> p a; iteration p q;;*)

let parcours_profondeur_rec g = 
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	let rec visiter u =
		marque.(u) <- true;
		let traitement v =
			if not marque.(v) then begin
				pere.(v) <- u;
				visiter v
			end
		in
		List.iter traitement g.(u)
	in
	for i = 0 to (n-1) do
		pere.(i) <- i
	done;
	for s = 0 to (n-1) do
		if not marque.(s) then visiter s
	done;
	pere;;
	
parcours_profondeur_rec g;;

type 'a pile = 'a list ref;;

let creer_pile () :'a pile = ref [];;

let est_vide (p:'a pile) = !p = [];;

let empiler (p :'a pile) v = p := v::!p;;

let depiler (p :'a pile) = let a::q = !p in p:=q;a;;






let parcours_profondeur_pile g = 
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do
		pere.(i) <- i
	done;
	let p = creer_pile () in
	for s = 0 to (n-1) do
		if not marque.(s) then begin
			empiler p s;
			while not (est_vide p) do
				let u = depiler p in
				if not marque.(u) then begin
					marque.(u) <- true;
					let traitement v =
						if not marque.(v) then begin
							pere.(v) <- u;
							empiler p v
						end
					in
					List.iter traitement g.(u);
				end
			done;
		end
	done;
	pere;;

parcours_profondeur_pile g;;

let tri_topologique g = 
	let n = Array.length g in
	let marque = Array.make n false in
	let tri = ref [] in
	let rec visiter u =
		marque.(u) <- true;
		let traitement v =
			if not marque.(v) then begin
				visiter v
			end
		in
		List.iter traitement g.(u);
		tri := u::!tri
	in
	for s = 0 to (n-1) do
		if not marque.(s) then visiter s
	done;
	!tri;;
	
let g = [| [1;2] ; [] ; [3] ; [4;5] ; [] ; [4] |];;

tri_topologique g;;
