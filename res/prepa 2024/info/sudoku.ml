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
		if sudoku.(i).(j) <> 0 
		then parcours (pos+1)
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



