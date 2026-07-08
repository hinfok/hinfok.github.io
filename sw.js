const CACHE = "hkinfo-v1";
const URLS = ["/","/index.html","/privacy.html","/about.html","/rental-price-index.html","/public-housing.html","/income-vs-price.html","/vacancy-rate.html","/homeownership-district.html"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(URLS))); self.skipWaiting(); });
self.addEventListener("fetch", e => { e.respondWith(caches.match(e.request).then(r => r || fetch(e.request))); });