# numerical
![Figure_1](https://github.com/user-attachments/assets/293c51bc-4948-427f-a6dc-efa73a1342fe)


The subject of numerical modelling came up recently, which reminded me of a physics laboratory exercise (going back to about 1994 here!) which was an introduction to using numerical methods. The theme was a Restricted 3 body problem - earth, moon and spaceship.

With this project I'll recreate & revisit as much of the task as I can, and as a bonus I'll test drive some of the AI code tools everyone's banging on about.

The code is contained within a single file: [taylor.py](taylor.py) which is run without any parameters, as it stands.
Dependancies are numpy 1.21.2 and matplotlib 3.4.3

I've selected [CoPilot](https://copilot.microsoft.com/) for a chatbot and [GitHub-CoPilot](https://github.com/features/copilot)  as an AI Coding Assistant, as it integrates easily into VS-Code. For brevity, I'll refer to these as Copilot and GitHub-AI respectively.

## First thoughts on CoPilot
### Some things it will give you without a struggle
A function that generates a Taylor series of trajectory points for the spaceship.
Code that terminates the series in the event of collision with either body.
### Some crucial things it would just cheerfully omit unless you mention them
>Er, shouldn't the earth and moon be moving?

Copilot acknowledges the omission, and gives the moon a circular orbit, with the correct period. 

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

### Quirks and Errors
Whilst refactoring the code from a simple 'stationary earth' model to account for motion around the barycentre, GitHub Copilot started suggesting lines of code : positions and angular speeds for the earth & moon, etc. Unfortunately, it never seemed to be content with the results: spitting out incorrect calculations (different angular speeds for the two bodies) and repeating lines of code.
After some head scratching I realised that earth & moon should have the same angular velocities, but travel in antiphase.
To be fair, when I pointed this out, the AI agreed and provided a correction.

One area that seems to be lacking in AI is humility! Sam Altman famously quiped that users typing please & thankyou had added many millions to OpenAI's electricity bills. Concepts like apology would of course be add to that waste. I can, however see value in curating a dedicated 'oops' database, from which more careful & reliable models could be developed. I would wager that a good deal of what makes human engineers trustworthy is that we apply a higher weighting to our mistakes, which are a source of embarassment, than to our successes, which we tend to take for granted.

# Possible Improvements & Next step
Asking AI to write a test suite seems the obvious next step. This seems already pretty common in AI workflows, I've already seen people on LinkedIn recommending it.
