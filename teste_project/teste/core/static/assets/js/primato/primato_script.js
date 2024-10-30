setTimeout(function(){
    swal({
        title: "Sua sessão expirou.",
        text: "Faça login novamente para acessar o sistema.",
        icon : "info",
	    buttons: {
		    confirm: {
			    className : 'btn btn-info'
		        }
	        },
        })
    .then(
        function(){location.reload();}
        );
    } ,1000 * 60 * 30 ); //30 MINUTES

