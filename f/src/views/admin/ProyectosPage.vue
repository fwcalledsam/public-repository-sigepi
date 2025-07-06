<template>
  <div class="space-y-2">
    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Gestión de Proyectos</h2>
        <Button v-if="proyectos.length > 0" @click="modalStore.openCreateModal()" class="md:size-default">
          <TblrFolderPlus class="h-4 w-4" />
          <span class="hidden md:inline ml-2">Nuevo Proyecto</span>
        </Button>
      </div>
      <div class="relative w-full max-w-sm">
        <HrsldSearch class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <input type="search" placeholder="Buscar por título..."
          class="flex h-8 w-full rounded-md border border-input bg-background px-3 py-1 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          v-model="searchTerm" />
      </div>
    </div>

    <!-- Vista móvil (cards) -->
    <div v-if="proyectos.length > 0" class="md:hidden space-y-3">
      <div v-for="proyecto in filteredProyectos" :key="proyecto.project_id" class="p-4 border rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">{{ proyecto.project_name }}</h3>
            <p class="text-sm text-muted-foreground">{{ getNivelDescription(proyecto.level_id) }} - {{
              proyecto.project_agno }}</p>
          </div>
          <div class="flex space-x-1">
            <Button variant="ghost" size="sm" @click="handleEdit(proyecto)" class="p-2">
              <TblrEdit class="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" @click="handleDelete(proyecto.project_id)"
              class="p-2 text-red-600 hover:text-red-800">
              <HrsldTrash class="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div class="mt-2">
          <p class="text-sm line-clamp-2">{{ proyecto.project_description }}</p>
        </div>

        <div class="mt-3 flex flex-wrap gap-1">
          <template v-if="proyecto.project_keywords && proyecto.project_keywords.trim() !== ''">
            <template v-if="proyecto.project_keywords.split(',').length > 2">
              <Badge variant="outline" class="text-xs">
                +{{ proyecto.project_keywords.split(',').length }} keywords
              </Badge>
            </template>
            <template v-else>
              <Badge v-for="(keyword, index) in proyecto.project_keywords.split(',')" :key="index" variant="outline"
                class="text-xs max-w-[80px] truncate" :title="keyword.trim()">
                {{ keyword.trim() }}
              </Badge>
            </template>
          </template>
          <template v-else>
            <Badge variant="outline" class="text-xs">Sin keywords</Badge>
          </template>
        </div>

        <div class="mt-3">
          <Badge variant="outline" class="text-xs cursor-pointer hover:bg-gray-100"
            @click="handleImageClick(proyecto.project_id, proyecto.project_image_path)">
            {{ proyecto.project_image_path ? 'Ver imagen' : 'Sin imagen' }}
          </Badge>
        </div>
      </div>
    </div>

    <!-- Vista desktop (tabla) -->
    <div v-if="proyectos.length > 0" class="hidden md:block rounded-md border">
      <!-- Contenedor con scroll -->
      <div :style="{ 'max-height': containerHeight + 'px' }" class="overflow-auto">
        <table class="w-full">
          <thead class="sticky top-0 bg-white shadow-md">
            <tr class="border-b bg-muted/50">
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Proyecto</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Descripción</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Palabras clave</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Año</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Nivel</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Imagen</th>
              <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="proyecto in filteredProyectos" :key="proyecto.project_id" class="border-b">
              <!-- name -->
              <td class="p-4 align-middle font-medium max-w-48 truncate">{{ proyecto.project_name }}</td>
              <!-- description -->
              <td class="p-4 align-middle max-w-48 truncate">{{ proyecto.project_description }}</td>
              <!-- keywords -->
              <td class="p-4 align-middle max-w-48 truncate">
                <template v-if="!proyecto.project_keywords || proyecto.project_keywords.trim() === ''">
                  <span class="text-muted-foreground">Sin keywords asignadas</span>
                </template>
                <template v-else>
                  <template v-if="proyecto.project_keywords.split(',').length > 2">
                    <Badge variant="outline">
                      Más de 2 keywords
                    </Badge>
                  </template>
                  <template v-else>
                    <div class="flex flex-wrap gap-1">
                      <Badge v-for="(keyword, index) in proyecto.project_keywords.split(',')" :key="index"
                        variant="outline" class="max-w-[100px] truncate" :title="keyword.trim()">
                        {{ keyword.trim() }}
                      </Badge>
                    </div>
                  </template>
                </template>
              </td>
              <!-- year -->
              <td class="p-4 align-middle">{{ proyecto.project_agno }}</td>
              <!-- level -->
              <td class="p-4 align-middle">{{ getNivelDescription(proyecto.level_id) }}</td>
              <!-- actions -->
              <td class="p-4 align-middle">
                <Badge variant="outline" class="cursor-pointer hover:bg-gray-100"
                  @click="handleImageClick(proyecto.project_id, proyecto.project_image_path)">
                  {{ proyecto.project_image_path ? 'Ver imagen' : 'Sin imagen' }}
                </Badge>
              </td>
              <td class="p-4 align-middle text-right">
                <Button variant="ghost" size="sm" @click="handleEdit(proyecto)">
                  <TblrEdit class="mr-2 h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" class="text-red-600 hover:text-red-800"
                  @click="handleDelete(proyecto.project_id)">
                  <HrsldTrash class="mr-2 h-4 w-4" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <EmptyState v-else title="No hay proyectos registrados" description="Comience creando su primer proyecto"
      actionText="Crear proyecto" :icon="TblrSettings" :onAction="modalStore.openCreateModal" />

  </div>
  <!-- Modales -->
  <ProyectoModal :is-open="modalStore.isCreateModalOpen" :on-close="modalStore.closeCreateModal" mode="create"
    @refresh="fetchProjects" />

  <ProyectoModal v-if="modalStore.currentItem" :is-open="modalStore.isEditModalOpen"
    :on-close="modalStore.closeEditModal" :proyecto="modalStore.currentItem" mode="edit" @refresh="fetchProjects" />

  <!-- Image Preview Modal -->
  <div v-if="imagePreviewOpen" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
    @click="closeImagePreview">
    <div class="bg-white p-4 rounded-lg max-w-4xl max-h-[90vh] overflow-auto" @click.stop>
      <img :src="projectImagePath" alt="Project Image Preview" class="max-w-full max-h-[80vh]">
      <div class="mt-4 flex justify-end">
        <Button @click="closeImagePreview">Cerrar</Button>
      </div>
    </div>
  </div>

  <!-- Alert Modal -->
  <AlertModal :is-open="modalStore.isAlertOpen" :on-close="modalStore.closeAlert" :title="modalStore.alertConfig.title"
    :message="modalStore.alertConfig.message" :confirm-text="modalStore.alertConfig.confirmText"
    :cancel-text="modalStore.alertConfig.cancelText" :loading-text="modalStore.alertConfig.loadingText"
    :confirm-variant="modalStore.alertConfig.confirmVariant" :show-cancel="modalStore.alertConfig.showCancel"
    :on-confirm="modalStore.alertConfig.onConfirm" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { projectsApi, levelsApi, projectImagesApi } from '../../lib/api'
import { useModalStore } from '../../stores/modal'
import Button from '../../components/common/Button.vue'
import ProyectoModal from '../../components/modals/projects/ProyectoModal.vue'
import Badge from '../../components/common/Badge.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import AlertModal from '../../components/modals/general/AlertModal.vue'
import { useContainerHeight } from '../../utils/calculateContainerHeight'

const { containerHeight } = useContainerHeight()
const modalStore = useModalStore();
const proyectos = ref([]);
const niveles = ref([]);
const projectImagePath = ref(null);
const imagePreviewOpen = ref(false);
const searchTerm = ref('');

// Función para normalizar vocales con acentos
const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

const sortedProyectos = computed(() => {
  return [...proyectos.value].sort((a, b) => b.project_id - a.project_id);
});

const filteredProyectos = computed(() => {
  if (!searchTerm.value.trim()) return sortedProyectos.value;

  const searchTermNormalized = normalizeString(searchTerm.value);

  return sortedProyectos.value.filter(proyecto =>
    normalizeString(proyecto.project_name).includes(searchTermNormalized))
});

const getNivelDescription = (levelId) => {
  const nivel = niveles.value.find(n => n.level_id === levelId);
  return nivel ? nivel.level_description : 'No especificado';
};

async function handleImageClick(projectId, imagePath) {
  if (!imagePath) {
    modalStore.showAlert('No hay imagen disponible');
    return;
  }

  try {
    const response = await projectImagesApi.get(projectId);
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    projectImagePath.value = URL.createObjectURL(blob);
    imagePreviewOpen.value = true;
  } catch (error) {
    console.error('Error cargando imagen del proyecto:', error);
    modalStore.showAlert('No se pudo cargar la imagen del proyecto');
  }
}

function closeImagePreview() {
  if (projectImagePath.value?.startsWith('blob:')) {
    URL.revokeObjectURL(projectImagePath.value);
  }
  projectImagePath.value = null;
  imagePreviewOpen.value = false;
}

async function fetchProjects() {
  try {
    const [projectsResponse, levelsResponse] = await Promise.all([
      projectsApi.getAll(),
      levelsApi.getAll()
    ]);

    proyectos.value = projectsResponse.data;
    niveles.value = levelsResponse.data;
  } catch (error) {
    console.error('Error fetching proyectos:', error);
    modalStore.showAlert('Error al cargar los proyectos');
  }
}

async function handleDelete(projectId) {
  const confirmed = await modalStore.showConfirm('¿Está seguro que desea eliminar este proyecto?', 'Confirmar eliminación');

  if (confirmed) {
    try {
      await projectsApi.delete(projectId);
      await fetchProjects();
      modalStore.showAlert('Proyecto eliminado exitosamente', 'Éxito');
    } catch (error) {
      console.error('Error eliminando proyecto:', error);
      modalStore.showAlert('Ocurrió un error al eliminar el proyecto', 'Error');
    }
  }
}

function handleEdit(proyecto) {
  modalStore.openEditModal(proyecto);
}

onMounted(() => {
  fetchProjects();
});
</script>