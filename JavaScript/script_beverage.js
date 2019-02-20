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
            //create three cells for product properties
            var cellName = row.insertCell(0);
            var cellQuantity = row.insertCell(1);
            //fill cells with values from current product object of our array
            cellName.innerHTML = item_cart[items].Name;
            cellQuantity.innerHTML = item_cart[items].Quantity;

        }

    }


    function AddtoCart(name,quantity){
       //Below we create JavaScript Object that will hold three properties you have mentioned:    Name,Description
       var singleProduct = {};
       //Fill the product object with data
       singleProduct.Name=name;
       singleProduct.Quantity=quantity;

       //Add newly created product to our shopping cart
       item_cart.push(singleProduct);
       //call display function to show on screen
       display_item_cart();

    }






