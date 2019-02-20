var item_cart = [];
    function display_item_cart(){
        var ordered_items_list=document.getElementById("ordered_items_list");
        //ensure we delete all previously added rows from ordered products table
        while(ordered_items_list.rows.length>0) {
            ordered_items_list.deleteRow(0);
        }
         //iterate over array of objects
        for(var items in item_cart){
            //add new row
            var row=ordered_items_list.insertRow();
            //create two cells for product properties
            var cellId=row.insertCell(0)
            var cellName = row.insertCell(1);
            var cellQuantity = row.insertCell(2);
            //fill cells with values from current product object of our array
            cellId.innerHTML=item_cart[items].Id;
            cellName.innerHTML = item_cart[items].Name;
            cellQuantity.innerHTML = item_cart[items].Quantity;
              if (item_cart[items].Id==cellId)
                {

                alert('This item is already exits')
                return
                }

        }
    }

    function AddtoCart(id,name,quantity){
       //Below we create JavaScript Object that will hold two properties you have mentioned:    Name,Quantity
       var singleProduct = {};
       //Fill the product object with data
       singleProduct.Id=id
       singleProduct.Name=name;
       singleProduct.Quantity=quantity;


       //Add newly created product to our shopping cart
       item_cart.push(singleProduct);
       //call display function to show on screen
       display_item_cart();

    }



    function myFunction() {
        document.getElementById("myNumber").stepUp();
        }
    function myFunction1() {
    document.getElementById("myNumber").stepDown();
        }





