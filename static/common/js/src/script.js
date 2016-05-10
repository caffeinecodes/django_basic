var base_url = window.location.protocol+'//'+window.location.hostname;

var requestHelper = {

    simpleAjax : function(url,method,data,callback){
        var ajax_data = {
            'url':url,
            'type':method,
            'data':data,
            'success':function(response){
                if(typeof callback!='undefined' && response){
                    callback(response)

                }
            }
        }

        var csrf_token = requestHelper.getCookie('csrftoken');
        if(csrf_token!=''){
            ajax_data['beforeSend'] = function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }

        $.ajax(ajax_data)
    },
    
    ajaxTokenAuth : function(url,method,data,token,callback){

        var csrf_token = requestHelper.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':JSON.stringify(data),
            'contentType':'application/json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response,status,xhr){
                if(typeof callback!='undefined' && response){
                    callback(response)
                }
            },
            error: function(response,status,error){
                if(response.status==401){
                    requestHelper.ajax(url,method,data,callback,'expired')
                }

            }

      
        })
    },
    ajaxTokenAuthFile : function(url,method,data,token,callback){

        var csrf_token = requestHelper.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':data,
            'contentType':false,
            'processData':false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response){
                if(typeof callback!='undefined' && response){
                    callback(response)
                }

            },
            error: function(response,status,error){
                if(response.status==401){
                    requestHelper.ajaxFiles(url,method,data,callback,'expired')
                }

            }
        })
    },

    getCookie : function(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    ajax : function(url,method,data,callback,type){
        var token = localStorage.getItem('jwt_token')
        if(token=='' || type=='expired'){
            requestHelper.ajaxHandler(base_url+'/accounts/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                requestHelper.ajaxTokenAuth(url,method,data,response.token,callback)
            })
        }
        else{
           requestHelper.ajaxTokenAuth(url,method,data,token,callback)
        }
    },

    ajaxFiles : function(url,method,data,callback,type){
        var token = localStorage.getItem('jwt_token')
        if(token=='' || type=='expired'){
            requestHelper.ajaxHandler(base_url+'/accounts/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                requestHelper.ajaxTokenAuthFile(url,method,data,response.token,callback)
            })
        }
        else{
           requestHelper.ajaxTokenAuthFile(url,method,data,token,callback)
        }
    },

}





