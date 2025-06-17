# numerical
The subject of numerical modelling came up recently, which reminded me of a physics laboratory exercise (going back to about 1994 here!) which was an introduction to using numerical methods. The theme was a Restricted 3 body problem - earth, moon and spaceship.

With this project I'll recreate & revisit as much of the task as I can, and as a bonus I'll test drive some of the AI code tools everyone's banging on about.

The code is contained within a single file: [Taylor.py](talyor.py) which is run without any parameters, as it stands.
Dependancies are numpy 1.21.2 and matplotlib 3.4.3
([RK4.py](RK4.py) shouldn't be committed yet. VSCode said it was untracked, but here it is anyway)

I've selected [CoPilot](https://copilot.microsoft.com/) for a chatbot and [GitHub-CoPilot](https://github.com/features/copilot)  as an AI Coding Assistant, as it integrates easily into VS-Code. For brevity, I'll refer to these as Copilot and GitHub-AI respectively.

## First thoughts on CoPilot
### Some things it will give you without a struggle
A function that generates a Taylor series of trajectory points for the spaceship.
Code that terminates the series in the event of collision with either body.
### Some crucial things it would just cheerfully omit unless you mention them
>Er, shouldn't the earth and moon be moving?

Copilot acknowledges the omission, and gives the moon a circular orbit, with the correct period. 
### Some things would be gotchas if you weren't paying attention
>Don't the Earth & moon rotate about a barywotsit?

Copilot gives a description of the effect, a nice illustration, and a corresponding equation of motion for the earth.
![th](https://github.com/user-attachments/assets/1977c507-e3f2-4d1f-b633-350bd924db27)

Unfortunately, it neglects to mention that the path of the moon needs to be updated accordingly. The origin of the plot has moved from the centre of the earth to the earth-moon barycentre.

I suspect this is one of the main risks in 'vibe coding': New code is rendered up by AI without due care of side effects on the code already written. I should (sooner rather than later) ask it to suggest some unit / regression tests.

### Just occasionally a pearl of wisdom will appear unnanounced:
I noticed that gravitational forces had a factor $\vec{ r } \div \vec{ r }^3$ instead the expected $1 \div \vec{r}^2$.
This is a neat trick which avoids losing the direction information when squaring the vector r. I have, in the past, solved similar problems by calculating magnitude & direction seperately and then reconstructing the vector. This is elegant in a good way: the simple & obvious kind, not the showing off kind.

## First thoughts on github AI autocomplete
Intelisense on steroids.

### When it works, it is really effective 
The collision detection block initially lumped all collisions together.
AI spotted that I was about to seperate them out (no more prompting required than pressing return half way along the IF ... OR ... statement) and did the rest for me.

### Echoes poor / undisciplined coding practices
once you start some task, it may well recognise the aim and start suggesting lines of code.
Unless you have a good mental picture of what completion looks like, this can end up something like hacking - hacking by proxy? Don't rely on the AI to know when it has finished either!

Whilst refactoring the code from a simple 'stationary earth' model to account for motion around the barycentre, GitHub Copilot started suggesting lines of code : positions and angular speeds for the earth & moon, etc. Unfortunately, it never seemed to be content with the results: spitting out incorrect calculations (different angular speeds) and repeating lines of code.
After some head scratching I realised that earth & moon should have the same angular velocities, but travel in antiphase.
To be fair, when I pointed this out, the AI agreed and provided a correction.

One area that seems to be lacking in AI is humility! It does not say oops, or sorry. Worse still nobody seems to collect a dedicated 'oops' dataset, from which more careful & reliable models could be developed.
I would wager that a good deal of what makes human engineers trustworthy is that we apply a higher weighting to our mistakes, which are a source of embarassment, than to our successes, which we tend to take for granted.
