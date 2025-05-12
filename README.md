# 🎮 Dumpster Dash - Enhanced Edition ♻️

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash-SoftEng/blob/main/assets/icons/menu_logo.png" width="512" height="512"/>
</p>

---

## ♻️ Significance of the Game ♻️

<img src="https://github.com/trey020304/test-repository/blob/main/images/E-WEB-Goal-12.png" align="left" width="212"/>

<p align="justify">
According to the 12th goal under the Sustainable Development Goals, it involves establishing sustainable production and consumption habits, which are essential to maintaining the standard of living for both the present and future generations. It calls for more effective and environmentally responsible management of materials throughout their whole lifecycle, from manufacture to disposal. With Dumpster Dash's existence, this would not only serve as a fun application but also raise awareness of sustainability and proper waste segregation. Since many people play video games on their devices, this game is an effective tool to promote Goal 12 to a wide audience of all ages.
</p>

<img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/E_SDG-goals_icons-individual-rgb-15-500x500.jpg" align="left" width="212"/>

<p align="justify">
Human survival depends as much on land as it does on the ocean. Forests cover 30% of Earth's surface, provide clean air and water, and regulate climate. Trash and improper waste segregation destroy natural habitats. Animals often ingest plastic or hazardous waste, which can lead to illness or death. Dumpster Dash aligns with environmental sustainability by teaching users about proper segregation and how irresponsible waste disposal negatively impacts our planet.
</p>

---

## 🎮 Game Concept & Early Development

### Early Design Phase

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/341477161_1250051515632988_5368769938844971349_n.jpg" width="212"/>
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/346149733_1056012145373168_2721184389200773529_n.jpg" width="212"/>
</p>
<p align="center">Initial character sketches of Wally Waste</p>

### Prototype Evolution

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/346134559_808486404179534_5777925480861872611_n.png" width="424"/>
</p>
<p align="center">First background concept for DumpVania</p>

### Animation Development

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/335428268_1526468007762830_3256599577823479950_n.png" width="212"/>
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/349222251_118642044568040_6257362520514358034_n.gif" width="212"/>
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/348901030_1296695137890699_4411804075523543893_n.png" width="212"/>
</p>
<p align="center">Wally's animation progression from sketch to sprite</p>

---

## 🎮 Controls

| Key               | Action                                     |
| ----------------- | ------------------------------------------ |
| `Q`               | Throw trash into **Biodegradable Bin**     |
| `E`               | Throw trash into **Non-Biodegradable Bin** |
| `← (Left Arrow)`  | Move Wally **Left**                        |
| `→ (Right Arrow)` | Move Wally **Right**                       |

---

## 🔥 Firebase-Powered Leaderboard

### Features:

- Real-time global rankings
- Secure score validation
- Personal progress tracking
- Daily/weekly challenges

---

## 🧩 Game Overview

<p align="justify">
Dumpster Dash is a 2D side-scrolling game built with Python and Pygame where players control Wally Waste, sorting trash into the correct bins (biodegradable/non-biodegradable) while running through DumpVania. The enhanced version includes Firebase integration for global leaderboards and real-time score tracking.
</p>

<p align="justify">
The game implements several core classes: The `Runner` class handles Wally's movement and animations, while `Bio` and `NonBio` manage the bin mechanics. Trash objects use `Garbage`, `BioGarbage`, and `NonBioGarbage` classes to randomize lane and type.  
</p>

<p align="justify">
Game flow is divided into three states: `MainMenu` (UI navigation + Firebase login), `Game` (gameplay loop + automatic score upload), and `GameOver` (shows personal bests and leaderboard). The game loop handles input, collision detection, and background scrolling while maintaining Firebase connectivity.
</p>

---

## 📊 Class Diagram

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash-SoftEng/blob/main/images/classdiagram.png" width="848"/>
</p>

---

## 📊 Sequence Diagram

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash-SoftEng/blob/main/images/sequencediagram.png" width="848"/>
</p>

---

## 🛠️ Installation Guide

### 1. 📦 Create a Virtual Environment

```bash
python -m venv .venv
```

### 2. 💡 Switch to the Main Python Interpreter

Ensure your interpreter is set to the **main Python interpreter**.

### 3. 📄 Install Initial Dependencies

```bash
pip install -r requirements.txt
```

⚠️ This may overwrite your `requirements.txt` to fit your virtual environment.

### 4. 🚀 Activate the Virtual Environment

**On Windows:**

```bash
.venv\Scripts\activate
```

**On macOS/Linux:**

```bash
source .venv/bin/activate
```

### 5. 🧰 Install setuptools (Inside Virtual Environment)

```bash
python -m pip install setuptools
```

### 6. 📥 Finalize Dependency Installation

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 Development Team

| [<img src="https://github.com/leaurix.png" width="100" alt="Louis Yvan"/>](https://github.com/leaurix) | [<img src="https://github.com/alyssaml.png" width="100" alt="Alessandra"/>](https://github.com/alyssaml) | [<img src="https://github.com/trey020304.png" width="100" alt="Trevor"/>](https://github.com/trey020304) | [<img src="https://github.com/kebinmirabel.png" width="100" alt="Kevin"/>](https://github.com/kebinmirabel) | [<img src="https://github.com/kmatheuu.png" width="100" alt="Karl"/>](https://github.com/kmatheuu) | [<img src="https://github.com/marieemoiselle.png" width="100" alt="Ma'am Fatima"/>](https://github.com/marieemoiselle) |
| :----------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------: |
|                                [Louis Yvan](https://github.com/leaurix)                                |                                [Alessandra](https://github.com/alyssaml)                                 |                                 [Trevor](https://github.com/trey020304)                                  |                                  [Kevin](https://github.com/kebinmirabel)                                   |                                [Karl](https://github.com/kmatheuu)                                 |                         [Ma'am Fatima (Course Instructor)](https://github.com/marieemoiselle)                          |

---

## 🙏 Acknowledgement

<p align="justify">
We would like to express our profound appreciation to our course instructor, <strong>Ms. Fatima Marie P. Agdon</strong>, for her invaluable advice and assistance throughout the development of Dumpster Dash. Her guidance greatly contributed to the success of this project.
</p>

<p align="justify">
We also extend our gratitude to our dedicated team members for their collaborative effort and creative input:
</p>

<ul>
    <li>Alcayde, Louis Yvan C.</li>
    <li>Landicho, Alessandra Marie M.</li>
    <li>Marcos, Mark Wilhelm Trevor K.</li>
    <li>Mirabel, Kevin Hans Aurick S.</li>
    <li>Mojar, Karl Mathew D.</li>
</ul>

<p align="justify">
This project has been a valuable experience in teamwork and interdisciplinary collaboration, and we are thankful for the opportunity to learn and grow together.
</p>

## 🌍 Play Now & Help Save the Planet! ♻️🚮
