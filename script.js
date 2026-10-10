// Draw the route once the hero map is on screen.
const map = document.querySelector('.route');
if (map) {
    new IntersectionObserver((entries, obs) => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.classList.add('drawn'); obs.unobserve(e.target); }
        });
    }, { threshold: 0.3 }).observe(map);
}

// Staggered reveal for content blocks.
const blocks = document.querySelectorAll('.head, .split > *, .steps li, .algo, .table-wrap, .foot-note, .limits li, .stats li');
blocks.forEach(el => el.classList.add('reveal'));

const revealer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const siblings = Array.from(entry.target.parentElement.children).filter(n => n.classList.contains('reveal'));
        const i = Math.max(0, siblings.indexOf(entry.target));
        entry.target.style.transitionDelay = Math.min(i * 70, 280) + 'ms';
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
    });
}, { threshold: 0.15, rootMargin: '0px 0px -40px' });

blocks.forEach(el => revealer.observe(el));

// Highlight the section currently in view.
const links = Array.from(document.querySelectorAll('.bar-nav a'));
const sections = links
    .map(a => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);

const spy = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id));
    });
}, { rootMargin: '-45% 0px -50% 0px' });

sections.forEach(s => spy.observe(s));
