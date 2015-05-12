/* @start(__macros__)

@define(s1, One Line 1)
@define(s2, One Line 2)

@start()

Main text @subst(s1), @subst(s2), @subst(__line__+3)

@include(sub text)

@*/


/* @start(sub text) 

Include subtext block

@*/
