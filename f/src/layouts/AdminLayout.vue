<template>
  <div class="flex min-h-screen">
    <!-- Mobile Sidebar (Drawer) -->
    <Transition name="fade">
      <div v-if="isMobileMenuOpen" class="fixed inset-0 z-40 md:hidden">
        <div class="fixed inset-0 bg-black/40" @click="isMobileMenuOpen = false"></div>
        <div class="fixed left-0 top-0 h-full w-64 bg-background border-r">
          <div class="flex h-16 items-center border-b px-6 justify-between">
            <p class="flex items-center gap-2 font-semibold">
              <LogoSVG class="h-6 w-6" />
              <span>GRUPO ALEF</span>
            </p>
            <button @click="isMobileMenuOpen = false" class="p-1 rounded-md hover:bg-muted">
              <TblrX class="h-5 w-5" />
            </button>
          </div>
          <div class="h-[calc(100vh-4rem)] overflow-auto p-4">
            <div class="flex flex-col gap-4 h-full">
              <div class="flex flex-col gap-2">

                <router-link to="/admin" @click="isMobileMenuOpen = false"
                  class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
                  exact-active-class="bg-muted">
                  <HrsldBriefcase class="mr-2 h-4 w-4" />
                  Proyectos
                </router-link>

                <router-link to="/admin/project-assignments" @click="isMobileMenuOpen = false"
                  class="flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors hover:bg-muted"
                  active-class="bg-muted">
                  <TblrReplaceFilled class="mr-3 h-4 w-4" />
                  Asignaciones de Proyectos
                </router-link>

                <div class="border-t border-gray-300 w-full max-w-2xl my-1"></div>

                <router-link to="/admin/personas" @click="isMobileMenuOpen = false"
                  class="flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors hover:bg-muted"
                  active-class="bg-muted">
                  <HrsldUsers class="mr-3 h-4 w-4" />
                  Personas
                </router-link>
                <router-link to="/admin/roles" @click="isMobileMenuOpen = false"
                  class="flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors hover:bg-muted"
                  active-class="bg-muted">
                  <TblrPuzzle class="mr-3 h-4 w-4" />
                  Roles
                </router-link>
                <router-link to="/admin/niveles" @click="isMobileMenuOpen = false"
                  class="flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors hover:bg-muted"
                  active-class="bg-muted">
                  <TblrAdjustments class="mr-3 h-4 w-4" />
                  Niveles de Proyecto
                </router-link>
              </div>

              <!-- <div class="border-t border-gray-300 w-full max-w-2xl my-1"></div>
              
              <button @click="modalStore.openUploadModal(); isMobileMenuOpen = false"
                class="flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors hover:bg-muted">
                <TblrUpload class="mr-3 h-4 w-4" />
                Cargar información
              </button>
              
              <div class="border-t border-gray-300 w-full max-w-2xl my-1"></div> -->
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Desktop Sidebar -->
    <div class="hidden border-r bg-muted/40 md:block md:w-64">
      <div class="flex h-16 items-center border-b px-6">
        <p class="flex items-center gap-2 font-semibold">
          <LogoSVG class="h-6 w-6" />
          <span>GRUPO ALEF</span>
        </p>
      </div>

      <div class="h-[calc(100vh-4rem)] overflow-auto">
        <div class="flex flex-col gap-4 p-4">
          <div class="flex flex-col gap-2">
            <router-link to="/admin" exact
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
              exact-active-class="bg-muted">
              <HrsldBriefcase class="mr-2 h-4 w-4" />
              Proyectos
            </router-link>
            <router-link to="/admin/project-assignments"
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
              active-class="bg-muted">
              <TblrReplaceFilled class="mr-2 h-4 w-4" />
              Asignaciones de Proyectos
            </router-link>

            <div class="border-t border-gray-300 w-full max-w-2xl"></div>

            <router-link to="/admin/personas"
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
              active-class="bg-muted">
              <HrsldUsers class="mr-2 h-4 w-4" />
              Personas
            </router-link>
            <router-link to="/admin/roles"
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
              active-class="bg-muted">
              <TblrPuzzle class="mr-2 h-4 w-4" />
              Roles
            </router-link>
            <router-link to="/admin/niveles"
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium transition-colors hover:bg-muted"
              active-class="bg-muted">
              <TblrAdjustments class="mr-2 h-4 w-4" />
              Niveles de Proyecto
            </router-link>
          </div>

          <div class="border-t border-gray-300 w-full max-w-2xl"></div>
          <!-- cargar datos masivamente | .csv -->
          <div class="mt-auto">
            <button @click="modalStore.openUploadModal"
              class="flex h-8 w-full items-center rounded-md px-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <TblrUpload class="mr-2 h-4 w-4" />
              Cargar información
            </button>
          </div>

          <div class="border-t border-gray-300 w-full max-w-2xl"></div>

          <!-- Botón de cerrar sesión -->
          <div class="mt-auto">
            <button @click="logout"
              class="flex h-8 w-full items-center rounded-md px-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <TblrLogOut class="mr-2 h-4 w-4 text-gray-700" />
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Main content -->
    <div class="flex-1">
      <div class="h-16 border-b">
        <div class="flex h-full items-center justify-between px-4 md:px-6">
          <div class="flex items-center gap-2">
            <!-- Mobile menu button -->
            <button @click="isMobileMenuOpen = true" class="md:hidden p-2 rounded-md hover:bg-muted">
              <TblrMenu class="h-5 w-5" />
            </button>

            <h1 class="text-lg font-medium">Panel de Administración</h1>
            <button @click="modalStore.openGuideModal()"
              class="p-1.5 rounded-md hover:bg-gray-100 text-muted-foreground transition-colors" title="Mostrar guía">
              <HrsldBook class="h-4 w-4" />
            </button>
          </div>

          <div class="md:hidden">
            <button @click="logout"
              class="flex h-8 items-center rounded-md px-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <TblrLogOut class="h-5 w-5 text-red-500" />
            </button>
          </div>
        </div>
      </div>
      <div class="p-4 md:p-6">
        <router-view />
      </div>
    </div>
  </div>
  <!-- Modals -->
  <UploadModal :is-open="modalStore.isUploadModalOpen" :on-close="modalStore.closeUploadModal" />
  <GuideModal :is-open="modalStore.isGuideModalOpen" :on-close="modalStore.closeGuideModal" />

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useModalStore } from '../stores/modal';
import { authApi } from '../lib/api';
import UploadModal from '../components/modals/general/UploadModal.vue';
import GuideModal from '../components/modals/general/GuideModal.vue';
import LogoSVG from '../assets/icons/logo.vue';

const router = useRouter();
const modalStore = useModalStore();
const isMobileMenuOpen = ref(false);

const updateIsMobile = () => {
  if (window.innerWidth >= 768) {
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

const logout = async () => {
  try {
    await authApi.logout();

    // Elimina el token de autenticación del localStorage
    localStorage.removeItem('isAuthenticated');

    // Verifica que el token se haya eliminado correctamente
    if (!localStorage.getItem('isAuthenticated')) {
      console.log('Logout exitoso: Token eliminado');
      // Redirige al login con un mensaje de éxito
      router.push({ path: '/login', query: { logout: 'success' } });
    } else {
      console.error('Error: Token no eliminado');
    }
  } catch (error) {
    console.error('Error durante el logout:', error);
    // Redirige igualmente, pero muestra un mensaje de error si es necesario
    router.push('/login');
  }
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