<template>
  <div class="space-y-2">
    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Niveles de Proyecto</h2>
        <Button v-if="levels.length > 0" @click="modalStore.openCreateModal()" class="md:size-default">
          <TblrSettings class="h-4 w-4" />
          <span class="hidden md:inline ml-2">Nuevo Nivel</span>
        </Button>
      </div>
      <div class="relative w-full max-w-sm">
        <HrsldSearch class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <input type="search" placeholder="Buscar por nombre..."
          class="flex h-8 w-full rounded-md border border-input bg-background px-3 py-1 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          v-model="searchTerm" />
      </div>
    </div>

    <!-- Vista móvil (cards) -->
    <div v-if="filteredLevels.length > 0" class="md:hidden space-y-2">
      <div v-for="lvl in filteredLevels" :key="lvl.level_id" class="p-4 border rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">{{ lvl.level_description }}</h3>
            <p class="text-sm text-muted-foreground">{{ countByLevel[lvl.level_id] || 0 }} proyectos activos</p>
          </div>
          <div class="flex space-x-1">
            <Button variant="ghost" size="sm" @click="handleEdit(lvl)" class="p-2">
              <TblrEdit class="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" @click="handleDelete(lvl)" class="p-2 text-red-600 hover:text-red-800">
              <HrsldTrash class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista desktop (tabla) -->
    <div v-if="filteredLevels.length > 0" class="hidden md:block rounded-md border">
      <!-- Contenedor con scroll -->
      <div :style="{ 'max-height': containerHeight + 'px' }" class="overflow-auto">
        <table class="w-full">
          <thead class="sticky top-0 bg-white shadow-md">
            <tr class="border-b bg-muted/50">
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Nombre del Nivel</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Proyectos Activos</th>
              <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lvl in filteredLevels" :key="lvl.level_id" class="border-b">
              <td class="p-4 align-middle font-medium">{{ lvl.level_description }}</td>
              <td class="p-4 align-middle">
                {{ countByLevel[lvl.level_id] || 0 }}
              </td>
              <td class="p-4 align-middle text-right space-x-2">
                <Button variant="ghost" size="sm" @click="handleEdit(lvl)">
                  <TblrEdit class="mr-2 h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" @click="handleDelete(lvl)" class="text-red-600 hover:text-red-800">
                  <HrsldTrash class="mr-2 h-4 w-4" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


    <EmptyState v-else title="No hay niveles registrados" description="Comience creando su primer nivel"
      actionText="Crear primer nivel" :icon="TblrSettings" :onAction="modalStore.openCreateModal" />
  </div>
  <!-- Modales -->
  <NivelModal :is-open="modalStore.isCreateModalOpen" :on-close="modalStore.closeCreateModal" mode="create"
    @success="handleSuccess" />

  <NivelModal v-if="modalStore.currentItem" :is-open="modalStore.isEditModalOpen" :on-close="modalStore.closeEditModal"
    :nivel="modalStore.currentItem" mode="edit" @success="handleSuccess" />

  <!-- Alert Modal -->
  <AlertModal :is-open="modalStore.isAlertOpen" :on-close="modalStore.closeAlert" :title="modalStore.alertConfig.title"
    :message="modalStore.alertConfig.message" :confirm-text="modalStore.alertConfig.confirmText"
    :cancel-text="modalStore.alertConfig.cancelText" :loading-text="modalStore.alertConfig.loadingText"
    :confirm-variant="modalStore.alertConfig.confirmVariant" :show-cancel="modalStore.alertConfig.showCancel"
    :on-confirm="modalStore.alertConfig.onConfirm" />

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { levelsApi, projectsApi } from '../../lib/api'
import { useContainerHeight } from '../../utils/calculateContainerHeight'
import { useModalStore } from '../../stores/modal'
import Button from '../../components/common/Button.vue'
import NivelModal from '../../components/modals/projects/NivelModal.vue'
import AlertModal from '../../components/modals/general/AlertModal.vue'
import EmptyState from '../../components/common/EmptyState.vue'

const { containerHeight } = useContainerHeight()
const modalStore = useModalStore()
const levels = ref([])
const countByLevel = ref({})
const searchTerm = ref('')

const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

const sortedLevels = computed(() => {
  return [...levels.value].sort((a, b) => b.level_id - a.level_id)
})

const filteredLevels = computed(() => {
  if (!searchTerm.value.trim()) return sortedLevels.value

  const searchTermNormalized = normalizeString(searchTerm.value)
  return sortedLevels.value.filter(lvl =>
    normalizeString(lvl.level_description).includes(searchTermNormalized))
})

async function fetchData() {
  try {
    const [levelsResponse, projectsResponse] = await Promise.all([
      levelsApi.getAll(),
      projectsApi.getAll()
    ])

    // Procesar niveles
    levels.value = levelsResponse.data.map(lvl => ({
      level_id: lvl.level_id,
      level_description: lvl.level_description
    }))

    // Contar proyectos por nivel
    const counts = {}
    projectsResponse.data.forEach(project => {
      const levelId = project.level_id
      if (levelId) {
        counts[levelId] = (counts[levelId] || 0) + 1
      }
    })
    countByLevel.value = counts

  } catch (error) {
    console.error('Error cargando datos:', error)
    modalStore.showAlert('Error al cargar los datos. Por favor recarga la página.', 'Error')
  }
}

onMounted(fetchData)

function handleEdit(nivel) {
  modalStore.openEditModal({
    level_id: nivel.level_id,
    level_description: nivel.level_description
  })
}

async function handleDelete(nivel) {
  const projectCount = countByLevel.value[nivel.level_id] || 0

  if (projectCount > 0) {
    modalStore.showAlert('No se puede eliminar un nivel que tiene proyectos asignados', 'Acción no permitida')
    return
  }

  const confirmed = await modalStore.showConfirm(
    `¿Estás seguro de que deseas eliminar el nivel "${nivel.level_description}"?`,
    'Confirmar eliminación'
  )

  if (!confirmed) return

  try {
    await levelsApi.delete(nivel.level_id)
    await fetchData()
    modalStore.showAlert('Nivel eliminado exitosamente', 'Éxito')
  } catch (error) {
    console.error('Error al eliminar el nivel:', error)
    modalStore.showAlert(
      error.response?.data?.message || 'Ocurrió un error al eliminar el nivel',
      'Error'
    )
  }
}

function handleSuccess({ message }) {
  fetchData()
  modalStore.showAlert(message, 'Éxito')
}
</script>

<style scoped>
.text-red-600 {
  color: #dc2626;
}

.text-red-600:hover {
  color: #991b1b;
}
</style>