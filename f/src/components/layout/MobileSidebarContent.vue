<template>
    <Transition name="fade">
        <div class="flex min-h-screen">
            <!-- Sidebar Mobile (Drawer) -->
            <div v-if="isMobileMenuOpen" class="fixed inset-0 z-40 md:hidden">
                <div class="fixed inset-0 bg-black/40" @click="isMobileMenuOpen = false"></div>
                <div class="fixed left-0 top-0 h-full w-64 bg-background border-r">
                    <div class="flex h-16 items-center border-b px-6 justify-between">
                        <p class="flex items-center gap-2 font-semibold">
                            <LogoSVG class="h-6 w-6" />
                            <span>CINVESTAV</span>
                        </p>
                        <button @click="isMobileMenuOpen = false" class="p-1 rounded-md hover:bg-muted">
                            <TblrX class="h-5 w-5" />
                        </button>
                    </div>
                    <div class="h-[calc(100vh-4rem)] overflow-auto p-4">
                        <MobileSidebarContent @close="isMobileMenuOpen = false" />
                    </div>
                </div>
            </div>

            <!-- Sidebar Desktop -->
            <div class="hidden border-r bg-muted/40 md:block md:w-64">
                <!-- ... (contenido existente del sidebar) ... -->
            </div>

            <!-- Main content -->
            <div class="flex-1">
                <div class="h-16 border-b">
                    <div class="flex h-full items-center justify-between px-4 md:px-6">
                        <!-- Botón para abrir el menú móvil -->
                        <button @click="isMobileMenuOpen = true" class="md:hidden p-2 rounded-md hover:bg-muted">
                            <TblrMenu class="h-5 w-5" />
                        </button>

                        <div class="flex items-center gap-2">
                            <h1 class="text-lg font-medium">Panel de Administración</h1>
                            <!-- Botón de guía -->
                            <button @click="modalStore.openGuideModal()"
                                class="p-1.5 rounded-md hover:bg-gray-100 text-muted-foreground transition-colors"
                                title="Mostrar guía">
                                <HrsldBook class="h-4 w-4" />
                            </button>
                        </div>

                        <!-- Botón de cerrar sesión para móviles -->
                        <div class="md:hidden">
                            <button @click="logout"
                                class="flex h-8 items-center rounded-md px-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
                                <TblrLogOut class="mr-2 h-4 w-4" />
                            </button>
                        </div>
                    </div>
                </div>
                <div class="p-4 md:p-6">
                    <router-view />
                </div>
            </div>

            <!-- Modal para cargar CSV -->
            <UploadModal :is-open="modalStore.isUploadModalOpen" :on-close="modalStore.closeUploadModal" />
            <GuideModal :is-open="modalStore.isGuideModalOpen" :on-close="modalStore.closeGuideModal" />
        </div>
    </Transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useModalStore } from '../../stores/modal';
import UploadModal from '../../components/modals/general/UploadModal.vue';
import GuideModal from '../../components/modals/general/GuideModal.vue';
import MobileSidebarContent from '../../components/layout/MobileSidebarContent.vue';
import LogoSVG from '../../assets/icons/logo.vue';

const router = useRouter();
const modalStore = useModalStore();
const isMobileMenuOpen = ref(false);
const isMobile = ref(window.innerWidth < 768);

const updateIsMobile = () => {
    isMobile.value = window.innerWidth < 768;
    if (!isMobile.value) {
        isMobileMenuOpen.value = false;
    }
};

onMounted(() => {
    window.addEventListener('resize', updateIsMobile);
    const isAuthenticated = localStorage.getItem('isAuthenticated');
    if (!isAuthenticated) {
        router.push('/login');
    }
});

onBeforeUnmount(() => {
    window.removeEventListener('resize', updateIsMobile);
});

const logout = () => {
    localStorage.removeItem('isAuthenticated');
    router.push('/login');
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>