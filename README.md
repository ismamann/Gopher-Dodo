# 🤖 IA pour les jeux Gopher et Dodo

## 📖 Description
Nous avons conçu et implémenté une **intelligence artificielle** capable de jouer aux jeux **Gopher** et **Dodo**, en utilisant différentes approches issues de la recherche en intelligence artificielle appliquée aux jeux.  

L’objectif était de comparer et d’optimiser plusieurs méthodes de prise de décision face à un adversaire, en prenant en compte les spécificités et symétries propres aux jeux étudiés.

## 🧠 Méthodes et Algorithmes utilisés
- **MCTS (Monte Carlo Tree Search)** :  
  Utilisé pour explorer l’espace des possibles via des simulations aléatoires afin d’estimer les coups les plus prometteurs.  

- **Min-Max avec élagage Alpha-Beta et mémoïsation** :  
  - Réduction de l’espace de recherche grâce à l’**élagage alpha-beta**.  
  - Utilisation de la **mémoïsation** pour stocker et réutiliser les résultats déjà calculés.  
  - Prise en compte des **six symétries** du plateau afin de réduire les états équivalents et optimiser les performances.  

## 🎯 Objectifs
- Développer une IA capable de prendre des décisions optimales ou quasi-optimales.  
- Comparer les performances de **MCTS** et **Min-Max Alpha-Beta** en termes de rapidité et d’efficacité.  
- Exploiter les **symétries des jeux** pour améliorer la vitesse d’exécution et réduire la redondance.  

## 👥 Équipe
- Jeanne Galet
- Ismaël Driche

