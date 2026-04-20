document.addEventListener('DOMContentLoaded', () => {
    const mobileBtn = document.getElementById('mobile_btn');
    if (mobileBtn) {
        mobileBtn.addEventListener('click', () => {
            const mobileMenu = document.getElementById('mobile_menu');
            if (mobileMenu) mobileMenu.classList.toggle('active');
            
            const icon = mobileBtn.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-xmark');
            }
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
    window.location.href = 'https:
}

function tiktok() {
    window.location.href = 'https:
}

function gmail() {
    window.location.href = 'https:
}