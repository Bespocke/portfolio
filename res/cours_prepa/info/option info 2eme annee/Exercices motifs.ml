let mot_pos_i t m i =
	let n = String.length t in
	let a = String.length m in
	let b = ref 0 in
	let u = ref 0 in 
	if n - i < a then false
	else begin
		while !u < a && !b = 0 do
		if m.[!u] <> t.[i + !u] then incr b
		else incr u
		done;
		!b = 0
		end;;
		
let recherche_sous_mot m t =
	let n = String.length t in
	let l = ref [] in
	for i = 0 to (n-1) do
	if mot_pos_i t m i then l:= i::!l
	done;
	!l;;
	
recherche_sous_mot "aab" "aaabaab";;




recherche_non_consec "abcde" "ce";;

let recherche_non_consec t m = 
	let n_t = String.length t in
	let n_m = String.length m in
	let i_m = ref 0 in 
	let i_t = ref 0 in 
	while !i_m < n_m && !i_t < n_t do 
		if t.[!i_t] = m.[!i_m] then (incr i_m ; incr i_t) 
		else incr i_t
	done ; 
	!i_m = n_m ;;
	
recherche_non_consec "daaecbe" "abc";;