<!DOCTYPE html>
<html>
<body>


<button onclick="myFunction1('Coffee')">Add to cart</button>
<button onclick="myFunction3()">-</button>
<input type="number" id="myNumber">

<button onclick="myFunction2()">+</button>

<p id="demo"></p>

<script>
function myFunction1(name) {
 document.getElementById("demo").innerHTML =   name ;
}
function myFunction2() {
 document.getElementById("myNumber").stepUp();
}
function myFunction3() {
 document.getElementById("myNumber").stepDown();
}

</script>

</body>
</html>
