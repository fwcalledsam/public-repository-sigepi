<!-- L A N D S C A P E -->
<template>
    <div class="flex min-h-screen w-full flex-col">
        <!-- NavBar con fondo en mobile y sin fondo en desktop -->
        <NavBar :has-background="isMobile" variant="access" />

        <main class="flex-1">

            <!-- Versión Mobile -->
            <div class="md:hidden">
                <div class="relative min-h-screen pt-[190px]">
                    <img :src="heroImage" alt="Grupo ALEF" class="absolute inset-0 w-full h-full object-cover" />
                    <div class="relative z-10 h-full flex items-center p-6">
                        <div class="bg-white/90 backdrop-blur-sm p-6 rounded-lg shadow-lg w-full">
                            <ImagoTipo class="w-40 mb-1 mx-auto" />
                            <h1 class="text-3xl font-bold tracking-tight text-gray-900 mb-4">
                                Descubre nuestras contribuciones
                            </h1>
                            <p class="text-lg text-[#808080] mb-6">
                                Únete al Grupo ALEF y forma parte de nuestra comunidad de investigación y desarrollo
                                tecnológico.
                            </p>
                            <Button class="w-fit bg-btn">
                                <router-link to="/proyectos" class="flex items-center gap-2">
                                    Explorar ALEF
                                    <HrsldArrowRight class="h-4 w-4" />
                                </router-link>
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Versión Desktop -->
            <div class="hidden md:flex h-screen">
                <!-- Sección izquierda (Texto y CTA) -->
                <div class="w-1/2 p-12 flex flex-col justify-center bg-white">
                    <div class="max-w-lg mx-auto space-y-6">
                        <ImagoTipo class="w-96 mb-10 mx-auto" />
                        <h1 class="text-4xl font-bold tracking-tight text-gray-900">
                            Descubre nuestras contribuciones
                        </h1>
                        <p class="text-lg text-gray-700">
                            Únete al Grupo ALEF y forma parte de nuestra comunidad de investigación y desarrollo
                            tecnológico.
                        </p>
                        <Button class="w-fit mt-4 bg-btn">
                            <router-link to="/proyectos" class="flex items-center gap-2">
                                Explorar ALEF
                                <HrsldArrowRight class="h-4 w-4" />
                            </router-link>
                        </Button>
                    </div>
                </div>

                <!-- Sección derecha (Imagen) -->
                <div class="w-1/2 relative">
                    <img :src="heroImage" alt="Grupo ALEF" class="absolute inset-0 w-full h-full object-cover" />
                </div>
            </div>

        </main>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import NavBar from '../../components/layout/NavBar.vue'
import Button from '../../components/common/Button.vue'
import ImagoTipo from '../../assets/icons/ImagoTipo.vue'

// URL de la imagen centralizada en una variable
const heroImage = '/landpage.png'

const isMobile = ref(false)

const checkIsMobile = () => {
    isMobile.value = window.innerWidth < 768
}

onMounted(() => {
    checkIsMobile()
    window.addEventListener('resize', checkIsMobile)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', checkIsMobile)
})
</script>

<style scoped>
.bg-btn {
    background: #008d85;
    color: white;
}

.bg-btn:hover {
    background: #006b64;
}
</style>