$(document).ready(function(){
    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    
    function displaySubmitting(submitBtn, text, doSubmit){
        if(doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i>Enviando")
        }
        else{
            submitBtn.removeClass("disabled")
            submitBtn.html(text)
        }
    }
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                thisForm[0].reset()
                $.alert({
                    title:"Enviado",
                    content:data.message,
                    theme:"modern"
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
                },500)
            },
            error: function(error){
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function(key,value){
                    msg += key+": "+value[0].message+"<br>"
                })
                $.alert({
                    title:"Error!",
                    content: msg,
                    theme: "modern"
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
                },500)
            }
        })
    })
    // auto search
    var  searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") //input name="q"
    var typingTimer;
    var typingInterval=500 //.5 segundos
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        clearTimeout(typingTimer)
        searchBtn.addClass('disabled')
        searchBtn.html("<i class='fas fa-spin fa-spinner'></i> Buscando...")
       typingTimer = setTimeout(perfomSearch,typingInterval)
    })

    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
    })

    function perfomSearch(){
        
        var query = searchInput.val()
        window.location.href="/search/?q="+query
    }

    // agregar, quitar productos
    var productForm = $(".form-product-ajax");
    productForm.submit(function(e){
        e.preventDefault();
        console.log("Form is not sending")
        var thisForm = $(this);
        // var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint")
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url:actionEndpoint,
            method:httpMethod,
            data:formData,
            success:function(data){
                console.log("success");
                console.log(data);
                console.log("Added",data.added);
                console.log("Removed",data.removed);
                var submitSpan = thisForm.find(".submit-span");
                if (data.added) {
                    submitSpan.html('In Cart <button type="submit" class="btn btn-link">Remove</button>')
                }else{
                    submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>')
                }
                var navbarCount = $("#navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                if (window.location.href.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Error",
                    content: "Ocurrio un error al procesar la petición"
                })
                console.log("error");
                console.log(errordata)
            }
        })
    });

    function refreshCart(){
        console.log("in current cart");
        var cartTable = $(".cart-table");
        var cartBody = cartTable.find(".cart-body");

        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        // productRows.html("")
        // cartBody.html("<h1>Changed</h1>");

        var refreshCartUrl = "/api/cart/";
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url:refreshCartUrl,
            method:refreshCartMethod,
            data:data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                console.log("success");
                if (data.products.length > 0) {
                    productRows.html("");
                    i = data.products.length
                    $.each(data.products, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display","block")
                        // newCartItemRemove.removeClass("hidden-class")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">"+ i +"</th><td><a href='"+value.url+"''>"+
                            value.name+"</a>"+newCartItemRemove.html()+"</td><td>"+value.price+"</td></tr>")
                        i--
                    })
                    cartBody.find("#cart-subtotal").text(data.subtotal);
                    cartBody.find("#cart-total").text(data.total);
                    window.location.href = currentUrl
                }
                else{
                    window.location.href = currentUrl
                }
                console.log(data)
            },
            error:function(error){
                alert("an error ocurred")
                console.log("error");
                console.log(error);
            }
        })
    }
})