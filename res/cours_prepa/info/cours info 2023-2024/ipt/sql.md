## Attributs d'une table
### Clé primaire :
Ensemble d'attribut de la table donnant la garantie que deux lignes distinctes ne fournissent pas la même valeur
### Clé étrangère : 
Attribut de la table renvoyant vers la clé primaire d'une autre.  

## Effectuer des requêtes sql sur les tables et leurs attributs :
```sql   
Select nom   
From ELEVE
```
ou pour tout sélectionner : 
```sql
Select *
From ELEVE
```

### Ajouter une condition :
On utilisera Where suivi de la condition
```sql
Select nom,prenom
From ELEVE
Where classe = "MP"
```

### Le Select permet également de réaliser des calculs : 
```SQL
Select nom, prenom, (moyenne_Math + moyenne_Physique)/2
From ELEVE
Where classe = "MP"
```

### Renommer ce que l'on récupère : 
```SQL
Select nom, prenom, (moyenne_Math + moyenne_Physique)/2 as moyenne_scientifique
From ELEVE
Where classe = "MP"
```

### Opérations ensemblistes : 
On possède les unions et intersection classique avec les mots clés **Union** et **Intersecetion** ou **Intersect**
```sql
Select nom, prenom
From PROF_BUFFON
Union
Select nom, prenom
From PROF_LLG
```
et pour l'intersection :
```sql
Select nom, prenom
From PROF_BUFFON
Intersect
Select nom, prenom
From PROF_LLG
```

### Jointures :
Permet de combiner les attributs de deux tables
```sql
Select *
From ELEVE Join CLASSE
On ELEVE.filiere = CLASSE.filiere
```
Puis on peut ajouter les conditions : 
```sql
Select filiale
From CLASSE Join SALLE
On numerosalle = numero
Where effectif > capacité
```

## Architecture
- une association 1-1 associe à chaque élément d'une table exactement un élément de l'autre table
- 1-* chaque élément de B est associé à un élément de B, mais un élément de A est associé à un nombre quelconcque d'éléments de B. **La clé étrangère est dans B**
- *-1 chaque élément de A est associé à un élément de B, mais un élément de B est associé à un nombre quelconcque d'éléments de A. **La clé étrangère est dans A**
- *-* associe à chaque éléments d'une table un nomber quelconque d'éléments de l'autre table.

