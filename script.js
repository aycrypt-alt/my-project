/* ============================================
   ROMZY — Luxury Fashion E-Commerce
   ============================================ */

// --- Product Data ---
const PRODUCTS = [
    // Featured Collection
    { id: 1, name: 'Silk Wrap Dress', price: 285, salePrice: null, category: 'dresses', image: 'https://picsum.photos/400/533?random=20', description: 'An elegant silk wrap dress with a flattering silhouette. Perfect for evening occasions or refined daytime styling.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 2, name: 'Linen Oversized Blazer', price: 320, salePrice: null, category: 'tops', image: 'https://picsum.photos/400/533?random=21', description: 'A relaxed-fit linen blazer crafted from premium Italian linen. Effortless sophistication for every season.', sizes: ['XS', 'S', 'M', 'L', 'XL'] },
    { id: 3, name: 'Tailored Wide-Leg Trousers', price: 195, salePrice: null, category: 'bottoms', image: 'https://picsum.photos/400/533?random=22', description: 'High-waisted wide-leg trousers in a fluid crepe fabric. A modern staple for the discerning wardrobe.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 4, name: 'Gold Chain Necklace', price: 145, salePrice: null, category: 'accessories', image: 'https://picsum.photos/400/533?random=23', description: 'A delicate gold-plated chain necklace with an adjustable clasp. Minimalist luxury at its finest.', sizes: ['One Size'] },
    { id: 5, name: 'Cashmere Knit Top', price: 210, salePrice: null, category: 'tops', image: 'https://picsum.photos/400/533?random=24', description: 'A lightweight cashmere knit top with a relaxed fit. Luxuriously soft against the skin.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 6, name: 'Midi Pleated Skirt', price: 175, salePrice: null, category: 'bottoms', image: 'https://picsum.photos/400/533?random=25', description: 'A flowing midi skirt with delicate pleating. Moves beautifully with every step.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 7, name: 'Structured Leather Bag', price: 395, salePrice: null, category: 'accessories', image: 'https://picsum.photos/400/533?random=26', description: 'A handcrafted leather bag with clean lines and gold hardware. The ultimate everyday luxury.', sizes: ['One Size'] },
    { id: 8, name: 'Satin Evening Gown', price: 450, salePrice: null, category: 'dresses', image: 'https://picsum.photos/400/533?random=27', description: 'A floor-length satin gown with a draped neckline. Timeless elegance for special occasions.', sizes: ['XS', 'S', 'M', 'L'] },

    // New Arrivals
    { id: 9, name: 'Cropped Tweed Jacket', price: 340, salePrice: null, category: 'tops', image: 'https://picsum.photos/400/533?random=28', description: 'A cropped jacket in luxurious bouclé tweed. A modern take on a classic silhouette.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 10, name: 'Draped Jersey Dress', price: 225, salePrice: null, category: 'dresses', image: 'https://picsum.photos/400/533?random=29', description: 'A body-skimming jersey dress with elegant draping. Effortless from day to night.', sizes: ['XS', 'S', 'M', 'L', 'XL'] },
    { id: 11, name: 'Leather Belt', price: 95, salePrice: null, category: 'accessories', image: 'https://picsum.photos/400/533?random=30', description: 'A sleek leather belt with a brushed gold buckle. The finishing touch to any outfit.', sizes: ['S', 'M', 'L'] },
    { id: 12, name: 'High-Waist Straight Jeans', price: 185, salePrice: null, category: 'bottoms', image: 'https://picsum.photos/400/533?random=31', description: 'Premium denim in a high-waisted straight cut. Designed for a flattering, modern fit.', sizes: ['24', '25', '26', '27', '28', '29', '30'] },

    // Sale Items
    { id: 13, name: 'Floral Maxi Dress', price: 310, salePrice: 189, category: 'dresses', image: 'https://picsum.photos/400/533?random=32', description: 'A romantic floral maxi dress in soft chiffon. Flowing and feminine for warm-weather occasions.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 14, name: 'Cotton Poplin Shirt', price: 165, salePrice: 99, category: 'tops', image: 'https://picsum.photos/400/533?random=33', description: 'A crisp cotton poplin shirt with a relaxed oversized fit. A wardrobe essential reimagined.', sizes: ['XS', 'S', 'M', 'L', 'XL'] },
    { id: 15, name: 'Wool Blend Trousers', price: 240, salePrice: 149, category: 'bottoms', image: 'https://picsum.photos/400/533?random=34', description: 'Tailored trousers in a premium wool blend. Sharp lines and impeccable construction.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 16, name: 'Silk Scarf', price: 120, salePrice: 72, category: 'accessories', image: 'https://picsum.photos/400/533?random=35', description: 'A hand-printed silk scarf in an exclusive pattern. Versatile luxury for every season.', sizes: ['One Size'] },
    { id: 17, name: 'Ribbed Knit Dress', price: 195, salePrice: 119, category: 'dresses', image: 'https://picsum.photos/400/533?random=36', description: 'A body-conscious ribbed knit dress. Understated elegance with a modern edge.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 18, name: 'Linen Wide Pants', price: 180, salePrice: 108, category: 'bottoms', image: 'https://picsum.photos/400/533?random=37', description: 'Relaxed wide-leg pants in breathable linen. Effortless summer sophistication.', sizes: ['XS', 'S', 'M', 'L'] },
    { id: 19, name: 'Pearl Drop Earrings', price: 85, salePrice: 51, category: 'accessories', image: 'https://picsum.photos/400/533?random=38', description: 'Freshwater pearl drop earrings set in gold-plated sterling silver. Timeless and refined.', sizes: ['One Size'] },
    { id: 20, name: 'Cropped Cardigan', price: 155, salePrice: 93, category: 'tops', image: 'https://picsum.photos/400/533?random=39', description: 'A soft cropped cardigan with mother-of-pearl buttons. Cozy luxury for layering.', sizes: ['XS', 'S', 'M', 'L'] },
];

// --- DOM References ---
const dom = {
    navbar: document.getElementById('navbar'),
    announcementBar: document.getElementById('announcement-bar'),
    closeAnnouncement: document.getElementById('close-announcement'),
    cartBtn: document.getElementById('cart-btn'),
    cartSidebar: document.getElementById('cart-sidebar'),
    cartOverlay: document.getElementById('cart-overlay'),
    closeCart: document.getElementById('close-cart'),
    continueShopping: document.getElementById('continue-shopping'),
    cartItems: document.getElementById('cart-items'),
    cartEmpty: document.getElementById('cart-empty'),
    cartCount: document.getElementById('cart-count'),
    cartHeaderCount: document.getElementById('cart-header-count'),
    cartTotal: document.getElementById('cart-total'),
    cartFooter: document.getElementById('cart-footer'),
    searchBtn: document.getElementById('search-btn'),
    searchOverlay: document.getElementById('search-overlay'),
    closeSearch: document.getElementById('close-search'),
    searchInput: document.getElementById('search-input'),
    hamburgerBtn: document.getElementById('hamburger-btn'),
    mobileMenu: document.getElementById('mobile-menu'),
    closeMobileMenu: document.getElementById('close-mobile-menu'),
    quickViewOverlay: document.getElementById('quick-view-overlay'),
    closeQuickView: document.getElementById('close-quick-view'),
    qvImage: document.getElementById('qv-image'),
    qvName: document.getElementById('qv-name'),
    qvPrice: document.getElementById('qv-price'),
    qvDescription: document.getElementById('qv-description'),
    qvSize: document.getElementById('qv-size'),
    qvQty: document.getElementById('qv-qty'),
    qvQtyMinus: document.getElementById('qv-qty-minus'),
    qvQtyPlus: document.getElementById('qv-qty-plus'),
    qvAddToBag: document.getElementById('qv-add-to-bag'),
    featuredGrid: document.getElementById('featured-grid'),
    newArrivalsGrid: document.getElementById('new-arrivals-grid'),
    saleGrid: document.getElementById('sale-grid'),
    filterPills: document.getElementById('filter-pills'),
    newsletterForm: document.getElementById('newsletter-form'),
    newsletterSuccess: document.getElementById('newsletter-success'),
};

// --- Utility Functions ---
function formatPrice(amount) {
    return '$' + amount.toFixed(2);
}

function lockScroll() {
    document.body.classList.add('no-scroll');
}

function unlockScroll() {
    document.body.classList.remove('no-scroll');
}

// --- Cart Module ---
const Cart = {
    items: JSON.parse(localStorage.getItem('romzy-cart')) || [],

    save() {
        localStorage.setItem('romzy-cart', JSON.stringify(this.items));
    },

    addItem(productId, size, qty) {
        const product = PRODUCTS.find(p => p.id === productId);
        if (!product) return;
        const existing = this.items.find(item => item.productId === productId && item.size === size);
        if (existing) {
            existing.qty += qty;
        } else {
            this.items.push({ productId, size, qty });
        }
        this.save();
        this.render();
        openCart();
    },

    removeItem(index) {
        this.items.splice(index, 1);
        this.save();
        this.render();
    },

    updateQty(index, newQty) {
        if (newQty < 1) {
            this.removeItem(index);
            return;
        }
        this.items[index].qty = newQty;
        this.save();
        this.render();
    },

    getTotal() {
        return this.items.reduce((sum, item) => {
            const product = PRODUCTS.find(p => p.id === item.productId);
            if (!product) return sum;
            const price = product.salePrice || product.price;
            return sum + price * item.qty;
        }, 0);
    },

    getCount() {
        return this.items.reduce((sum, item) => sum + item.qty, 0);
    },

    render() {
        const count = this.getCount();
        dom.cartCount.textContent = count;
        dom.cartHeaderCount.textContent = count;
        dom.cartTotal.textContent = formatPrice(this.getTotal());

        // Remove existing rendered items
        const existingItems = dom.cartItems.querySelectorAll('.cart-item');
        existingItems.forEach(el => el.remove());

        if (this.items.length === 0) {
            dom.cartEmpty.style.display = 'block';
            dom.cartFooter.style.display = 'none';
            return;
        }

        dom.cartEmpty.style.display = 'none';
        dom.cartFooter.style.display = 'block';

        this.items.forEach((item, index) => {
            const product = PRODUCTS.find(p => p.id === item.productId);
            if (!product) return;
            const price = product.salePrice || product.price;

            const el = document.createElement('div');
            el.className = 'cart-item';
            el.innerHTML = `
                <div class="cart-item-image">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="cart-item-details">
                    <h4>${product.name}</h4>
                    <div class="item-size">Size: ${item.size}</div>
                    <div class="item-price">${formatPrice(price)}</div>
                    <div class="qty-controls">
                        <button data-action="decrease" data-index="${index}">&minus;</button>
                        <span>${item.qty}</span>
                        <button data-action="increase" data-index="${index}">+</button>
                    </div>
                    <button class="remove-item" data-action="remove" data-index="${index}">Remove</button>
                </div>
            `;
            dom.cartItems.appendChild(el);
        });
    }
};

// --- Product Rendering ---
function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card fade-in';
    card.dataset.id = product.id;
    card.dataset.category = product.category;

    let priceHTML;
    if (product.salePrice) {
        priceHTML = `<span class="price-original">${formatPrice(product.price)}</span><span class="price-sale">${formatPrice(product.salePrice)}</span>`;
    } else {
        priceHTML = `<span>${formatPrice(product.price)}</span>`;
    }

    card.innerHTML = `
        <div class="product-card-image">
            <img src="${product.image}" alt="${product.name}" loading="lazy">
            <div class="product-card-actions">
                <button class="btn-product btn-product-outline" data-action="quick-view" data-id="${product.id}">Quick View</button>
                <button class="btn-product" data-action="add-to-bag" data-id="${product.id}">Add to Bag</button>
            </div>
        </div>
        <div class="product-card-info">
            <h4>${product.name}</h4>
            <div class="price">${priceHTML}</div>
        </div>
    `;
    return card;
}

function renderProducts(container, products) {
    if (!container) return;
    container.innerHTML = '';
    products.forEach((product, index) => {
        const card = createProductCard(product);
        card.style.transitionDelay = `${index * 0.08}s`;
        container.appendChild(card);
    });
}

// --- Quick View ---
let currentQuickViewId = null;
let qvQuantity = 1;

function openQuickView(productId) {
    const product = PRODUCTS.find(p => p.id === productId);
    if (!product) return;

    currentQuickViewId = productId;
    qvQuantity = 1;

    dom.qvImage.src = product.image;
    dom.qvImage.alt = product.name;
    dom.qvName.textContent = product.name;
    dom.qvDescription.textContent = product.description;
    dom.qvQty.textContent = '1';

    if (product.salePrice) {
        dom.qvPrice.innerHTML = `<span class="price-original">${formatPrice(product.price)}</span> <span class="price-sale">${formatPrice(product.salePrice)}</span>`;
    } else {
        dom.qvPrice.textContent = formatPrice(product.price);
    }

    dom.qvSize.innerHTML = '';
    product.sizes.forEach(size => {
        const option = document.createElement('option');
        option.value = size;
        option.textContent = size;
        dom.qvSize.appendChild(option);
    });

    dom.quickViewOverlay.classList.add('open');
    lockScroll();
}

function closeQuickView() {
    dom.quickViewOverlay.classList.remove('open');
    unlockScroll();
    currentQuickViewId = null;
}

// --- Cart Sidebar ---
function openCart() {
    dom.cartSidebar.classList.add('open');
    dom.cartOverlay.classList.add('open');
    lockScroll();
}

function closeCartSidebar() {
    dom.cartSidebar.classList.remove('open');
    dom.cartOverlay.classList.remove('open');
    unlockScroll();
}

// --- Mobile Menu ---
function openMobileMenu() {
    dom.mobileMenu.classList.add('open');
    lockScroll();
}

function closeMobileMenu() {
    dom.mobileMenu.classList.remove('open');
    unlockScroll();
}

// --- Search Overlay ---
function openSearch() {
    dom.searchOverlay.classList.add('open');
    lockScroll();
    setTimeout(() => dom.searchInput.focus(), 100);
}

function closeSearch() {
    dom.searchOverlay.classList.remove('open');
    unlockScroll();
    dom.searchInput.value = '';
}

// --- Sale Filtering ---
function filterSaleProducts(category) {
    const cards = dom.saleGrid.querySelectorAll('.product-card');
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// --- Announcement Bar ---
function initAnnouncement() {
    if (sessionStorage.getItem('romzy-announcement-dismissed')) {
        dom.announcementBar.classList.add('hidden');
        dom.navbar.classList.remove('has-announcement');
    }

    dom.closeAnnouncement.addEventListener('click', () => {
        dom.announcementBar.classList.add('hidden');
        dom.navbar.classList.remove('has-announcement');
        sessionStorage.setItem('romzy-announcement-dismissed', 'true');
    });
}

// --- Navbar Scroll Behavior ---
function initNavbarScroll() {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 80) {
            dom.navbar.classList.add('scrolled');
        } else {
            dom.navbar.classList.remove('scrolled');
        }
    });
}

// --- Scroll Animations ---
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

// --- Newsletter ---
function initNewsletter() {
    dom.newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = dom.newsletterForm.querySelector('input[type="email"]').value;
        if (email) {
            dom.newsletterForm.style.display = 'none';
            dom.newsletterSuccess.style.display = 'block';
        }
    });
}

// --- Event Delegation for Product Grids ---
function initProductEvents() {
    document.addEventListener('click', (e) => {
        const quickViewBtn = e.target.closest('[data-action="quick-view"]');
        if (quickViewBtn) {
            e.preventDefault();
            const id = parseInt(quickViewBtn.dataset.id);
            openQuickView(id);
            return;
        }

        const addToBagBtn = e.target.closest('[data-action="add-to-bag"]');
        if (addToBagBtn) {
            e.preventDefault();
            const id = parseInt(addToBagBtn.dataset.id);
            const product = PRODUCTS.find(p => p.id === id);
            if (product) {
                Cart.addItem(id, product.sizes[0], 1);
            }
            return;
        }
    });
}

// --- Event Listeners ---
function initEventListeners() {
    // Cart sidebar
    dom.cartBtn.addEventListener('click', openCart);
    dom.closeCart.addEventListener('click', closeCartSidebar);
    dom.cartOverlay.addEventListener('click', closeCartSidebar);
    dom.continueShopping.addEventListener('click', closeCartSidebar);

    // Cart item actions (delegation)
    dom.cartItems.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        const index = parseInt(btn.dataset.index);
        const action = btn.dataset.action;

        if (action === 'increase') Cart.updateQty(index, Cart.items[index].qty + 1);
        else if (action === 'decrease') Cart.updateQty(index, Cart.items[index].qty - 1);
        else if (action === 'remove') Cart.removeItem(index);
    });

    // Quick view
    dom.closeQuickView.addEventListener('click', closeQuickView);
    dom.quickViewOverlay.addEventListener('click', (e) => {
        if (e.target === dom.quickViewOverlay) closeQuickView();
    });

    dom.qvQtyMinus.addEventListener('click', () => {
        if (qvQuantity > 1) {
            qvQuantity--;
            dom.qvQty.textContent = qvQuantity;
        }
    });

    dom.qvQtyPlus.addEventListener('click', () => {
        qvQuantity++;
        dom.qvQty.textContent = qvQuantity;
    });

    dom.qvAddToBag.addEventListener('click', () => {
        if (currentQuickViewId) {
            const size = dom.qvSize.value;
            Cart.addItem(currentQuickViewId, size, qvQuantity);
            closeQuickView();
        }
    });

    // Search
    dom.searchBtn.addEventListener('click', openSearch);
    dom.closeSearch.addEventListener('click', closeSearch);

    // Mobile menu
    dom.hamburgerBtn.addEventListener('click', openMobileMenu);
    dom.closeMobileMenu.addEventListener('click', closeMobileMenu);

    // Mobile menu links
    dom.mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => closeMobileMenu());
    });

    // Filter pills
    dom.filterPills.addEventListener('click', (e) => {
        const pill = e.target.closest('.filter-pill');
        if (!pill) return;
        dom.filterPills.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        filterSaleProducts(pill.dataset.filter);
    });

    // Escape key handler
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeCartSidebar();
            closeQuickView();
            closeSearch();
            closeMobileMenu();
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const href = anchor.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // Render product grids
    const featuredProducts = PRODUCTS.filter(p => p.id >= 1 && p.id <= 8);
    const newArrivals = PRODUCTS.filter(p => p.id >= 9 && p.id <= 12);
    const saleProducts = PRODUCTS.filter(p => p.salePrice !== null);

    renderProducts(dom.featuredGrid, featuredProducts);
    renderProducts(dom.newArrivalsGrid, newArrivals);
    renderProducts(dom.saleGrid, saleProducts);

    // Initialize modules
    initAnnouncement();
    initNavbarScroll();
    initProductEvents();
    initEventListeners();
    initNewsletter();

    // Render cart from localStorage
    Cart.render();

    // Init scroll animations after a small delay to ensure DOM is ready
    setTimeout(() => initScrollAnimations(), 100);
});
