<p align="center">
    <img src="https://github.com/trey020304/test-repository/blob/main/images/logo%202.jpg" width=512px height=512px/>
</p>

___

# 🎮 What is the game about? 🎮

<p align="justify">
DumpsterDash is heavily inspired by the infamous game, Subway Surfers, which plays out as an endless running game that embodies the importance of segragation. The mechanic of the game is to continuously collect garbage with accordance to the specific garbage bins that Wally Waste (our mascot!) is holding, whether it may be biodegradable and non-biodegradable. And just like any other endless running games, the objective is to collect as many points as you can by collecting the trash with the right specific trash bin on hand while running through the streets of DumpVania! 🤖♻️
</p>

<p align="center">
    <img src="https://github.com/trey020304/test-repository/blob/main/images/wally%20waste%202.png" width=250px/>
</p>
                                                                                                              
<p align="center">
This is Wally Waste, the cleaning robot!
</p>

___

## ♻️ Significance of the Game ♻️

<img src="https://github.com/trey020304/test-repository/blob/main/images/E-WEB-Goal-12.png" align=left width=212px/>

<p align="justify">
According to the 12th goal under the Sustainable Development Goals, it involves establishing sustainable production and consumption habits, which are essential to maintaining the standard of living for both the present and future generations. It calls for more effective and environmentally responsible management of materials throughout their whole lifecycle, from manufacture to disposal. With DumpsterDash's existence, this would not only serve as a fun application but would also raise awareness of the status of our world today in terms of how sustainability and correct segregation of waste is being handled. Since the majority of people play video games on their devices, this game would be helpful in spreading awareness of the 12th Sustainable Development Goal as it would be accessible to practically all age groups and almost anyone with a gadget would be able to play this game!
</p>

<img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/E_SDG-goals_icons-individual-rgb-15-500x500.jpg" align=left width=212px/>

<p align="justify">
For our food and means of subsistence, human existence depends just as much on the ground as it does the ocean. Eighty percent of the human diet is made up of plants, and agriculture is a significant source of income for us. Providing habitat for millions of species, significant sources of clean air and water, and being essential for preventing climate change, forests encompass 30% of the Earth's surface. And trash, or improper rubbish segregation, is one of the elements that ruins animal habitats. Because when we scatter our rubbish around, some little creatures end up eating it and becoming ill or occasionally even perish. Our program is in line with this objective since we want to educate people about the value of segregation and how to accomplish it, as well as the effects that waste we simply put into the environment can have.
</p>


___

## 😎 Future Plans for the Game 😎

- Multiple skins of Wally Waste (that can be bought with microtransactions or in-game currency that can be collected from playing)
- Multiple game modes!
- Multi-platform! Mobile, consoles, etc.!

___

<p align="center"> Screenshots and Some Visual Concepts </p>

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/341477161_1250051515632988_5368769938844971349_n.jpg" width=212px/>
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/346149733_1056012145373168_2721184389200773529_n.jpg" width=212px/>
</p>
    
<p align="center">
    Early Design of Wally 🤖♻️
</p>

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/346134559_808486404179534_5777925480861872611_n.png" width=424px/>
</p>

<p align="center">
    Early Design of the Background 🌳
</p>

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/335428268_1526468007762830_3256599577823479950_n.png" width=212px/>
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/349222251_118642044568040_6257362520514358034_n.gif" width=212px/>         
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/348901030_1296695137890699_4411804075523543893_n.png" width=212px/>
</p>

<p align="center">
    Early Animation Sprites of Wally 🤖♻️
</p>

___

## Overview of Dumpster Dash and the Program

<p align="justify">
Python and the Pygame library were used in the creation of the video game "Dumpster Dash". The player plays a man named "Wally" in this 2D side-scrolling game who must gather garbage from the side of the road with the appropriate sort of bin for each piece of trash that it passes, avoiding catching trash with the incorrect type of bin. The goal of this game is to attain the highest score by collecting garbage with the right corresponding bin.
</p>

<p align="justify">
For various game elements, the program defines a number of classes. Logos are displayed on screens using the "Logo" class. The player-controlled character "Wally" has a base class called "Runner", which has methods for updating its animation frames and dealing with collisions with garbage objects. The "Bio" and "NonBio" classes, which represent various iterations of the player character, derive from the Runner class. "Garbage", "BioGarbage", and "NonBioGarbage" classes are only a few examples of the classes for garbage objects that the program defines. These classes are used to construct instances of garbage objects that drop from the top of the screen and inherit from the pygame.sprite.Sprite class. The software generates fresh instances of garbage objects by randomly choosing a lane and garbage type, whether it is biodegradable or not.
</p>

<p align="justify">
Classes like "MainMenu", "Game", and "GameOver" are used to define the different game states. The play and quit buttons' mouse button clicks are handled by the MainMenu class, which also shows on the main menu screen. The primary gameplay state, in which the user controls Wally and attempts to catch garbage with the right corresponding bin, is represented by the Game class. The game over screen, the player's score, and the highest score they've ever gotten are all displayed by the GameOver class, as well as the restart and main menu buttons. The program uses a game loop that continuously updates and redraws the game elements on the screen. It handles user input events, such as key presses and mouse clicks, and updates the game state accordingly. It also handles the scrolling background by updating the positions of the background images.
</p>


___

## UML Diagram of Dumpster Dash

<p align="center">
    <img src="https://github.com/trey020304/Dumpster-Dash/blob/main/images/UML%20class.jpeg" width=848px/>
</p>


___


## Video Presentation of Dumpster Dash and the Program
- <a href="https://www.youtube.com/watch?v=JnIWZd-0lYs">Game Demo</a>
- <a href="https://youtu.be/VXk6wL1Rw1Y">Presentation</a>

___


## Authors

- <a href="https://github.com/trey020304">Marcos, Mark Wilhelm Trevor</a>
- <a href="https://github.com/kebinmirabel">Mirabel, Kevin Hans Aurick</a>
- <a href="https://github.com/JulyanGarcia">Garcia, Julian Simon</a>
- <a href="https://github.com/Ronnieee1">Del Mundo, Ron Gabriel</a>
