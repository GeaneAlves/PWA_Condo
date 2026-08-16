const CACHE_NAME = 'condo-pwa-v1';
const urlsToCache = [
    '/',
    '/frontend/index.html',
    '/frontend/assets/css/style.css',
    '/frontend/assets/js/app.js'
];

self.addEventListener('install', (event) => {
    event.waiUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
    );
});

self.addEventListener('install', (event) => {
    event.waiUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
    );

});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => response || fetch(event.request))
    );

});