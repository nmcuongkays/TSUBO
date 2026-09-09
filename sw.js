const C='tsubogawa-v2-9-instant-last-good';
const SHELL=['./','./index.html','./manifest.webmanifest','./icon-180.png','./icon-192.png','./icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(u.origin!==location.origin) return;
  // Never cache data JSON/images here; the app explicitly asks network with cache busting.
  if(u.pathname.includes('/data/')) return;
  e.respondWith(
    Promise.race([
      fetch(e.request).then(r=>{const c=r.clone();caches.open(C).then(cache=>cache.put(e.request,c));return r;}),
      new Promise((_,rej)=>setTimeout(()=>rej(new Error('network-timeout')),1800))
    ]).catch(()=>caches.match(e.request))
  );
});
