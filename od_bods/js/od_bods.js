
$(document).ready(function(){

    $('#load_data').click(function(){

        $.ajax

            url:"odmods.csv",

            datatype: "text",

            Success:function(data)

            {

                var odmods_data = data.split(/\r?\n|\r/);

                var table_data = '<table class="table-bordered table-striped">;

                for(var count = 0, count<od_bods_data.length; count++)

                {
 
                    if(count === 0)

                    {

                        table_data += '<th>'+cell_data[cell_count]+'</th>';

                    }

                    else

                    {

                        table_data += '<td>'+cell_data[cell_count]+'</td>';

                    }

                }

                table_data += '</tr>';

                }

            }

            table_data += '</table>';
            $('#od_bods_table').html(table_data)


            }             


        });


    });


});