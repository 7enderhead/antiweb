/* @start(__macros__)

@define(Code)
This code can be found in @subst(__file__) at line @subst(__line__+2)
@code
@enifed(Code)


@start()

Main text 

@include(sub text)

@*/


/* @start(sub text) 

Include subtext block

@subst(Code)*/

void main() {
  int i = 0;

  for(i = 0; i < 1000; i++);
}

