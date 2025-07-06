import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './assets/main.css';

// Importar los íconos desde el archivo icons.js
import { icons } from './assets/icons/icons';

import LogoSVG from './assets/icons/logo.vue'

// Importar la configuración de API
import api from './lib/api';

const app = createApp(App);

// Configurar
app.use(createPinia());
app.use(router);

// Registrar los íconos globalmente
for (const [name, component] of Object.entries(icons)) {
    app.component(name, component);
}

app.component('LogoSVG', LogoSVG)

// Hacer que la API esté disponible globalmente (opcional)
app.config.globalProperties.$api = api;

app.mount('#app');