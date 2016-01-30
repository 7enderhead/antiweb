/* @start(__macros__)
@define(Code)
@if(show)
The source can be found in @subst(__file__) at line @subst(__line__):
@code
@fi(show)
@if(noshow)

.. 
@indent +4
@fi(noshow)
@enifed(Code)

@start()
The Main function ist the first one.
@subst(Code)*/

void main() {

}

