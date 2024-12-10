# **OT_Game_2024 - Game Design Document**

Na danom repozitáre sa nachádza implementácia prototypu hry v Pygame, ktorá bola realizovaná počas cvičení k predmetu Objektové technológie. Na danej hre boli prezentované podstatné herné funkcionality a repozitár slúži ako vzor k vývoju hry určenej pre projekt k predmetu.

**Autor**: Ľubomír Benko

**Vybraná téma**: Swarms (príklad témy)

---
## **1. Úvod**
Navrhnutá hra slúži ako ukážka pre predmet Objektové technológie, s cieľom vytvorenia funkčného prototypu hry ako projektu ku skúške. Vytvorená hra spĺňa požiadavky zadanej témy (Swarms - príklad témy). Hra má charakter hráč proti celému svetu, kde na hráča útočia príšery a jeho cieľom je prepracovať sa k cieľu.

### **1.1 Inšpirácia**
<ins>**Archero**</ins>

Archero je hra zameraná na osamelého lukostrelca, ktorý prechádza rôznymi úrovňami, pričom bojuje s rôznymi nepriateľmi. Koncept hry je založený na ***jeden proti celému svetu***, doplnený o rôzne herné mechaniky, ktoré časom vylepšujú hlavného hrdinu v boji si väčším množstvom silnejších nepriateľov. Hráč si v hre dokáže vylepšovať svoje skilly a zbroj.

<p align="center">
  <img src="https://github.com/l-benko/OT_Game_2024/blob/main/archero.jpg" alt="Archero">
  <br>
  <em>Obrázok 1 Ukážka hry Archero</em>
</p>

<ins>**Survivor.io**</ins>

Survivor.io je mobilná hra zameraná na jedného hrdinu bojujúceho proti veľkému množstvu nepriateľov. Cieľom je prežiť stanovený čas a poraziť všetkých nepriateľov. Počas boja sa hráč ***voľne pohybuje po mape*** a snaží sa prežiť, prípadne nájsť správny okamih zasiahnutia nepriateľov. Nepriatelia ***vždy prenasledujú hráča*** s cieľom ho poraziť.

<p align="center">
  <img src="https://github.com/l-benko/OT_Game_2024/blob/main/survivor.jpg" alt="Survivor.io">
  <br>
  <em>Obrázok 2 Ukážka hry Survivor.io</em>
</p>

### **1.2 Hráčsky zážitok**
Cieľom hry je, aby hráč prežil ***určitý časový interval v hre***, pričom sa nenechá poraziť veľkým množstvom nepriateľov, ktorí sa na neho rútia a pri kontakte mu spôsobujú zranenia. Hráč sa môže pohybovať po mape a zároveň môže likvidovať nepriateľov, čím zvyšuje svoje šance úspešného prežitia časového intervalu.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk 
- **PyCharm 2024.1**: vybrané IDE
- **Tiled 1.10.2**: grafický nástroj na vytváranie levelov
- **Itch.io**: zdroj grafických assetov a zvukov do hry

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč ovláda svoju postavu a snaží sa prežiť v hre stanovený ***časový interval*** (napr. 90 sekúnd). Počas tohto času ***na neho útočia*** nepriatelia, ktorí sa v pravidelných intervaloch spawnujú na mape. Hráč má možnosť násjť a využiť na mape objekty, ktoré mu pomôžu získať bezpečie a nebyť vystavený útokom zo všetkých strán.

### **2.2 Interpretácia témy (Swarms - príklad témy)**
**"Swarms"** - hráč je prenasledovaný veľkým množstvom nepriateľov, ktorých môže zabíjať, avšak sú opätovne generovaný do sveta. Nepriatelia majú nastavený pohyb vždy smerom k hráčovi a tak sa ho snažia premôcť obrovským množstvom. Vo vyšších leveloch je možné zvýšiť intenzitu generovania nepriateľov a zvyšovanie ich odolnosti voči hráčovým útokom.

### **2.3 Základné mechaniky**
- **Prekážky**: na mape sa nachádzajú objekty, ktoré tvoria aktívnu prekážku ako pre hráča, ak aj pre nepriateľov.
- **Bonusové predmety**: hráč môže na mape zbierať predmety, ktoré mu pridajú napr. život, silu útokom alebo znížia čas do konca kola.
- **Pevne stanovené miesta generovania nepriateľov**: nepriatelia sa negenerujú hocikde na mape, ale majú na to pevne stanovené miesta, aby nenastala situácia, že sa nepriateľ spawne doslova na hráčovi, čím sa zníži hrateľnost.

### **2.4 Návrh tried**
- **Game**: trieda, v ktorej sa bude nachádzať hlavná herná logika (úvodná obrazovka, herná slučka, vyhodnotenie hry, ...).
- **Player**: trieda reprezentujúca hráča, ovládanie hráča, vykreslenie postavy a schopnosti.
- **Enemies**: trieda nepriateľov, ich herná logika a pohyb smerom k hráčovi, vykreslenie postáv a schopnosti.

---
## **3. Grafika**

### **3.1 Interpretácia témy (Swarms - príklad témy)**
Hra chce byť vizuálne príťažlivá, kde pomocou assetov z itch.io boli vybrané assety hráča a následne nepriateľov, pričom nepriatelia tým, že budú na hráča útočiť vo veľkom množstve, tak boli vybrané assety rytierov a potom príšer (slime). Zameranie je na 2D kreslené objekty, ktoré budú mať minimalistické animácie pohybu.

<p align="center">
  <img src="https://github.com/l-benko/OT_Game_2024/blob/main/enemies.png" alt="Nepriatelia">
  <br>
  <em>Obrázok 3 Ukážka sprite-ov nepriateľov</em>
</p>

### **3.2 Dizajn**
V hre boli použité assety z itch.io, konkrétne Tiny Swords (https://pixelfrog-assets.itch.io/tiny-swords), s tým, že niektoré objekty budú slúžiť ako aktívne prekážky. Cieľom bolo dosiahnuť na pohľad príjemný animovaný dizajn v kontexte stredovekej fantasy. Ďalšie levely budú vychádzať z rovnakých assetov, pričom sa budú kombinovať rôzne terény a prostredia.

<p align="center">
  <img src="https://github.com/l-benko/OT_Game_2024/blob/main/level.png" alt="Level dizajn">
  <br>
  <em>Obrázok 4 Ukážka dizajnu levelu</em>
</p>

---
## **4. Zvuk**

### **4.1 Hudba**
Výber hudby do pozadia bol zameraný na RPG žánrovo orientovanú hudbu, ktorá bola vybraná z Free RPG Music Pack (https://gianni-canetti.itch.io/free-rpg-music-pack) a bude poskytovať vhodný nádych stredoveku a RPG tématiky, ktorý vhodne dopĺňa grafický dizajn hry.

### **4.2 Zvuky**
Zvuky v hre boli podobne orientované na RPG zvuky, pričom boli opätovne použité voľne dostupné assety vo forme RPG Maker Skit (https://theambientfort.itch.io/rpgmakerskit1), z ktorých bol vybraný zvuk pre výstrel ohnivej gule a zvuk pre zásah nepriateľa.

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Používateľské rozhranie bude orientované do ostatného grafického štýlu a úvodná obrazovka bude obsahovať možnosť spustiť a ukončiť hru.

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **WASD**: pohyb hráča po mape.
- **klávesy šípok**: alternatívne ovládanie pohybu hráča po mape.

<ins>**Myš**</ins> 
- **ľavé tlačidlo**: výstrel ohnivej gule.
