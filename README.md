## Introduction

**Antilaw** is a digital version of the card game  [Antimony](https://boardgamegeek.com/boardgame/251441/antinomy/). This is a card game with clear winning and losing conditions and two modalities; Solo or Competitive (1v1). The rules are simple, but the disposition of the cards on the board brings complexity to the game. This is a race to be the first one to collect the necessary amount of points to win the game, while solving a puzzle that changes with every movement.

***Disclaimer**: This code is purely for learning practice purpose and is not intended for commercial use. All the information used for the development of the application is publicly available online, as for whoever is interested on this game I encourage them to purchase the PnP versions of the [base game](https://www.pnparcade.com/products/copy-of-antinomy) and the [solo expansion](https://www.pnparcade.com/products/antinomy-1).*

<br>

## Game Rules

There are 9 cards placed face up, in a straight line, between the players. Each player starts with 3 cards on hand and a sorcerer at a starting position on one of the cards on the table.

The objective of the game is obtain 5 crystals. Players get a crystal when performing a "paradox", which is having on hand 3 cards with matching color, symbol or number. 

To get these combination players will use a card from their hand to move their sorcerer along the 9 cards, using the card number to move that number of positions to the right, or using the color/symbol to move to the position of a matching card to the left. Then the player will switch the card used to move for the card on the table where the sorcerer has landed.

If a player's sorcerer lands on the same position where the other player's sorcerer is, both would reveal their hand to compare the strength of their hand by comparing the number. The payer with stronger hand will steal a crystal from the other player.

<br>

## Project Objectives
The decision to choose this game was the easy rules and gameplay would allow me to focus on the overall structure of the app, develop a Machine Learning for the Competitive mode against the app, internet connectivity for a the Competitive mode Online against other players and manipulation of databases.

<br>

## Lessons Learned
Event management.
Create and manage animations.
Managing SQLite databases.
Use Buildozer to compile apk file.
Access Android internal storage.
