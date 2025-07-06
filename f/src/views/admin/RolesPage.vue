<template>
  <div class="space-y-2">
    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Gestión de Roles</h2>
        <Button v-if="roles.length > 0" @click="modalStore.openCreateModal()" class="md:size-default">
          <TblrCategory class="h-4 w-4" />
          <span class="hidden md:inline ml-2">Nuevo Rol</span>
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
    <div v-if="filteredRoles.length > 0" class="md:hidden space-y-2">
      <div v-for="rol in filteredRoles" :key="rol.role_id" class="p-4 border rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">{{ rol.role_description }}</h3>
            <p class="text-sm text-muted-foreground">{{ countByRole[rol.role_id] || 0 }} personas asignadas</p>
          </div>
          <div class="flex space-x-1">
            <Button variant="ghost" size="sm" @click="handleEdit(rol)" class="p-2">
              <TblrEdit class="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" @click="handleDelete(rol)" class="p-2 text-red-600 hover:text-red-800">
              <HrsldTrash class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista desktop (tabla) -->
    <div v-if="filteredRoles.length > 0" class="hidden md:block rounded-md border">
      <!-- Contenedor con scroll -->
      <div :style="{ 'max-height': containerHeight + 'px' }" class="overflow-auto">
        <table class="w-full">
          <thead class="sticky top-0 bg-white shadow-md">
            <tr class="border-b bg-muted/50">
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Nombre del Rol</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Personas Asignadas</th>
              <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rol in filteredRoles" :key="rol.role_id" class="border-b">
              <td class="p-4 align-middle font-medium">
                {{ rol.role_description }}
              </td>
              <td class="p-4 align-middle">
                <div class="ml-8">
                  {{ countByRole[rol.role_id] || 0 }}
                </div>
              </td>
              <td class="p-4 align-middle text-right space-x-2">
                <Button variant="ghost" size="sm" @click="handleEdit(rol)">
                  <TblrEdit class="mr-2 h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" @click="handleDelete(rol)" class="text-red-600 hover:text-red-800">
                  <HrsldTrash class="mr-2 h-4 w-4" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <EmptyState v-else title="No hay roles registrados" description="Comience creando su primer rol"
      actionText="Crear rol" :icon="TblrSettings" :onAction="modalStore.openCreateModal" />
  </div>
  <!-- Modales -->
  <RolModal :is-open="modalStore.isCreateModalOpen" :on-close="modalStore.closeCreateModal" mode="create"
    @success="handleSuccess" />

  <RolModal v-if="modalStore.currentItem" :is-open="modalStore.isEditModalOpen" :on-close="modalStore.closeEditModal"
    :rol="modalStore.currentItem" mode="edit" @success="handleSuccess" />

  <!-- Alert Modal -->
  <AlertModal :is-open="modalStore.isAlertOpen" :on-close="modalStore.closeAlert" :title="modalStore.alertConfig.title"
    :message="modalStore.alertConfig.message" :confirm-text="modalStore.alertConfig.confirmText"
    :cancel-text="modalStore.alertConfig.cancelText" :loading-text="modalStore.alertConfig.loadingText"
    :confirm-variant="modalStore.alertConfig.confirmVariant" :show-cancel="modalStore.alertConfig.showCancel"
    :on-confirm="modalStore.alertConfig.onConfirm" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { rolesApi, stakeholdersApi } from '../../lib/api'
import { useModalStore } from '../../stores/modal'
import Button from '../../components/common/Button.vue'
// import Badge from '../../components/common/Badge.vue'
import RolModal from '../../components/modals/users/RolModal.vue'
import AlertModal from '../../components/modals/general/AlertModal.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { useContainerHeight } from '../../utils/calculateContainerHeight'

const { containerHeight } = useContainerHeight()
const modalStore = useModalStore()
const roles = ref([])
const countByRole = ref({})
const searchTerm = ref('')

const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

const sortedRoles = computed(() => {
  return [...roles.value].sort((a, b) => b.role_id - a.role_id)
})

const filteredRoles = computed(() => {
  if (!searchTerm.value.trim()) return sortedRoles.value

  const searchTermNormalized = normalizeString(searchTerm.value)
  return sortedRoles.value.filter(rol =>
    normalizeString(rol.role_description).includes(searchTermNormalized))
})

async function fetchRoles() {
  try {
    const response = await rolesApi.getAll()
    roles.value = response.data.map(rol => ({
      role_id: rol.role_id,
      role_description: rol.role_description,
    }))
  } catch (error) {
    console.error("Error cargando roles:", error)
    modalStore.showAlert('Error al cargar los roles', 'Error')
  }
}

async function fetchStakeholdersCount() {
  try {
    const response = await stakeholdersApi.getAll()
    const roleCounts = {}
    response.data.forEach(stakeholder => {
      const roleId = stakeholder.role_id
      roleCounts[roleId] = (roleCounts[roleId] || 0) + 1
    })
    countByRole.value = roleCounts
  } catch (error) {
    console.error("Error cargando stakeholders:", error)
    modalStore.showAlert('Error al cargar las asignaciones de roles', 'Error')
  }
}

async function fetchData() {
  await Promise.all([fetchRoles(), fetchStakeholdersCount()])
}

onMounted(fetchData)

function handleEdit(rol) {
  modalStore.openEditModal({
    role_id: rol.role_id,
    role_description: rol.role_description
  })
}

async function handleDelete(rol) {
  const confirmed = await modalStore.showConfirm(
    `¿Estás seguro de que deseas eliminar el rol "${rol.role_description}"? Esta acción no se puede deshacer.`,
    'Confirmar eliminación'
  )

  if (!confirmed) return

  try {
    // Verificar si el rol está asignado a alguna persona
    if (countByRole.value[rol.role_id] > 0) {
      throw new Error('No se puede eliminar un rol que está asignado a personas')
    }

    await rolesApi.delete(rol.role_id)
    await fetchData()
    modalStore.showAlert('Rol eliminado exitosamente', 'Éxito')
  } catch (error) {
    console.error('Error al eliminar el rol:', error)
    modalStore.showAlert(
      error.response?.data?.message || error.message || 'Ocurrió un error al eliminar el rol',
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