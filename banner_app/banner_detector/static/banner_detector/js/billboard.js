        'use strict';

        ;( function ( document, window, index )
        {
            var billboardSendTimer;
            var billboardDisplayTimer;
            var iterations = 5;
            function SendTimer(){
                var billBoardForm = $('#billboard_form');
                try {
                    showModal();
                    billBoardForm.submit();
                }
                catch (e) {
                    console.log(e);
                }
            }

            function DisplayTimer(){
                iterations--;
                document.getElementById("billboard_timer").innerHTML = "До отправки: " + iterations;
                if (iterations <= 0){
                    for(var i=0; i<20; i++){
                        window.clearInterval(i);
                        document.getElementById("billboard_timer").style.display = 'none';
                    }
                }
            }

            function readURL(input) {
                if (input.files && input.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        $('#profile-img-tag').attr('src', e.target.result);
                    }
                    reader.readAsDataURL(input.files[0]);
                }
            }

            var inputs = document.querySelectorAll( '.inputfile-1' );
            Array.prototype.forEach.call( inputs, function( input )
            {
                var label	 = input.nextElementSibling,
                    labelVal = label.innerHTML;

                input.addEventListener('click', function(e){
                    iterations = 5;
                    if (billboardSendTimer){
                        clearTimeout(billboardSendTimer);
                    }
                    if(billboardDisplayTimer){
                        clearInterval(billboardDisplayTimer);
                    }
                    document.getElementById("billboard_timer").style.display = 'block';
                });

                input.addEventListener('change', function( e )
                {
                    billboardDisplayTimer = setInterval(DisplayTimer, 1000);
                    billboardSendTimer = setTimeout(SendTimer, 5000);
                    readURL(this);
                    var fileName = '';
                    if( this.files && this.files.length > 1 )
                        fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
                    else
                        fileName = e.target.value.split( '\\' ).pop();

                    if( fileName )
                        label.querySelector( 'span' ).innerHTML = fileName;
                    else
                        label.innerHTML = labelVal;
                });

                // Firefox bug fix
                input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
                input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
            });


        }( document, window, 0 ));