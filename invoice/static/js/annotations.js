function call(vals) {
   $.ajax({
       type: "POST",
       url: "test",
       data: { csrfmiddlewaretoken: '{{ csrf_token }}',
        vals:vals},
       success: function () {
            console.log('success')
       }
   })
}


function annote() {
var anno = Annotorious.init({
  image: 'the-canvas',
  locale: 'auto',
});

anno.on('selectAnnotation', function(annotation) {
    anno.removeAnnotation(annotation.id)
  console.log('selected', annotation);
});

anno.on('createAnnotation', function(a) {
    var vals = a.target.selector.value
    console.log('created', vals);
    call(vals)
});

anno.on('updateAnnotation', function(annotation, previous) {
  console.log('updated', previous, 'with', annotation);
});

anno.on('deleteAnnotation', function(annotation) {
  console.log('deleted', annotation);
});

anno.loadAnnotations("annotorious.w3c.json");

return anno
}

annote()
