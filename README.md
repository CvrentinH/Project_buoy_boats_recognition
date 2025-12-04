# Maritime Obstacle Detection : buoy and boats

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-FF0000?style=for-the-badge&logo=ultralytics&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

## Résumé
Ce projet est un module de perception autonome conçu pour détecter des obstacles maritimes (bouées et bateaux) en temps réel.

L'architecture est optimisée pour un déploiement faible consommation, sans GPU :
1.  **Computer Vision** : Utilisation de YOLOv8 Nano fine-tuné sur un dataset maritime spécifique.
2.  **Inférence Optimisée** : Pipeline vidéo via OpenCV avec gestion de mémoire par générateurs (`stream=True`) pour une stabilité sur longue durée.
3.  **Conteneurisation** : Image Docker optimisée pour CPU (< 1GB) séparant l'environnement de build et de run.
4.  **Reproductibilité** : Automatisation complète via `Makefile` et gestion sécurisée des secrets.

![Image reconnaissance](recognition.PNG)

---

## Performance & Résultats

Le modèle a été entraîné sur 50 epochs (par manque de puissance de calcul) avec un Dataset spécifique "Buoys & Boats" (via Roboflow).
[fichiers](https://universe.roboflow.com/clearwater/buoys-and-boats)

### 1. Métriques d'Entraînement
Le modèle atteint une précision (mAP) satisfaisante pour un modèle Nano, garantissant une inférence rapide (>30 FPS sur CPU standard).

![Résultats de l'entraînement](results.png)
*(Courbes de perte et de précision durant l'entraînement)*

### 2. Matrice de Confusion
Capacité du modèle à distinguer les classes (Bouées vs Bateaux) et à ignorer le fond (Background).

![Matrice de Confusion](confusion_matrix.png)

---

## Architecture Technique

Le projet suit une séparation stricte entre la **R&D (Entraînement)** et la **Production (Inférence)**.

| Module | Techno | Description |
| :--- | :--- | :--- |
| **Training** | `PyTorch` + `CUDA` | Entraînement sur GPU/Cloud. Nécessite une clé API. Génère le fichier `best.pt`. |
| **Inférence** | `OpenCV` + `YOLO` | **Totalement Offline**. N'utilise que le CPU. Ne dépend pas d'internet. |

### Optimisation Embarquée (Challenges résolus)
* **Réduction de l'image Docker :** Passage de 16Go (Standard) à **~1Go** en forçant l'installation de `torch-cpu`, `opencv-headless` et en excluant les caches de build.
* **Stabilité RAM :** Utilisation de générateurs Python pour le traitement vidéo, évitant la saturation mémoire sur les flux continus.

---

## Comment lancer le projet

### Prérequis

* Docker
* Python 3.11+
* Webcam (Pour la démo temps réel)

### Option 1 : Inférence Rapide (Local)
Pour tester la détection sur votre webcam immédiatement sans passer par Docker.

```bash
# 1. Installer les dépendances
make install

# 2. Lancer la détection (Webcam par défaut)
make run
```

### Option 2 : Déploiement Conteneurisé

Simule le déploiement sur le drone. L'image est construite et lancée avec accès au périphérique vidéo et forward X11.

```bash
# Build image + Lance le conteneur GUI
make deploy
```

### Option 3 : Ré-entraîner le modèle (R&D)

Si vous souhaitez reproduire l'entraînement (nécessite une clé API) :

Créez un fichier .env à la racine : API_KEY=votre_clé.

Lancez le script d'entraînement :

```bash
# Build l'image + Lance le conteneur GUI
python src/train.py
```
