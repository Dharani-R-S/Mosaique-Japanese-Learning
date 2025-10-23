// main.js - small helpers for play buttons and simple waveform animation
document.addEventListener('DOMContentLoaded', function() {
  const audio = document.getElementById('global-audio');
  if (!audio) return;

  function animateWave(el) {
    el.classList.add('playing');
  }
  function stopWave(el) {
    el.classList.remove('playing');
  }

  document.querySelectorAll('.btn-play').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const src = btn.getAttribute('data-audio-src');
      const container = btn.closest('.bg-white');
      const wave = container ? container.querySelector('.wave') : null;

      if (!src) {
        btn.classList.add('opacity-80');
        setTimeout(()=> btn.classList.remove('opacity-80'), 200);
        return;
      }

      // normalize full URL if necessary (browser will resolve)
      if (audio.src !== src) {
        audio.src = src;
      }

      if (audio.paused) {
        audio.play().then(()=> {
          // update all play buttons to "Play" then this one to "Pause"
          document.querySelectorAll('.btn-play').forEach(b => b.textContent = 'Play');
          btn.textContent = 'Pause';
          if (wave) animateWave(wave);
        }).catch((err)=> {
          console.warn('Audio play failed:', err);
        });
      } else {
        audio.pause();
        btn.textContent = 'Play';
        if (wave) stopWave(wave);
      }

      audio.onended = function() {
        document.querySelectorAll('.btn-play').forEach(b => b.textContent = 'Play');
        if (wave) stopWave(wave);
      };
    });
  });
});
