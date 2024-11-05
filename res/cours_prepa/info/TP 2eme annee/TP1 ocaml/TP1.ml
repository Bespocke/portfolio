(*sudoku*)

let test_colonne s i j =
	let k = ref 0 in
	while !k < 9 && (!k = i || (s.(!k).(j) <> s.(i).(j) )) do
		incr k
	done;
	!k = 9;;
	
	
let test_ligne s i j =
	let k = ref 0 in
	while !k < 9 && (!k = j || (s.(i).(!k) <> s.(i).(j) )) do
		incr k
	done;
	!k = 9;;

let test_carre s i j =
	let imin = i - (i mod 3) in
	let jmin = j - (j mod 3) in
	let k = ref 0 in
	while (let x = imin + (!k/3) in let y = jmin + (!k mod 3) in !k < 9  && ((x,y) = (i,j) || (s.(x).(y) <> s.(i).(j) ))) do
		incr k
	done;
	!k = 9;;

let afficher_grille g = 
	let n = Array.length g in
	for i = 0 to (n-1) do
		for j = 0 to (n-1) do
			print_int g.(i).(j);
			let s = if ((j+1) mod n) = 0 then "\n" else "\t" in
			print_string s;
			done;
		done;
	print_string "\n\n";;

let g = Array.make_matrix 9 9 0;;

g.(1).(2) <- 3;;


g.(4).(4) <- 7;;

g.(6).(7) <- 8;;

g.(0).(3) <- 9;;

g.(8).(8) <- 2;;

g.(1).(4) <- 1;;

g.(2).(5) <- 2;;

g.(6).(1) <- 5;;


afficher_grille g;;	

test_ligne g 6 1;;

let resoudre sudoku =
	let continuer = ref true in
	let rec parcours pos =
		if not !continuer then () else
		let i = pos / 9 in
		let j = pos mod 9 in
		if pos = 81 then (continuer := false; afficher_grille sudoku) else
		begin
		if sudoku.(i).(j) <> 0 then
			parcours (pos+1)
		else
		for k = 1 to 9 do
			sudoku.(i).(j) <- k;
			if test_ligne sudoku i j && test_colonne sudoku i j && test_carre sudoku i j
			then parcours (pos+1)
		done;
		sudoku.(i).(j) <- 0
		end
	in
	parcours 0;;
	
resoudre g;;





let gauche i = 2*i + 1;;

let droit i = 2*i + 2;;

let pere i = (i-1)/2;;





(* file de priorité avec modification de priorité *)




let gauche i = 2*i + 1;;

let droit i = 2*i + 2;;

let pere i = (i-1)/2;;



type file_prio = {mutable taille : int ; tas : (int*int) array ; position : int array};; 

let creer_file c = {taille = 0 ; tas = Array.make c (-1,-1) ; position = Array.make c c};;


let cle f i = fst f.tas.(i);;

let valeur f i = snd f.tas.(i);;

let echanger f i j = 
	f.position.(valeur f i) <- j;
	f.position.(valeur f j) <- i;
	let temp = f.tas.(i) in
	f.tas.(i) <- f.tas.(j);
	f.tas.(j) <- temp;;



let max3 a b c = max a (max b c);;


let indice_max t i j k =
	let max3 i j k = max (max i j ) k in
	let m = max3 t.(i) t.(j) t.(k) in
	if m = t.(i) then i
	else if m = t.(j) then j
	else k;;


let rec entasser f i =
	let g = gauche i in
	let d = droit i in
	let n = f.taille in
	if d<n then
		begin
		let k = indice_max t i g d in
		if k!=i then 
			begin
			echanger f i k;
			entasser f k			
			end
		end
	else if d = n && t.(g) > t.(i) then 
		echanger f i g
	;;

let rec remonter f i =
	if i!=0 && cle f (pere i)<cle f i then begin echanger f i (pere i); remonter f (pere i) end;;
 						
let est_vide f = f.taille = 0;;	

let defiler f = 
	let resultat = f.tas.(0) in
	echanger f 0 (f.taille - 1);
	f.taille <- f.taille - 1;
	entasser f 0;
	resultat;;



let ajouter_valeur f c v = 
	if f.taille = Array.length f.tas then failwith "file complète";
	f.taille<-f.taille + 1;
	f.tas.(f.taille - 1)<-(c,v);
	f.position.(v)<-f.taille - 1;
	remonter f (f.taille-1);;
	


let modifier_prio f c v =
	let i = f.position.(v) in
	if i>=f.taille then failwith "valeur non présente";
	let c' = cle f i in
	f.tas.(i) <- (c,v);
	if c'>c then entasser f i else remonter f i;;


(* Tri pâr tas *)

let echanger t i j =	
	let a = t.(i) in
	t.(i) <- t.(j);
	t.(j) <- a;;


let rec entasser t i taille =
	let g = gauche i in
	let d = droit i in
	if d < taille then
		begin
		let k = indice_max t i g d in
		if k!=i then 
			begin
			echanger t i k;
			entasser t k taille			
			end
		end
	else if d = taille && t.(g) > t.(i) then 
		echanger t i g
	;;


let tri_par_tas t =
	let n = Array.length t in
	let taille = ref n in
	for i = 1 to n do entasser t (n-i) !taille done;
	for i = 1 to (n-1) do 
		echanger t 0 (n-i) ;
		decr taille;
		entasser t 0 !taille;
	done;;

let t = [|3;2;4;5;5;6;2;1|];;

tri_par_tas t;;

t;;

				  