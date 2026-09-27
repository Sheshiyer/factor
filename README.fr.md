[English](README.md) · **Français**

<div align="center">

<img src="assets/morning.jpg" width="100%" alt="Le travail est préparé avant votre arrivée" />

# Factor

Un collaborateur pour le travail qui n’a pas besoin de vous.<br>
Vous gardez les décisions.

</div>

Factor est un framework réutilisable. L’identité, les faits, la voix et les décisions d’une entreprise vivent dans **un dépôt séparé**. Hermes fournit les sessions et les capacités de l’agent. Factor fournit les outils, les modèles et les procédures.

Vous décrivez une tâche. Le système prépare le travail à partir du contexte de l’entreprise. Envoyer, publier ou dépenser exige votre autorisation explicite.

## Comprendre avant de commencer

| Besoin | Ressource |
|---|---|
| Comprendre les composants et leurs rôles | [Guide du framework](docs/ecosystem/2026-09-27/ecosystem.fr.md) |
| Configurer et réaliser une première tâche | [Guide opérationnel](docs/ecosystem/2026-09-27/playbook.fr.md) |
| Présenter le framework | [8 diapositives PDF](docs/assets/fr/framework-slides-v2.pdf) · [PowerPoint](docs/assets/fr/framework-slides-v2.pptx) |
| Expliquer le flux de travail | [8 diapositives PDF](docs/assets/fr/operations-slides-v2.pdf) · [PowerPoint](docs/assets/fr/operations-slides-v2.pptx) |
| Voir une synthèse | [Vidéo — 5 min 10 s](docs/assets/fr/overview-video.mp4) |
| Voir les composants | [Infographie d’architecture](docs/assets/fr/architecture-infographic-v2.png) |
| Comprendre l’apprentissage | [Infographie du protocole](docs/assets/fr/learning-infographic-v2.png) |

La [bibliothèque de ressources](docs/learning.fr.md) rassemble les supports, les versions anglaises des guides et les limites du contrôle. Les médias sont inclus dans le dépôt : leur ouverture ne nécessite pas l’accès au notebook privé.

## Trois portes, une même tâche

| Porte | Usage |
|---|---|
| Menu Mac | Lancez `sh apps/mac/run.sh`, choisissez l’entreprise, puis décrivez la tâche. Application locale non signée. |
| Raycast | Ajoutez `surfaces/raycast` aux commandes de script. Les commandes anglaise et française utilisent la même entreprise. |
| Hermes | La compétence `take-intent` lit la demande et ouvre une carte. |

Le menu Mac écrit une intention ; son ouverture ne prouve pas que le modèle ou la messagerie fonctionne. Le listener de messagerie est la passerelle Hermes, distincte de l’application Mac.

## Anglais par défaut, français au choix

Le menu Mac propose **EN / FR**. L’accueil en ligne de commande propose le même choix, avec accès aux guides et médias.

```sh
# Français pour cette commande.
python3 scripts/onboard.py --language fr --steps

# Conserver le français pour cette entreprise.
python3 scripts/onboard.py --company /chemin/absolu/entreprise --set-language fr

# Afficher ses ressources, sans ouvrir automatiquement une application.
python3 scripts/onboard.py --company /chemin/absolu/entreprise --resources
```

Le choix est enregistré dans `preferences.json` de l’entreprise. Sans préférence, l’anglais s’applique. Les instructions Hermes utilisent cette langue pour leurs réponses et nouveaux brouillons, en respectant les consignes explicites de la tâche et les règles de marque approuvées. Les faits, citations, fichiers et identifiants existants ne sont pas traduits automatiquement. Les médias disponibles sont actuellement en français.

## Installer ou mettre à jour

Ouvrez le dépôt dans votre assistant de code et dites :

> Lis `prompt-install.md` et exécute sa procédure d’installation ou de mise à jour. Réponds en français.

Le [prompt d’installation](prompt-install.md) inspecte l’état existant, protège les données de l’entreprise, vérifie la source de mise à jour, exécute les contrôles et prépare la passerelle choisie.

Pour créer manuellement une entreprise neuve :

```sh
git clone https://github.com/Sheshiyer/factor.git
cd factor
sh scripts/new-company.sh acme ~/companies/acme
```

Dans le projet où vous avez construit l’entreprise, utilisez le [prompt Claude français](prompts/harvest-claude.fr.md) ou le [prompt Codex français](prompts/harvest-codex.fr.md). Enregistrez `factor-harvest.md`, puis appliquez-le :

```sh
python3 scripts/onboard.py --company ~/companies/acme \
  --apply-harvest /chemin/du/projet/factor-harvest.md
python3 scripts/onboard.py --company ~/companies/acme --set-language fr
python3 scripts/check_company.py ~/companies/acme
```

Les titres structurés du harvest restent en anglais pour préserver le format lu par les outils ; les réponses et le contenu peuvent être français. Une information manquante reste explicitement inconnue.

## Une mémoire qui se consulte

L’instinct reste court et accompagne le travail. Le wiki, la marque et les corrections restent sur disque. L’agent lit l’index puis la page utile, sans remplir sa mémoire de toute l’entreprise. Les compétences et connecteurs sont choisis au besoin ; consulter une ressource pédagogique n’active aucun outil.

Les outils locaux de [curation](docs/knowledge-curation.md) conservent provenance, versions et corrections. Le [flux de bookmarks](docs/bookmark-ingest.md) signale les articles manquants. Le [protocole d’apprentissage Hermes](docs/hermes-learning-loop.md) prévoit relecture, approbation et essai dans une nouvelle session sur un cas différent.

La version [v0.6.0](https://github.com/Sheshiyer/factor/releases/tag/v0.6.0) ajoute la curation, l’accueil bilingue et la bibliothèque de ressources. Consultez les [notes de version](docs/releases/v0.6.0.md). Une mise à jour du dépôt reste distincte de la mise à jour d’un profil installé. **Le pilote d’apprentissage sur une entreprise et un profil réels reste à valider.** Un succès local ne démontre ni publication automatique ni amélioration du modèle.

## Repères

- [Deux profils, Claude et Codex](docs/seats.md)
- [Menu Mac](apps/mac/README.md)
- [Commandes Raycast](surfaces/raycast/README.md)
- [Documentation complète EN / FR](docs/ecosystem/2026-09-27/README.md)
- [Licence MIT](LICENSE)
