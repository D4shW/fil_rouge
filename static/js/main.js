document.addEventListener('DOMContentLoaded', () => {

    // ─── Navbar scroll ───────────────────────────
    const nav = document.getElementById('mainNav');
    window.addEventListener('scroll', () => {
        nav.classList.toggle('nav--scrolled', window.scrollY > 50);
    });

    // ─── Mobile burger ───────────────────────────
    const burger = document.getElementById('navBurger');
    const mobile = document.getElementById('navMobile');
    if (burger && mobile) {
        burger.addEventListener('click', () => mobile.classList.toggle('open'));
    }

    // ─── Auto-dismiss flash ──────────────────────
    document.querySelectorAll('.flash').forEach(flash => {
        setTimeout(() => {
            flash.style.transition = 'all 0.4s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(30px)';
            setTimeout(() => flash.remove(), 400);
        }, 4500);
    });

    // ─── Scroll reveal ───────────────────────────
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.service-card, .agence-card, .why-card, .form-page').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(25px)';
        el.style.transition = `all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) ${i * 0.05}s`;
        observer.observe(el);
    });

    // ─── Add-to-cart feedback ────────────────────
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function () {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.textContent = '✓ Ajouté au devis';
                btn.style.background = 'var(--green)';
                btn.style.borderColor = 'var(--green)';
                btn.style.color = '#fff';
            }
        });
    });
});
