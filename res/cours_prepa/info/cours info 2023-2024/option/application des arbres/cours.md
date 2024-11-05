## Arbre des configurations

**Le backtracking** est une technique de programmation pertinente lorsqu'on cherche la solution d'un problème parmi un grand nombre de possibilités et pouvant être représentées par un arbre des configurations possibles. Les feuilles correspondent aux configurations complètes, et les noeuds internes aux configurations partielles.

## Tas binaire

Est un arbre binaire vérifiant certaines propriétées :
- A chaque noeud est associé une clé
- La clé de chaque noeud est supérieure à la clé de chacun de ses fils :
- l'arbre est complet à gauche : tous les niveaux de profondeur sont complet sauf éventuellement le dernier, rempli de gauche à droite.

On représentera les tas binaires sous forme de tableaux en lisant les clés de haut en bas et de gauche à droite.  

exemple : [|20;27;8;12;15;3;2;1;4;13|] est un tas binaire,
et pour un noeud d'indice i :
- le fils gauche est d'indice : $2i+1$
- le fils droit : $2i+2$
- le père :
    - $\frac{i-2}{2}$ si i pair
    - $\frac{i-1}{2}$ si i impair  
    
    $\lfloor \frac{i-1}{2} \rfloor$ dans le cas général

### i-sur-tas
Est un arbre que l'on peut transformer en tas en remplaçant le noeud i par une valeur inférieur. Autrement dit, c'est un arbre vérifiant les propriétés d'un tas, sauf éventuellement au niveau des inégalités entre le noeud i et ses ascendants.

### i-sous-tas
Est un arbre que l'on peut transformer en tas en remplaçant le noeud i par une valeur supérieur. Autrement dit, c'est un arbre vérifiant les propriétés d'un tas, sauf éventuellement au niveau des inégalités entre le noeud i et ses descendants.

### tri par tas
pour trier un tableau t :
- on initialise une variable taille à la taille du tableau 
- on entasse, de la droite vers la gauche, chaque élément du tableau, de manière à obtenir un tas
- on met l'élément d'indice 0, maximal, à sa place, en le permuttant avec le dernier élément. On décrémente la taille pour s'assurer que l'élément maximal ne soit plus compris dans le tas, donc plus déplacé. On entasse l'élément arrivé en mosition 0 pour retrouver une structure de tas
- On itère l'étape précédente pour placer tous les éléments à leur place.

### files de priorité
```ocaml
type ('a,'b) file_prio =
    {mutable taille :int;
    tas : ('a*'b) option array};;
```

## Graphes

### Parcours de graphe
stratégie d'exploration des sommets du graphe, les arrêtes empruntés lors du parcours forment une arborescence ie un ensemble d'arbres.
Une telle arborescence peut être représentée efficacement par un tableau associant à chaque sommet son père. Les sommets initiaux sont dans cette représentation traités comme leurs propre père.
On distingue deux familles de parcours :
- en largeur : on explore tous les sommets de distance $k$ du sommet initial avant de passer à ceux de distance $k + 1$
- en profondeur : on visite à chaque étape un successeur du dernier sommet exploré.

### Parcours largeur
``` ocaml
parcours_largeur G
    chaque sommet est non marqué
    chaque sommet est son propre père
    soit F une file vide
    pour chaque sommet s de G
        si s non marqué
            on marque s 
            on enfile s dans F
            tant que F non vide
                on défile un sommet u dans F
                pour chaque v successeur de u 
                    si v non marqué 
                        on marque v 
                        le père de v devient u
                        on enfile v dans F
```

``` ocaml
let parcours_largeur G =
    let n = Array.length g in
    let marque = Array.make n false in
    let pere = Array.make n 0 in
    for i = 0 to (n-1) do pere.(i) <- i done;
    let f = creer_file () in
    for s = 0 to (n-1) do
        if not marque.(s) then begin
            marque.(s) <- true;
            print_int(s);
            print_newline();
            enfiler f s;
            while not (est_vide f) do
                let u = (defiler f) in
                let aux v =
                    if not marque.(v) then begin
                        marque.(v) <- true;
                        pere.(v) <- u;
                        enfiler f v
                    end
                in
                list.iter aux g.(u)
            done
        end
    done
    pere;;
```
### En profondeur
```
parcours_en_profondeur G
    chaque sommet est non marqué
```

``` ocaml
let parcours_en_profondeur g =
    let n = Array.length g in 
    let marque = Array.make n false in
    let pere = Array.make n 0 in
    for i = 0 to (n-1) do pere.(i) <- i done; 

    let rec visiter u =
        marque.(u) <- true;
        print_int(s);
        print_newline();
        let aux v =
            if not marque.(v) then begin
                pere.(v) <- u;
                visiter v
            end
        in
        list.iter aux g.(u)
    in  

    for s = 0 to (n-1) do
        if not marque.(s) then visiter s
    done;;
```

### tri topolgique
sur un graphe orienté acyclique. Obtenu à partir d'un parcours en profondeur récursif : on traite chaque sommet après ses successeurs. Les sommets seront alors traités dans l'ordre inverse d'un tri topologique.
On peut par exemple traiter chaque élément en l'ajoutant au début d'une liste pour récupérer un tri topologiquesous forme de liste.
