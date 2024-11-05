let couplage_max g bigU = 
	let n = Array.length g in
	let chemin = Array.make n (-1) in
	let bout = ref 0 in
	let couplage = Array.make n (-1) in
	let existe_chemin_augmentant () =
		let rec aux_pour ls = 
			match ls with
				[] -> false
				|u::rs -> 
					let marque = Array.make n false in
					let rec visiter u =
						marque.(u) <- true;
						let rec visiter_aux ladj =
							match ladj with
								[] -> false
								|v::q -> if couplage.(v) = -1
											then (bout := v; chemin.(v) <- u; true)
											else let w = couplage.(v) in
											if marque.(w) then visiter_aux q
											else begin
												chemin.(v) <- u;
												chemin.(w) <- v;
												(visiter w) || (visiter_aux q)
											end
						in
						visiter_aux g.(u)
					in
					(couplage.(u) = -1 && visiter u) || aux_pour rs
		in
		aux_pour bigU
	in
	let ajouter_arete i j =
		couplage.(i) <- j;
		couplage.(j) <- i
	in
	let enlever_arete i j = 
		couplage.(i) <- -1;
		couplage.(j) <- -1
	in
	let augmenter_couplage () =
		while chemin.(chemin.(!bout)) <> - 1 do
			let x = chemin.(!bout) in
			let y = chemin.(x) in
			enlever_arete x y;
			ajouter_arete !bout x;
			bout := y			
		done;
		ajouter_arete !bout chemin.(!bout)
	in
	while existe_chemin_augmentant () do
		augmenter_couplage ()
	done;
	couplage;;


let g = [|[4;5]; [4;5;6];[6];[5;6]; [0;1]; [0;1;3]; [1;2;3] |];;	

couplage_max g [0;1;2;3];;	

let g = [|[4;5;6]; [5];[5;7];[7]; [0]; [0;1;2]; [0] ; [2;3] |];;	

couplage_max g [0;1;2;3];;	