(* Backtracking *)

let rec print_list = function
  |[] -> print_string "[]" 
  |[x] -> print_int x
  |a::q -> print_int a; print_string ";"; print_list q;;

(* print_list [1;2;3] *)

let rec print_list_list = function
  |[] -> print_string "[]"
  |[x] -> print_string "["; print_list x; print_string "]"
  |a::q -> print_string "["; print_list a; print_string "];"; print_list_list q;;

let exemple n m = 
  let l = ref [] in
  let rec backtracking config  length =
    if length == n then l := config::!l
    else
      for i = 0 to m-1 do 
        if not (List.mem i config) then backtracking (i::config) (length+1)
      done
  in
  backtracking [] 0;
  print_list_list(!l);;

(* exemple 2 3;; *)

let rec contrainte config i dec = 
  match config with 
    |[] -> true
    |j::q -> i<>j && abs(j-i) <> dec && contrainte q i (dec+1);;

let n_dames n = 
  let l = ref [] in
  let rec backtracking config  length =
    if length == n then l := config::!l
    else
      for i = 0 to n-1 do 
        if contrainte config i 1 then backtracking (i::config) (length+1)
      done
  in
  backtracking [] 0;
  print_list_list(!l); print_newline(); print_string "nombre de possibilités: " ; print_int (List.length !l);;

(* n_dames 12;; *)

let n_dames_rapide n = 
  let l = ref [] in
  let continue = ref true in
  let rec backtracking config  length =
    if !continue then begin
      if length == n then begin l := config::!l; continue:= false end
      else
        for i = 0 to n-1 do 
          if contrainte config i 1 then backtracking (i::config) (length+1)
        done
    end
  in
  backtracking [] 0;
  print_list_list(!l);;
   
(* n_dames_rapide 15;;  *)

let contrainte_cavalier config i = 
  match config with 
    |[] -> true
    |[j] -> abs(j-i) <> 2
    |j::k::q -> abs(j-i) <> 2 && abs(k-i) <> 1

let super_dame n = 
  let l = ref [] in
  let rec backtracking config  length =
      if length == n then begin l := config::!l end
      else
        for i = 0 to n-1 do 
          if (contrainte config i 1) && (contrainte_cavalier config i) then backtracking (i::config) (length+1)
        done
  in
  backtracking [] 0;
  print_list_list(!l);;

(* super_dame 9 ;; *)
(* super_dame 10;; *)



(* Tas binaire *)

let gauche i = 2 * i + 1;;
let droite i = 2 * i + 2;;
let pere i  = (i - 1) / 2;;

type arbre = N of arbre * int * arbre | V;;

let tableau_vers_arbre t =
  let rec aux i =
    if i >= Array.length t then V else N(aux (gauche i),t.(i) , aux (droite i)) 
  in
  aux 0;;

(* tableau_vers_arbre [|20;17;8;12;15;3;2;1;4;13|];; *)

let rec taille a = 
  match a with 
    |V -> 0
    |N(g,_,d) -> 1 + taille g + taille d;;

let arbre_vers_tableau a =
  let t = Array.make (taille a) 0 in
  let rec aux b i =
    match b with 
      |V -> ()
      |N(g, c, d) -> 
        t.(i) <- c;
        aux g (gauche i);
        aux d (droite i)
  in
  aux a 0;
  t;;



(* i-sur-tas *)

let echange t i j =
  let r = t.(i) in
  t.(i) <- t.(j);
  t.(j) <- r;;

let rec remonter t i =
  if i > 0 && t.(i) > t.(pere i) then begin
    echange t i (pere i);
    remonter t (pere i)
  end;;


let rec entasser t i =
  let n = Array.length t in
  let g = gauche i in
  if g = n-1 then 
    (if t.(i) < t.(g) then
      echange t i g)
  else
    let d = droite i in
    if t.(g) < t.(d) && t.(i) < t.(d) then begin
      echange t i d;
      entasser t d
    end
    else if t.(g) > t.(d) && t.(i) < t.(g) then begin
      echange t i g;
      entasser t g 
  end;;



(* file de priorité *)
type ('a,'b) file_prio =
    {mutable taille :int;
    tas : ('a*'b) option array};;

let creer_file_prio c =
  {taille = 0;
  tas = Array.make c None
  }

let est_vide f = f.taille = 0;;

let enfiler f c v =
  if f.taille = Array.length f.tas then failwith "y'a pas de place";
  f.tas.(f.taille) <- Some (c,v);
  remonter f.tas f.taille;;
  
