<template>
    <div>
        <!-- Línea superior (solo visible en rutas específicas) -->
        <div v-if="showTopLine" class="fixed top-0 left-0 right-0 h-2 bg-[#008d85] z-50"></div>

        <nav :class="['fixed w-full z-40 flex flex-col',
            {
                'bg-white': hasBackground,
                'bg-transparent': !hasBackground
            }]" :style="showTopLine ? 'top: 1px' : 'top: 0'">

            <!-- Primera línea (logo y menú) -->
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div class="flex justify-between h-16 items-center">
                    <!-- Logo -->
                    <div class="flex items-center">
                        <LogoSVG class="h-8 w-auto" />
                    </div>

                    <!-- Menú desktop -->
                    <div class="hidden md:flex items-center space-x-4">
                        <div class="flex space-x-8">
                            <router-link v-for="link in filteredLinks" :key="link.path" :to="link.path"
                                class="inline-flex items-center px-1 pt-1 text-sm" :class="getLinkClasses(link.path)">
                                {{ link.name }}
                            </router-link>
                        </div>

                        <!-- Botón de inicio de sesión -->
                        <Button v-if="variant === 'access'" size="sm" class="ml-4 bg-btn" variant="secondary">
                            <router-link to="/login">Iniciar Sesión</router-link>
                        </Button>
                    </div>

                    <!-- Botón menú móvil -->
                    <div class="-mr-2 flex items-center md:hidden">
                        <button @click="toggleMobileMenu"
                            class="inline-flex items-center justify-center p-2 rounded-md focus:outline-none" :class="{
                                'text-gray-500 hover:text-gray-700 hover:bg-gray-100': hasBackground,
                                'text-white hover:text-white/80 hover:bg-white/10': !hasBackground
                            }">
                            <span class="sr-only">Abrir menú principal</span>
                            <TblrMenu v-if="!isMobileMenuOpen" class="h-6 w-6" />
                            <TblrX v-else class="h-6 w-6" />
                        </button>
                    </div>
                </div>
            </div>

            <!-- Menú móvil desplegable -->
            <Transition enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95">
                <div v-show="isMobileMenuOpen" class="md:hidden">
                    <div class="px-2 pt-2 pb-3 space-y-1 shadow-lg"
                        :class="{ 'bg-white': hasBackground, 'bg-gray-900': !hasBackground }">
                        <router-link v-for="link in filteredLinks" :key="link.path" :to="link.path"
                            class="block px-3 py-2 rounded-md text-base font-medium"
                            :class="getMobileLinkClasses(link.path)" @click="closeMobileMenu">
                            {{ link.name }}
                        </router-link>

                        <!-- Opción de inicio de sesión en móvil -->
                        <router-link v-if="variant === 'access'" to="/login"
                            class="block px-3 py-2 rounded-md text-base font-medium border-t border-gray-200 mt-2"
                            :class="getMobileLinkClasses('/login')" @click="closeMobileMenu">
                            Iniciar Sesión
                        </router-link>
                    </div>
                </div>
            </Transition>
        </nav>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import LogoSVG from '../../assets/icons/logo.vue'
import Button from '../../components/common/Button.vue'

const props = defineProps({
    hasBackground: {
        type: Boolean,
        default: true
    },
    variant: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'access'].includes(value)
    }
})

const route = useRoute()
const isMobileMenuOpen = ref(false)

const allLinks = [
    { path: '/', name: 'Inicio' },
    { path: '/proyectos', name: 'Proyectos' },
    { path: '/investigadores', name: 'Investigadores' },
    { path: '/nosotros', name: 'Nosotros' }
]

// Computed para determinar si mostrar la línea superior
const showTopLine = computed(() => {
    return [
        '/proyectos',
        '/investigadores',
        '/nosotros'
    ].includes(route.path)
})

const filteredLinks = computed(() => {
    return allLinks
})

const getLinkClasses = (path) => {
    const isActive = route.path === path;
    if (props.hasBackground) {
        return {
            'font-bold text-[#008d85]': isActive,
            'font-bold border-transparent text-gray-500 hover:text-[#006b64]': !isActive
        };
    } else {
        return {
            'font-bold text-white': isActive,
            'font-bold border-transparent text-white/80 hover:text-white': !isActive
        };
    }
};

const getMobileLinkClasses = (path) => {
    const isActive = route.path === path;
    if (props.hasBackground) {
        return {
            'bg-green-50 font-bold text-[#008d85]': isActive,
            'font-bold text-gray-500 hover:text-[#006b64] hover:bg-gray-100': !isActive
        };
    }
};

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
}
</script>

<style scoped>
.bg-btn {
    background: #008d85;
    color: white;
    font-weight: bold;
}

.bg-btn:hover {
    background: #006b64;
}
</style>