# Contrôle des supports français Factor

Date : 27 septembre 2026. Notebook : `ed5305d5-9bca-4a00-b2a8-5d2f811c1222`. CLI NotebookLM : 0.8.0.

## Sources et périmètre

Chaque génération demande explicitement la langue `fr`, le même notebook et uniquement trois sources : guide d’écosystème français revu, guide opérationnel français revu et corrections éditoriales. Leurs identifiants sont enregistrés dans `generation-receipt.json`. Les consignes sont conservées dans `prompts/`. Aucun changement de langue globale ou de notebook courant n’est nécessaire.

Le sujet est Factor, son dépôt d’entreprise distinct et ses intégrations produit. Les supports ne prouvent ni installation de profil, ni activation de connecteur, ni réussite du pilote Hermes. Ils n’ont pas modifié ces composants. Cette livraison ne change aucun code du framework.

## Infographies

Les deux premiers jets ont été rejetés après lecture visuelle : texte français corrompu, chiffre de tests erroné, fausse immutabilité du dépôt d’entreprise et tableau incomplet. Ils sont conservés et renommés « BROUILLON NON VALIDÉ » dans NotebookLM.

Les deux versions v2 ont été intégralement relues. Architecture : rôles distincts, pilote en attente et autorisation humaine explicites. Apprentissage : sept étapes, séparation faits/contexte/procédure, relecture avant écriture et nouvelle session sur un cas différent. Cette dernière image omet le sous-titre demandé concernant l’état du pilote ; sa légende d’accompagnement doit rester « Protocole proposé ; pilote Hermes à valider ». Elle ne déclare pas un succès déjà obtenu.

## Présentations

Les premiers jets ont été lus sur leurs 26 diapositives. Les erreurs motivant leur rejet incluent un ordre d’apprentissage inversé, des commandes tronquées et des formulations trop larges sur l’état installé. Ils sont conservés comme brouillons non validés. Les versions v2 utilisent moins de texte, un protocole séquencé explicite et aucun exemple de commande dans le guide d’opérations ; les commandes exactes restent dans le guide opérationnel revu.

Contrôle des versions v2 : les huit diapositives de chaque présentation ont été inspectées visuellement et acceptées comme supports explicatifs. Aucun blocage factuel ou débordement du texte principal n’a été observé. Restent quelques étiquettes décoratives minuscules en anglais ou peu lisibles dans la présentation du framework et deux formulations de consigne éditoriale dans la présentation opérationnelle. Voir `deck-review.json` pour les constats détaillés.

## Vidéo

Export original de 309,731 secondes (5 min 10 s), 1280 × 720, H.264 24 images/s et audio AAC mono 44,1 kHz. Le décodage complet audio/vidéo réussit sans erreur. Contrôle visuel de 17 images réparties dans le temps et 12 images de changement de scène : français lisible, pilote à valider, autorisation humaine et absence de droit automatique de publication dans les passages contrôlés.

Limites : la narration n’a été ni écoutée ni transcrite indépendamment ; aucune piste de sous-titres n’était intégrée. L’étiquette décorative « Facteur » et quelques termes anglais restent visibles. Ce contrôle échantillonné ne vaut pas validation de chaque image ni du commentaire parlé. Voir `video-review.json`.

## Intégrité et conservation

Les fichiers sont téléchargés par identifiant explicite avec protection contre l’écrasement. `download-receipt.json` enregistre chemins, tailles et SHA-256. Les premiers jets restent distincts des éditions v2. Les médias binaires vivent dans le dossier de livrables de la conversation, hors du dépôt ; seuls consignes, index et preuves de contrôle sont versionnés. Les exports PowerPoint sont fournis sans garantie que tous les éléments soient éditables séparément.

Contrôle final : les 13 exports (premiers jets compris) ont été relus et comparés à leur taille et à leur SHA-256. Le lot de diffusion sélectionne cinq supports, soit sept fichiers avec les doubles exports PDF/PPTX.
