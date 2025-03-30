document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('blog-search');
    const cards = document.querySelectorAll('.card');
  
    input.addEventListener('input', () => {
      const query = input.value.toLowerCase();
  
      cards.forEach(card => {
        const title = card.dataset.title;
        const desc = card.dataset.desc;
        const tags = card.dataset.tags;
  
        const matches =
          title.includes(query) ||
          desc.includes(query) ||
          tags.includes(query);
  
        card.style.display = matches ? '' : 'none';
      });
    });
  });
  