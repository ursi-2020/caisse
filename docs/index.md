[Sommaire](https://ursi-2020.github.io/Documentation/)

# Sections

* [API](api.md)
* [Communication](communication.md)
* [Flux](flux.md)
* [Use Case](use-case.md)
* [Routes](routes.md)

# Rôle de l'application

Le rôle de `Caisse` est de faire la liaison entre le `magasin` et le `système de paiement`. 
Au moment d’un paiement, génération d’un ticket pour le `magasin` et fait appel au service de `système de paiement`.

Auprès de `paiement` la `caisse` calcul la somme totale à payer et s'assure que le paiement a bien été effectué.

Auprès de `magasin` la `caisse` récupère quotidiennement la liste des produits.
Pour chaque passage en caisse d'un client la caisse récupère les données du client, applique les promotions liés aux points de fidélité et envoie un ticket avec l'identifiant du client, le prix total payé, la liste des produits payés et les points de fidélités utilisé.
La `caisse` demande la création d'un compte client à `magasin` s'il n'existe pas.

La `caisse` peut également commander un produit pour un client

En local, la `caisse` peut schéduler la mise à jour de la base de données, mettre à jour la base de données manuellement et afficher le prix à payer, les promotions appliquées et les points de fidélités disponible.
La caisse peut chercher un produit dans le stock local.
