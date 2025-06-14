# numerical
The subject of numerical modelling came up recently, which reminded me of a physics laboratory exercise (going back to about 1994 here!) which was an introduction to using numerical methods. The theme was a Restricted 3 body problem - earth, moon and spaceship.

With this project I'll recreate & revisit as much of the task as I can, and as a bonus I'll test drive some of the AI code tools everyone's banging on about.

I've selected Copilot for text prompt and GitHub-free which integrates easily with VS-Code. 

First thoughts on Copilot text prompt:
Some things it will give you without a struggle:
A function that generates a Taylor series of trajectory points for the spaceship.
Code that terminates the series in the event of collision with either body.
Some crucial things it would just cheerfully omit unless you mention them:
Er, shouldn't the earth and moon be moving?
Copilot gives the moon a circular orbit, with the correct period. 

Some things would be gotchas if you weren't paying attention:
Don't the Earth & moon rotate about a barywotsit?
Copilot gives a description of the effect, a nice illustration, and a corresponding equation of motion for the earth.
Unfortunately, it neglects to mention that the path of the moon needs to be updated to account for what is effectively a change in the frame of reference.
