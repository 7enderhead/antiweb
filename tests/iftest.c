/* 
@start()
@if
Main Text

@include(sub text, simple_start_include.c)

@code*/

void main() {
  /*@rstart(complex)*/
  int i = 0;
  for(i = 0; i < 100; i++);
}

/*@edoc
<<complex>>

@include(complex)
@*/


