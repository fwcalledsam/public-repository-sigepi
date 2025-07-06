import axios from "axios";

// Configuración
const API_COOLDOWN = 2000; // 2 segundos entre llamadas al mismo endpoint
const CACHE_EXPIRY = 5 * 60 * 1000; // 5 minutos

// Crear instancia de axios con URL base
const api = axios.create({
    baseURL: "/api",
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: false
});

// Objeto para rastrear los últimos tiempos de llamada por endpoint
const lastCallTimes = {};

// Objeto para almacenar promesas en curso y evitar llamadas duplicadas
const pendingRequests = {};

console.log("===========================================");

// Interceptor para manejar caché y cooldown
api.interceptors.request.use(
    async (config) => {
        const endpointKey = `${config.method}:${config.url}`;
        const now = Date.now();

        console.log(`[API] Intentando acceder a: ${endpointKey} en ${new Date(now).toLocaleTimeString()}`);

        // Excluir endpoints de imágenes del cooldown y caché
        const isImageEndpoint = config.url.includes('/image') ||
            config.url.includes('/upload-image') ||
            config.url.includes('/update-image') ||
            config.url.includes('/delete-image');

        if (isImageEndpoint) {
            console.log(`[API] Endpoint de imagen detectado, omitiendo cooldown y caché: ${endpointKey}`);
            return config; // No aplicar caché ni cooldown para imágenes
        }

        // Verificar cooldown
        if (lastCallTimes[endpointKey] && (now - lastCallTimes[endpointKey] < API_COOLDOWN)) {
            console.log(`[API] Cooldown activo (${API_COOLDOWN} ms) para: ${endpointKey}`);
            // Intentar obtener de caché si está en cooldown
            const cachedData = getFromCache(endpointKey);
            if (cachedData) {
                console.log(`[API] Sirviendo desde caché debido al cooldown: ${endpointKey}`);
                return {
                    ...config,
                    adapter: () => Promise.resolve({
                        data: cachedData.data,
                        status: 200,
                        statusText: 'OK',
                        headers: {},
                        config
                    }),
                    metadata: { fromCache: true }
                };
            } else {
                console.log(`[API] Cooldown: no se encontró caché válida para ${endpointKey}`);
            }
        }

        // Si ya hay una petición en curso para este endpoint, reutilizarla
        if (pendingRequests[endpointKey]) {
            console.log(`[API] Reutilizando solicitud pendiente: ${endpointKey}`);
            return pendingRequests[endpointKey];
        }

        // Registrar tiempo de última llamada
        lastCallTimes[endpointKey] = now;

        // Crear nueva promesa para la petición
        const requestPromise = new Promise((resolve) => {
            // Verificar caché primero para GET requests
            if (config.method === 'get') {
                const cachedData = getFromCache(endpointKey);
                if (cachedData && !isCacheExpired(cachedData.timestamp)) {
                    console.log(`[API] Obteniendo cache para: ${endpointKey}`);
                    console.log("------------------");
                    resolve({
                        ...config,
                        adapter: () => Promise.resolve({
                            data: cachedData.data,
                            status: 200,
                            statusText: 'OK',
                            headers: {},
                            config
                        }),
                        metadata: { fromCache: true }
                    });
                    return;
                }
            }
            console.log(`[API] Enviando petición a ${endpointKey}`);
            resolve(config);
        });

        pendingRequests[endpointKey] = requestPromise;
        return requestPromise;
    },
    error => Promise.reject(error)
);

// Interceptor para manejar respuestas y almacenar en caché
api.interceptors.response.use(
    response => {
        const endpointKey = `${response.config.method}:${response.config.url}`;

        // Eliminar la petición pendiente
        delete pendingRequests[endpointKey];

        // Excluir endpoints de imágenes del caché
        const isImageEndpoint = response.config.url.includes('/image') ||
            response.config.url.includes('/upload-image') ||
            response.config.url.includes('/update-image') ||
            response.config.url.includes('/delete-image');

        if (!isImageEndpoint) {
            // Almacenar en caché solo las respuestas GET exitosas que no vengan de caché
            if (response.config.method === 'get' && !response.config.metadata?.fromCache) {
                console.log(`[API] Guardando respuesta en caché para: ${endpointKey}`);
                saveToCache(endpointKey, response.data);
            } else if (['post', 'put', 'delete', 'patch'].includes(response.config.method)) {
                console.log(`[API] Invalidando caché relacionada con: ${response.config.url}`);
                // Invalidar caché cuando hay cambios en la BD
                clearRelatedCache(response.config.url);
            }
        }

        return response;
    },
    error => {
        if (error.config) {
            const endpointKey = `${error.config.method}:${error.config.url}`;
            delete pendingRequests[endpointKey];
        }
        console.error('[API] Error en la respuesta:', error);
        return Promise.reject(error);
    }
);

// Función para limpiar caché relacionada con la URL
function clearRelatedCache(url) {
    // Extraer la parte base de la URL (por ejemplo, '/persons' de '/persons/123')
    const baseUrl = url.split('/').slice(0, 2).join('/');

    Object.keys(localStorage).forEach(key => {
        if (key.startsWith('api_cache_')) {
            // Eliminar caché de:
            // 1. La URL exacta
            // 2. La URL base (para operaciones con ID)
            // 3. Las listas que podrían incluir el elemento afectado
            if (key.includes(url) ||
                key.includes(baseUrl) ||
                (url.includes(baseUrl) && key.includes(`${baseUrl}s`))) {
                localStorage.removeItem(key);
                console.log(`[API] Cache limpiado para: ${key}`);
            }
        }
    });
    console.log("------------------");
}
// Funciones de caché
function saveToCache(key, data) {
    try {
        const cacheEntry = {
            data,
            timestamp: Date.now()
        };
        localStorage.setItem(`api_cache_${key}`, JSON.stringify(cacheEntry));
        console.log(`[API] Guardado en caché: ${key}`);
    } catch (e) {
        console.warn('[API] Error al guardar en caché', e);
    }
    console.log("------------------");
}

function getFromCache(key) {
    try {
        console.log(`[API] Caché encontrada para: ${key}`);
        const cached = localStorage.getItem(`api_cache_${key}`);
        console.log("------------------");
        return cached ? JSON.parse(cached) : null;
    } catch (e) {
        console.warn('[API] Error al leer desde caché', e);
        console.log("------------------");
        return null;
    }
}

function isCacheExpired(timestamp, key) {
    console.log(`[API] Caché expirada (${CACHE_EXPIRY} ms)`);
    return (Date.now() - timestamp) > CACHE_EXPIRY;
}

// Función para limpiar caché expirada
function cleanExpiredCache() {
    Object.keys(localStorage).forEach(key => {
        if (key.startsWith('api_cache_')) {
            try {
                const entry = JSON.parse(localStorage.getItem(key));
                if (isCacheExpired(entry.timestamp)) {
                    localStorage.removeItem(key);
                    console.log('[API] Cache removido', e);
                }
            } catch (e) {
                console.warn('[API] Error al limpiar el caché', e);
                localStorage.removeItem(key);
            }
        }
    });
}

// Limpiar caché expirada al cargar
cleanExpiredCache();

export default api;