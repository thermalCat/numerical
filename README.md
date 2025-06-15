# numerical
The subject of numerical modelling came up recently, which reminded me of a physics laboratory exercise (going back to about 1994 here!) which was an introduction to using numerical methods. The theme was a Restricted 3 body problem - earth, moon and spaceship.

With this project I'll recreate & revisit as much of the task as I can, and as a bonus I'll test drive some of the AI code tools everyone's banging on about.

I've selected [CoPilot](https://copilot.microsoft.com/) for a chatbot and [GitHub-CoPilot](https://github.com/features/copilot)  as an AI Coding Assistant, as it integrates easily into VS-Code. 

## First thoughts on CoPilot:
### Some things it will give you without a struggle:
A function that generates a Taylor series of trajectory points for the spaceship.
Code that terminates the series in the event of collision with either body.
### Some crucial things it would just cheerfully omit unless you mention them:
>Er, shouldn't the earth and moon be moving?

Copilot acknowledges the omission, and gives the moon a circular orbit, with the correct period. 
### Some things would be gotchas if you weren't paying attention:
>Don't the Earth & moon rotate about a barywotsit?

Copilot gives a description of the effect, a nice illustration, and a corresponding equation of motion for the earth.
![th](https://github.com/user-attachments/assets/1977c507-e3f2-4d1f-b633-350bd924db27)

Unfortunately, it neglects to mention that the path of the moon needs to be updated accordingly. The origin of the plot has moved from the centre of the earth to the earth-moon barycentre.

I suspect this is one of the main risks in 'vibe coding': New code is rendered up by AI without due care of side effects on the code already written. I should (sooner rather than later) ask it to suggest some unit / regression tests.

### Just occasionally a pearl of wisdom will appear unnanounced:
I noticed that gravitational forces had a factor $r/r^3$ instead the expected $1/r^2$.
This is a neat trick which avoids losing the direction information when squaring the vector r (more to follow)
