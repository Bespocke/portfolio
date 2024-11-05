val print_list : int list -> unit
val print_list_list : int list list -> unit
val exemple : int -> int -> unit
val contrainte : int list -> int -> int -> bool
val n_dames : int -> unit
val n_dames_rapide : int -> unit
val contrainte_cavalier : int list -> int -> bool
val super_dame : int -> unit
val gauche : int -> int
val droite : int -> int
val pere : int -> int
type arbre = N of arbre * int * arbre | V
val tableau_vers_arbre : int array -> arbre
val taille : arbre -> int
