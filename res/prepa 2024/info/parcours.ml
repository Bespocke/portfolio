

let c = 1000000;;

let creer_file () = Array.make (c+2) 0;; 
let file_vide file = file.(Array.length file - 1) = 0;;

let enfiler f v = 
	let t = f.(c+1) in
	if c=t then failwith "erreur enfiler : capacit� atteinte";
	f.(c+1) <- f.(c+1) + 1;
	let p = (f.(c) + t) mod c  in
	f.(p) <- v;;
	
let t = [|5;7;8;1;4;2;1;4;5|];;

enfiler  t 6;;


t;;	

let defiler f = 
    if f.(c+1) = 0 then failwith "erreur defiler : la file est vide";
    let v = f.(f.(c)) in
    f.(c) <- (f.(c) +1) mod c;
    f.(c+1) <- f.(c+1) -1;
    v;;
   
List.iter;;   

let parcours_largeur g = 
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do pere.(i) <- i done;
	let f = creer_file () in
	for s = 0 to (n-1) do
		if not marque.(s) then begin
			marque.(s) <- true;
			print_int s;
			print_newline ();
			enfiler f s;
			while not (est_vide f) do
				let u = defiler f in
				let aux v =
					if not marque.(v) then begin
						marque.(v) <- true;
						print_int v;
						print_newline ();
						pere.(v) <- u;
						enfiler f v
					end
				in
				List.iter aux g.(u);
			done
		end
	done;
	pere;;
	
let g = [| [1; 7]; [0; 2; 3]; [1; 3]; [1; 2]; [5; 6]; [4; 6]; [4; 5]; [0]|];;

parcours_largeur g;;
￼
let parcours_profondeur_rec g =
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do pere.(i) <- i done;
	
	let rec visiter u =
		marque.(u) <- true;
		print_int u;
		print_newline ();
		let aux v = 
			if not marque.(v) then begin
				pere.(v) <- u;
				visiter v
			end
		in
		List.iter aux g.(u)
	in
	
	for s = 0 to (n-1) do
		if not marque.(s)
		then visiter s
	done;
	pere;;
	
parcours_profondeur_rec g;;


type 'a pile = 'a list ref;;

let creer_pile () :'a pile = ref [];;

let est_vide (p:'a pile) = !p = [];;

let empiler (p :'a pile) v = p := v::!p;;

let depiler (p :'a pile) = let a::q = !p in p:=q;a;;

let parcours_profondeur_it g =
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do pere.(i) <- i done;
	let p = creer_pile () in
	for s = 0 to (n-1) do
		if not marque.(s) then begin
			empiler p s;
			while not (est_vide p) do
				let u = depiler p in
				if not marque.(u) then begin 
					marque.(u) <- true;
					print_int u;
					print_newline ();
					let aux v =
						if not marque.(v) then begin
							pere.(v) <- u;
							empiler p v
						end
					in
					List.iter aux g.(u);
				end
			done
		end
	done;
	pere;;
	
parcours_profondeur_it g;;


let tri_topologique g =
	let n = Array.length g in
	let marque = Array.make n false in
	let res = ref [] in
	
	let rec visiter u =
		marque.(u) <- true;
		let aux v = 
			if not marque.(v) then begin
				visiter v
			end
		in
		List.iter aux g.(u);
		res := u::!res
	in
	
	for s = 0 to (n-1) do
		if not marque.(s)
		then visiter s
	done;
	!res;;
	
let g2 = [| [1; 2]; [4]; [3]; [1; 4]; [5]; [1; 6; 7]; []; [] |];;

tri_topologique g2;;

let transpose g =
	let n = Array.length g in
	let gt = Array.make n [] in
	for u = 0 to (n-1) do
		let aux v =
			(* v est un successeur, ie on a un arc u->v dans g *)
			gt.(v) <- u::gt.(v)
		in
		List.iter aux g.(u);
	done;
	gt;;
	
let g3 = [| [2; 3]; [2; 7]; [1]; [4]; [0; 5; 6]; []; []; [8]; [7] |];;

transpose g3;;

let kosaraju g =
	let l = tri_topologique g in
	let gt = transpose g in
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do pere.(i) <- i done;
	
	let rec visiter u =
		marque.(u) <- true;
		let aux v = 
			if not marque.(v) then begin
				pere.(v) <- u;
				visiter v
			end
		in
		List.iter aux gt.(u)
	in
	
	let aux s =
		if not marque.(s)
		then visiter s
	in
	List.iter aux l;
	let m = ref 0 in
	let d = Hashtbl.create 10 in
	for i = 0 to (n-1) do
		if pere.(i) = i then begin
			Hashtbl.add d i !m;
			incr m
			end
	done;
	let t = Array.make !m [] in
	
	let rec racine i =
		if i = pere.(i) then i
		else racine pere.(i)
	in
	
	for i = 0 to (n-1) do
		let p = racine i in
		let j = Hashtbl.find d p in
		t.(j) <- i::t.(j)
	done;
	t;;
	
kosaraju g3;;



let distances g s = 
	let n = Array.length g in
	let marque = Array.make n false in
	let pere = Array.make n 0 in
	for i = 0 to (n-1) do pere.(i) <- i done;
	let f = creer_file () in
	marque.(s) <- true;
	let d = Array.make n 0 in
	enfiler f s;
	while not (file_vide f) do
		let u = defiler f in
		let aux v =
			if not marque.(v) then begin
				marque.(v) <- true;
				pere.(v) <- u;
				d.(v) <- d.(u) + 1;
				enfiler f v
			end
		in
		List.iter aux g.(u);
	done;
	d, pere;;

distances g3 0;;	
