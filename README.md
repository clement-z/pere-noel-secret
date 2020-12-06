# Père Noël secret

Deux petits scripts qui permettent de:

* Générer une liste de paires "donneur"/"receveur" de cadeau sur la base d'un
  fichier CSV contenant les noms et coordonnées des participants;
* Envoyer automatiquement un mail à tous les participants pour leur dire à qui
  envoyer leur cadeau.

L'idée est que celui qui lance le script n'a pas besoin de savoir qui donne un
cadeau à qui non plus.

[English version of the README](README.en.md)

## Prérequis

* Avoir `python3`;
* Pouvoir envoyer des mails depuis sa machine via la commande `sendmail` (en
  installant `sendmail`, `postfix`, `exim`...);
* Pour ne pas tomber dans le spam des destinataires voire être refoulé, je
  pense qu'il vaut mieux avoir configuré ses enregistrements DNS correctement
  avant (mais j'ai pas envie de tester/me renseigner maintenant).

## Utilisation

1. Remplir `coord.csv` avec les noms et coordonnées des participants, en
   suivant le format défini par la première ligne;
2. Optionnel: remplir `blacklist.txt` avec les règles d'exclusions (par exemple
   un couple);
3. Lancer `./generate_list.py`, vérifier que la sortie est correcte;
4. Modifier `send_mails.py` pour changer `zrounba.fr` en votre domaine,
   modifier la template du mail, le sujet, etc.
5. Lancer `./send_mails.py`, vérifier la sortie;
6. Lancer `./send_mails.py --ok` si tout est bon! C'est envoyé!

Pour un test-run, vous pouvez utiliser un service comme
[YOPmail](https://yopmail.com), pour utiliser de fausses addresses
destinataires. Cependant leur client mail n'affiche pas forcément bien le
contenu UTF8 apparemment.

## Noyeux Joël !
