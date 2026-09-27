# Supports visuels Factor en français

[NotebookLM — Factor](https://notebooklm.google.com/notebook/ed5305d5-9bca-4a00-b2a8-5d2f811c1222)

Ce lot comprend deux présentations, une vidéo de synthèse et deux infographies. Il utilise exclusivement les deux guides français revus et la source de corrections éditoriales, sélectionnés par identifiants explicites. Le contenu porte sur le framework Factor et ses intégrations produit.

| Support | Usage |
|---|---|
| Comprendre le framework | Présentation d’ensemble pour un fondateur et ses collaborateurs |
| Du premier travail à l’apprentissage | Présentation détaillée du flux opérationnel |
| Vue d’ensemble vidéo | Explication accessible du rôle et du fonctionnement de Factor |
| Architecture en un regard | Infographie des composants, du contexte et des décisions |
| Apprendre d’un travail vérifié | Infographie de la boucle de correction et de réutilisation |

Les supports distinguent les outils locaux vérifiés du pilote Hermes restant à valider. Leurs exemples n’activent ni profil, ni connecteur, ni routine. Les sources, paramètres et identifiants de génération sont conservés dans `generation-receipt.json` ; les consignes françaises se trouvent dans `prompts/`. Les exports et leurs empreintes sont enregistrés dans `download-receipt.json` lorsqu’ils sont disponibles.

Les éditions retenues sont maintenant incluses dans `docs/assets/fr/` pour l’accueil hors ligne. Les premiers jets restent dans le dossier historique de la conversation. Les reçus de téléchargement conservent les chemins d’origine ; `docs/assets/manifest.json` fournit les chemins portables et empreintes des éditions retenues.

## Infographies revues

- [Architecture de Factor — PNG](../../../assets/fr/architecture-infographic-v2.png)
- [Apprendre d’un travail vérifié — PNG](../../../assets/fr/learning-infographic-v2.png)

**Légende à conserver avec l’infographie d’apprentissage : protocole proposé ; pilote Hermes à valider.** La dernière étape demande une nouvelle session, un cas différent et une réussite vérifiée. Il s’agit d’apprentissage de procédures, sans modification des poids du modèle.

## Versions et contrôle

Les premiers jets des deux infographies et des deux présentations sont conservés pour la traçabilité, mais ne sont pas les éditions à diffuser. Ils sont nommés « BROUILLON NON VALIDÉ » dans NotebookLM. Les infographies v2 ont été relues entièrement ; les deux présentations v2 ont été relues sur leurs huit diapositives respectives. Les défauts et les limites sont consignés dans `infographic-review.json`, `deck-review.json` et `video-review.json`.

## Vidéo de synthèse

[Regarder la vidéo MP4 — 5 min 10 s](../../../assets/fr/overview-video.mp4). Export 1280 × 720, avec piste audio.

Le décodage complet a réussi. Le contrôle visuel couvre 17 images réparties dans la vidéo et 12 images de changement de scène. Une étiquette décorative « Facteur » et quelques termes anglais subsistent. La narration n’a pas fait l’objet d’une écoute ou d’une transcription indépendante ; le contrôle ne constitue donc pas une validation exhaustive du commentaire parlé.

## Présentations v2

| Présentation | PDF | PowerPoint |
|---|---|---|
| Comprendre le framework — 8 diapositives | [PDF](../../../assets/fr/framework-slides-v2.pdf) | [PPTX](../../../assets/fr/framework-slides-v2.pptx) |
| Du travail à l’apprentissage — 8 diapositives | [PDF](../../../assets/fr/operations-slides-v2.pdf) | [PPTX](../../../assets/fr/operations-slides-v2.pptx) |

Les fichiers PowerPoint sont les exports NotebookLM ; l’édition indépendante de chaque élément graphique n’est pas garantie. Pour les commandes exactes, consulter [le guide opérationnel français](../playbook.fr.md).

Contrôle détaillé et limites : [verification.md](verification.md). Les cinq supports finaux sont identifiés dans [delivery-manifest.json](delivery-manifest.json).
