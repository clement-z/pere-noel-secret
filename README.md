# Père Noël secret

Deux petits scripts qui permettent de:

* Générer une liste de paires "donneur"/"receveur" de cadeau sur la base d'un fichier
  CSV contenant les noms et coordonnées des participants;
* Envoyer automatiquement un mail à tous les participants pour leur dire à qui
  envoyer leur cadeau.

L'idée est que celui qui lance le script n'a pas besoin de savoir qui donne un cadeau à qui non plus.

[English version of the README](README.en.md)

## Prérequis

* Avoir `python` 3;
* Pouvoir envoyer des mails depuis sa machine via la commande `sendmail` (en
  installant `sendmail`, `postfix`, `exim`...);
* Pour ne pas tomber dans le spam des destinataires voire être refoulé, je
  pense qu'il vaut mieux avoir configuré ses enregistrements DNS correctement avant (mais
  j'ai pas envie de tester/me renseigner maintenant).

## Utilisation

1. Remplir `coord.csv` avec les noms et coordonnées des participants, en
   suivant le format défini par la première ligne;
2. Lancer `./generate_list.py`;
3. Lancer `./send_mails.py`, vérifier la sortie;
4. Lancer `./send_mails.py --ok` si tout est bon.

Pour un test-run, vous pouvez utiliser un service comme [YOPmail](https://yopmail.com), pour utiliser de fausses addresses destinataires.
