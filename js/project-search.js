document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('project-search');
    const blocks = document.querySelectorAll('.project-block');
  
    input.addEventListener('input', () => {
      const query = input.value.toLowerCase();
  
      blocks.forEach(block => {
        const title = block.dataset.title;
        const authors = block.dataset.authors;
        const tags = block.dataset.tags;
  
        const matches =
          title.includes(query) ||
          authors.includes(query) ||
          tags.includes(query);
  
        block.style.display = matches ? '' : 'none';
      });
    });
  });
  