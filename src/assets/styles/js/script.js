document.addEventListener('DOMContentLoaded', () => {
    const mobileBtn = document.getElementById('mobile_btn');
    const mobileMenu = document.getElementById('mobile_menu');
    const body = document.body;

    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.preventDefault();
            mobileBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            body.classList.toggle('menu-open');
        });

        const menuLinks = mobileMenu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                body.classList.remove('menu-open');
            });
        });
    }

    if (typeof ScrollReveal !== 'undefined') {
        ScrollReveal().reveal('#cta', { origin: 'left', duration: 2000, distance: '20%' });
        ScrollReveal().reveal('#br', { origin: 'right', duration: 2000, distance: '20%' });
        ScrollReveal().reveal('#nos', { origin: 'right', duration: 2000, distance: '20%' });
        ScrollReveal().reveal('.dish', { origin: 'left', duration: 2000, distance: '20%' });
        ScrollReveal().reveal('#contato', { origin: 'left', duration: 1000, distance: '20%' });
    }
});

function instagram() {
    window.location.href = 'https://www.instagram.com/brasilincena_?igsh=cWczMTN2b2JhODBk&utm_source=qr';
}

function gmail() {
    window.location.href = 'mailto:brasilincena@gmail.com';
}