let lastScroll = 0
const nav = document.querySelector('.floating-navbar')

window.addEventListener('scroll', () => {
  const current = window.scrollY
  if (!nav) return

  if (current > 150) {
    nav.classList.add('hide')
  } else {
    nav.classList.remove('hide')
  }
})
