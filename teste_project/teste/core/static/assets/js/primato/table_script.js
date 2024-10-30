$(document).ready(function() {
        $('.dataTable').DataTable({
            paging: true,
            lengthChange: false,
             columnDefs: [
                {
                 orderable: false, targets: -1
                }
             ],
             info: false,
             //https://datatables.net/reference/option/language
             //https://legacy.datatables.net/usage/i18n
             oLanguage: {
                "sSearch": "Procurar:",
                "sEmptyTable": "Sem Registros",
                "oPaginate": {
                    "sFirst":"Primeiro",
                    "sLast":       "Ultimo",
                    "sNext":       "Proximo",
                    "sPrevious":   "Anterior"
                    },
                 },
         });
    });