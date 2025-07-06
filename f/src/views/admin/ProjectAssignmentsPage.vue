<template>
  <div class="space-y-2">
    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Asignaciones de Proyectos</h2>
        <Button v-if="hasAssignments" @click="modalStore.openCreateModal()" class="hidden md:flex">
          <TblrLayersLinked class="mr-2 h-4 w-4" />
          Nueva Asignación
        </Button>
      </div>

      <div class="md:hidden bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
        <TblrDeviceLaptop class="mx-auto h-8 w-8 text-blue-500 mb-2" />
        <h3 class="font-medium text-blue-800">Acceso desde computador requerido</h3>
        <p class="text-sm text-blue-600 mt-1">
          Para modificar las asignaciones de proyectos, por favor acceda desde un computador.
        </p>
      </div>

      <!-- Barra de búsqueda agregada -->
      <div class="relative w-full max-w-sm">
        <HrsldSearch class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <input type="search" placeholder="Buscar por proyecto o persona..."
          class="flex h-8 w-full rounded-md border border-input bg-background px-3 py-1 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          v-model="searchTerm" />
      </div>
    </div>

    <!-- Vista móvil (cards) -->
    <div v-if="hasAssignments" class="md:hidden space-y-3">
      <div v-for="[projectId, projectData] in Object.entries(filteredProjectGroups)" :key="projectId"
        class="border rounded-lg overflow-hidden">
        <div class="p-4 bg-gray-200 border-b">
          <h3 class="font-medium">{{ projectData.name }}</h3>
        </div>

        <div class="divide-y">
          <div v-for="assignment in projectData.assignments" :key="assignment.id" class="p-4">
            <div class="flex justify-between items-start">
              <div>
                <p class="font-medium">{{ assignment.persona }}</p>
                <div class="mt-1 flex flex-wrap gap-1">
                  <template v-if="Array.isArray(assignment.rol)">
                    <Badge v-for="(rol, index) in assignment.rol" :key="index" class="text-xs">
                      {{ rol.name }}
                    </Badge>
                  </template>
                  <template v-else>
                    <Badge class="text-xs">
                      {{ assignment.rol.name }}
                    </Badge>
                  </template>
                </div>
              </div>
              <!-- <div class="flex space-x-1">
                <Button variant="ghost" size="sm" @click="handleEdit(assignment)" class="p-2">
                  <TblrEdit class="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" @click="handleDelete(assignment)"
                  class="p-2 text-red-600 hover:text-red-800">
                  <HrsldTrash class="h-4 w-4" />
                </Button>
              </div> -->
            </div>
          </div>
        </div>

        <!-- <div class="p-3 bg-gray-50 border-t">
          <Button variant="outline" size="sm"
            @click="handleAddPerson({ projectId: parseInt(projectId), projectName: projectData.name })" class="w-full">
            <TblrPlus class="mr-2 h-4 w-4" />
            Agregar persona
          </Button>
        </div> -->
      </div>
    </div>

    <!-- Vista desktop (collapsible) -->
    <div v-if="hasAssignments" class="hidden md:block rounded-md border">
      <div :style="{ 'max-height': containerHeight + 'px' }" class="overflow-auto">
        <ProjectCollapsible v-for="[projectId, projectData] in Object.entries(filteredProjectGroups)" :key="projectId"
          :project-name="projectData.name" :project-id="parseInt(projectId)" :assignments="projectData.assignments"
          @edit="handleEdit" @delete="handleDelete" @add-person="handleAddPerson" />
      </div>
    </div>

    <EmptyState v-else title="No hay asignaciones registradas" description="Comience creando su primera asignacion"
      actionText="Crear asignacion" :icon="TblrSettings" :onAction="modalStore.openCreateModal" />
  </div>

  <!-- Modals (se mantienen igual) -->
  <AsignacionModal :is-open="modalStore.isCreateModalOpen" :on-close="modalStore.closeCreateModal" mode="create"
    @success="handleSuccess" />

  <EditAsignacionModal v-if="modalStore.currentItem" :is-open="modalStore.isEditModalOpen"
    :on-close="modalStore.closeEditModal" :asignacion="modalStore.currentItem" @success="handleSuccess" />

  <DeleteAsignacionAlert v-if="modalStore.currentItem" :is-open="modalStore.isDeleteAlertOpen"
    :on-close="modalStore.closeDeleteAlert" :asignacion="modalStore.currentItem" @success="handleSuccess" />

  <AlertModal :is-open="modalStore.isAlertOpen" :on-close="modalStore.closeAlert" :title="modalStore.alertConfig.title"
    :message="modalStore.alertConfig.message" :confirm-text="modalStore.alertConfig.confirmText"
    :cancel-text="modalStore.alertConfig.cancelText" :loading-text="modalStore.alertConfig.loadingText"
    :confirm-variant="modalStore.alertConfig.confirmVariant" :show-cancel="modalStore.alertConfig.showCancel"
    :on-confirm="modalStore.alertConfig.onConfirm" />
</template>

<script setup>
import { useModalStore } from '../../stores/modal'
import {
  projectsApi,
  personsApi,
  rolesApi,
  stakeholdersApi,
  projectStakeholdersApi
} from '../../lib/api'
import { onMounted, ref, computed } from 'vue'
import Button from '../../components/common/Button.vue'
import ProjectCollapsible from '../../components/cards/ProjectCollapsible.vue'
import AsignacionModal from '../../components/modals/assignments/AsignacionModal.vue'
import EditAsignacionModal from '../../components/modals/assignments/EditAsignacionModal.vue'
import DeleteAsignacionAlert from '../../components/modals/assignments/DeleteAsignacionAlert.vue'
import AlertModal from '../../components/modals/general/AlertModal.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { useContainerHeight } from '../../utils/calculateContainerHeight'

const { containerHeight } = useContainerHeight()
const modalStore = useModalStore()
const projectGroups = ref({})
const searchTerm = ref('')
const isLoading = ref(false)

// Función para normalizar texto (elimina acentos y convierte a minúsculas)
const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

// Ordenar proyectos por ID descendente (últimos primero)
const sortedProjectGroups = computed(() => {
  const sorted = {}
  Object.keys(projectGroups.value)
    .sort((a, b) => b - a) // Orden descendente por projectId
    .forEach(key => {
      sorted[key] = projectGroups.value[key]
    })
  return sorted
})

// Filtrar proyectos y asignaciones según término de búsqueda
const filteredProjectGroups = computed(() => {
  if (!searchTerm.value.trim()) return sortedProjectGroups.value

  const searchTermNormalized = normalizeString(searchTerm.value)
  const filtered = {}

  Object.entries(sortedProjectGroups.value).forEach(([projectId, projectData]) => {
    // Buscar en nombre del proyecto
    const projectNameMatch = normalizeString(projectData.name).includes(searchTermNormalized)

    // Buscar en nombres de personas asignadas
    const hasPersonMatch = projectData.assignments.some(assignment =>
      normalizeString(assignment.persona).includes(searchTermNormalized)
    )

    if (projectNameMatch || hasPersonMatch) {
      filtered[projectId] = {
        ...projectData,
        // Si hay término de búsqueda, filtrar también las asignaciones que coincidan
        assignments: searchTerm.value.trim()
          ? projectData.assignments.filter(assignment =>
            normalizeString(assignment.persona).includes(searchTermNormalized) ||
            normalizeString(projectData.name).includes(searchTermNormalized)
          )
          : projectData.assignments
      }
    }
  })

  return filtered
})

const hasAssignments = computed(() => {
  return Object.keys(projectGroups.value).length > 0
})

const loadData = async () => {
  isLoading.value = true
  try {
    // ---------------------------------------
    const [
      projectsRes,
      personsRes,
      rolesRes,
      stakeholdersRes,
      projectStakeholdersRes
    ] = await Promise.all([
      projectsApi.getAll().catch(e => ({ data: null, error: e })),
      personsApi.getAll().catch(e => ({ data: null, error: e })),
      rolesApi.getAll().catch(e => ({ data: null, error: e })),
      stakeholdersApi.getAll().catch(e => ({ data: null, error: e })),
      projectStakeholdersApi.getAll().catch(e => ({ data: null, error: e }))
    ])

    const responses = [projectsRes, personsRes, rolesRes, stakeholdersRes, projectStakeholdersRes]
    const errors = responses.filter(r => r.error)
    if (errors.length > 0) {
      throw new Error(`API errors: ${errors.map(e => e.error.message).join(', ')}`)
    }

    const projectsData = projectsRes.data || []
    const personsData = personsRes.data || []
    const rolesData = rolesRes.data || []
    const stakeholdersData = stakeholdersRes.data || []
    const projectStakeholdersData = projectStakeholdersRes.data || []

    const projectsMap = projectsData.reduce((acc, project) => {
      if (project?.project_id) {
        acc[project.project_id] = project.project_name
      }
      return acc
    }, {})

    const personsMap = personsData.reduce((acc, person) => {
      if (person?.person_id) {
        acc[person.person_id] = {
          name: `${person.person_firstname || ''} ${person.person_lastname || ''}`.trim(),
          id: person.person_id
        }
      }
      return acc
    }, {})

    const rolesMap = rolesData.reduce((acc, role) => {
      if (role?.role_id) {
        acc[role.role_id] = role.role_description
      }
      return acc
    }, {})

    const groups = {}

    projectStakeholdersData.forEach(ps => {
      if (!ps?.stakeholder_id || !ps?.project_id) return

      const stakeholder = stakeholdersData.find(s => s.stakeholder_id === ps.stakeholder_id)
      if (!stakeholder?.person_id || !stakeholder?.role_id) return

      const projectId = ps.project_id
      const personId = stakeholder.person_id
      const roleId = stakeholder.role_id
      const personInfo = personsMap[personId] || { name: `Persona ${personId}`, id: personId }

      if (!groups[projectId]) {
        groups[projectId] = {
          name: projectsMap[projectId] || `Proyecto ${projectId}`,
          assignments: []
        }
      }

      const existingAssignmentIndex = groups[projectId].assignments.findIndex(
        a => a.personaId === personId
      )

      if (existingAssignmentIndex >= 0) {
        const existingAssignment = groups[projectId].assignments[existingAssignmentIndex]
        const newRole = {
          id: roleId,
          name: rolesMap[roleId] || `Rol ${roleId}`
        }

        if (Array.isArray(existingAssignment.rol)) {
          existingAssignment.rol.push(newRole)
        } else {
          existingAssignment.rol = [existingAssignment.rol, newRole]
        }
      } else {
        groups[projectId].assignments.push({
          id: ps.prj_stk_id,
          personaId: personId,
          persona: personInfo.name,
          proyectoId: projectId,
          proyecto: projectsMap[projectId] || `Proyecto ${projectId}`,
          rol: {
            id: roleId,
            name: rolesMap[roleId] || `Rol ${roleId}`
          },
          stakeholder_id: ps.stakeholder_id
        })
      }
    })

    // ---------------------------------------
    projectGroups.value = groups
  } catch (error) {
    console.error('Error fetching data:', error)
    modalStore.showAlert(`Error al cargar los datos: ${error.message}`, 'Error')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})

function handleDelete(asignacion) {
  const deleteData = {
    id: asignacion.id,
    persona: asignacion.persona,
    personaId: asignacion.personaId || asignacion.person_id, // Fallback alternativo
    proyecto: asignacion.proyecto,
    proyectoId: asignacion.proyectoId || asignacion.project_id, // Fallback alternativo
    rol: Array.isArray(asignacion.rol) ? asignacion.rol : [asignacion.rol],
    stakeholder_id: asignacion.stakeholder_id,
    ...(asignacion.prj_stk_id && { prj_stk_id: asignacion.prj_stk_id }),
    ...(asignacion.project_name && { project_name: asignacion.project_name }),
    ...(asignacion.person_name && { person_name: asignacion.person_name })
  }

  // console.log("Datos completos para eliminar:", JSON.parse(JSON.stringify(deleteData)))
  modalStore.openDeleteAlert(deleteData)
}

function handleEdit(asignacion) {
  const editData = {
    id: asignacion.id,
    persona: asignacion.persona,
    personaId: asignacion.personaId,
    proyecto: asignacion.proyecto,
    proyectoId: asignacion.proyectoId,
    rol: Array.isArray(asignacion.rol) ? asignacion.rol : [asignacion.rol],
    stakeholder_id: asignacion.stakeholder_id
  }
  // console.log("Datos a editar:", editData);
  modalStore.openEditModal(editData)
}

function handleAddPerson(projectData) {
  modalStore.currentItem = {
    proyecto: projectData.projectName,
    proyectoId: projectData.projectId
  }
  modalStore.openCreateModal()
}

function handleSuccess({ action, message, data }) {
  if (action === 'delete') {
    modalStore.showAlert(message || 'Asignación eliminada con éxito', 'Éxito')
  }
  loadData()
}
</script>
