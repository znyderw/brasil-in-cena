document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Loaded - Initializing Mobile Menu');
    const mobileBtn = document.getElementById('mobile_btn');
    const mobileMenu = document.getElementById('mobile_menu');
    const body = document.body;

    if (mobileBtn && mobileMenu) {
        console.log('Mobile elements found. Attaching listener...');
        mobileBtn.addEventListener('click', (e) => {
            console.log('Mobile button clicked');
            e.preventDefault();
            mobileBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            body.classList.toggle('menu-open');
            
            const isActive = mobileMenu.classList.contains('active');
            console.log('Menu state:', isActive ? 'Active' : 'Inactive');
        });

        // Close menu when clicking a link
        const menuLinks = mobileMenu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                console.log('Menu link clicked - Closing menu');
                mobileBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                body.classList.remove('menu-open');
            });
        });
    } else {
        console.error('Mobile menu elements not found:', { mobileBtn, mobileMenu });
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
    window.location.href = 'https:
}

function tiktok() {
    window.location.href = 'https:
}

function gmail() {
    window.location.href = 'https:
}