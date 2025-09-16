# SleepCycle Art: A Markov Model of Sleep Stages

## Overview
This project simulates human sleep cycles using a **Markov chain** and then visualizes the results in two ways:

1. **Graph Plot**: a timeline graph showing the sequence of sleep stages (Awake, Light, Deep, REM) over an 8-hour night, broken into 5-minute epochs.  
2. **Abstract Art**: a creative rendering where each epoch is represented as a shape and color (e.g., REM as a magenta triangle, Deep as a dark blue diamond). The final output is a piece of abstract art that encodes the sleep journey.

The system is implemented in Python using **NumPy** for simulation, **Matplotlib** for visualization, and **matplotlib.patches** for shape drawing.


Describe how the system is personally meaningful to you (at least 1 paragraph).

This system is personally meaningful to me because I am a big proponent of sleep. I can always sleep at least 10 hours and no matter how many hours I slept the night before, I can always find a way to nap. I find sleeping so important because it is how you heal your body, prevent sickness, and get the mind ready to learn more! For this project I thought it would be interesting to create a system that not only tracks your sleep graphically, similar to what we did in class, but also produced a somewhat "abstract" piece of art to depict the kind of sleep you had. Sleep is something we all experience, yet we rarely visualize it in creative ways. I often think about how much of our lives happen unconsciously while we sleep, and turning those hidden rhythms into visible art feels both personal and poetic. The abstract art gives me a way to “see” what an ordinary night might look like if it were expressed visually, blending scientific modeling with creative representation. By turning something deeply biological into a colorful artwork, I’ve created a bridge between my interest in science and sleep!

Explain how working on it genuinely challenged you as a computer scientist (at least 1 paragraph).

Working on this project genuinely challenged me as a computer scientist. While the concept of a Markov model is straightforward in theory, implementing it in a way that produces meaningful and interpretable output required careful thought. I had to translate probabilities into code, ensure the transition matrix was valid, and debug issues where plots wouldn’t render or images didn’t save properly. More importantly, going beyond “just simulation” and pushing into visualization required me to learn new tools (like matplotlib.patches) and think about not only correctness but also aesthetics. This was more demanding than typical coding assignments because it involved combining probability, algorithm design, and visual creativity.

How did you push yourself outside of your comfort zone?

I pushed myself outside of my comfort zone by adding a visual component after my graph was created. Normally I approach coding as a logical process where the goal is accuracy. Here, the “goal” was less rigid: to make something visually striking that also encoded information. That forced me to experiment with colors, shapes, and layout in ways I hadn’t before. I also had to troubleshoot platform-specific issues with Matplotlib (like plt.show() blocking on macOS), which tested my patience and problem-solving skills. This was an important challenge because it showed me how to persevere when a project isn’t just about writing correct code but about achieving a creative output that I had to pick (one of the hardest parts was thinking about an idea in the first place)! 

Why was this an important challenge for you?

This project was an important challenge for me because it combined two domains that I don’t usually put together: probability modeling and visualization. I had to step beyond simply making a program “work” and instead think about how to design a system that was not only computationally correct but also produced something creative to showcase my work. This mattered to me because it pushed me to confront the parts of programming that feel ambiguous and subjective. Instead of knowing in advance what the “right answer” looked like, I had to trust my judgment that my final output was creative. In this project, success was about producing something that communicates an idea and sparks interpretation. That shift forced me to grow - not just as a coder, but as someone who uses code as a creative medium.

What are the next steps for you going forward?

- Make the transition probabilities time-dependent, so the model produces more REM cycles toward morning (closer to real biology).
- Add legends or annotations to the artwork so viewers can decode which colors/shapes correspond to which stages.
- Maybe correlate certain shapes and colors to the different cycles more accurately (ie. maybe red is better for awake since its not good to wake up during your sleep cycle and will cause you to be cranky in the morning).

Include a discussion of whether you believe your system is creative (and why or why not).

I believe the system is creative because it transforms structured, quantitative data into something expressive and open to interpretation. While the Markov model itself is not “creative," the decision to map sleep stages into colors and shapes and present them as abstract art is a creative act. The randomness built into the model also ensures each run generates a unique piece, so in a sense the system collaborates with me in producing the artwork.

Make sure to credit your sources, including your colleagues if you sought their advice.

Python Libraries: NumPy, Matplotlib

Sleep Stage Background: I had to look up some terms to understand the sleep stages and what an epoch was several times!

Izzy Tsuchitori: I discussed several ideas with her, but she helped spark the idea of creating something along with my graphic to show something else visually creative.

OpenAI’s ChatGPT: I utilized Chat for help with Github questions.
