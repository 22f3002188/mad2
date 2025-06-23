// import './assets/main.css'

// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'

// const app = createApp(App)

// app.use(router)

// app.mount('#app')
// import './assets/main.css'

// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'

// const app = createApp(App)

// app.use(router)

// app.mount('#app')


// import './assets/main.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

const app = createApp(App);

// Add Bootstrap CSS and JS via CDN
const addBootstrapCDN = () => {
  // Bootstrap CSS
  const link = document.createElement('link');
  link.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css';
  link.rel = 'stylesheet';
  document.head.appendChild(link);

  // Bootstrap JavaScript Bundle
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js';
  script.defer = true; // Ensure it's loaded asynchronously
  document.head.appendChild(script);
};

addBootstrapCDN();

app.use(router);

app.mount('#app');
