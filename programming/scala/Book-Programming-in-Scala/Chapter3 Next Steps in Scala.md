# Next Steps in Scala

### Array, List and Tuple

It is to be said in the book that 

* Array vs List, Array is mutable and List is immutable
* List vs Tuple, List is homogenous (which contains variable of the same data type) and Tuple can be heterogenous (variables of different data types)

There are two catches.

Example 1:

```scala
// this compiles
val strList = List("One","Two",3)
```

why ? Isn't "One" of type java.lang.String and 3 of type java.lang.Int ? The reason is through type inference the List variable strList is inferenced as type List[Any], here both "One" and 3 are of type Any. [Futher reading here](https://stackoverflow.com/questions/14664822/types-of-objects-in-scalas-lists)

If you specify the type of strList explicitly (One of usage of explict type information), the compilation will fail

```scala
// this does not compile
// error message like: Found:    (3 : Int) Required: String
val strList: List[String] = List("One","Two",3)
```

Example 2:

```scala
// TODO: the intention of this example is to change the content of intArray here by changing the referenced object instead of the reference itself, even Array is not "mutable"
var a1 = 1
var a2 = 2
var a3 = 3

val intArray: Array[Int] = Array(a1,a2,a3)
intArray.foreach(x => println(x))

a3 = 4

intArray.foreach(x => println(x))
```