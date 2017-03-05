$('#submit').click(function() {
  if ($('#article').val()) {
    $('#article_submit').submit();
  }
  setTimeout(function() {
    $('.container').addClass('fadeOutLeft animated');
  }, 500);
  setTimeout(function() {
    $('body').css('overflow', 'hidden');
    $('.container').removeClass('fadeOutLeft');
    $('.container').removeClass('animated');
    $('.container').html('<section><div><h2 id="loading">Analyzing Your Article</h2></div></section>');
    $('.container').addClass('fadeInRight animated');
  }, 1500);
  setTimeout(function() {
    $('body').css('overflow', 'auto');
    i = 0;
    setInterval(function() {
      i = ++i % 4;
      $("#loading").html("Analyzing Your Article" + Array(i + 1).join("."));
    }, 500);
  }, 2500);
});
