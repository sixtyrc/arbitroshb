/* Service Worker para ArbitrosHB */

self.addEventListener('push', function(event) {
  let data = { title: 'Nueva Notificación', body: 'Revisá la app para más detalles.' };
  
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      data = { title: 'ArbitrosHB', body: event.data.text() };
    }
  }

  const options = {
    body: data.body,
    icon: '/pwa-192x192.png',
    badge: '/favicon.svg',
    vibrate: [200, 100, 200],
    data: {
      url: data.url || '/'
    }
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
