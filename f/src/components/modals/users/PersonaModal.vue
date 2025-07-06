<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative w-full max-w-lg rounded-lg bg-background p-6 shadow-lg">
        <div class="flex flex-col space-y-1.5">
          <h3 class="text-lg font-semibold leading-none tracking-tight">
            {{ mode === "create" ? "Nueva Persona" : "Editar Persona" }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ mode === "create"
              ? "Complete los detalles para registrar una nueva persona."
              : "Modifique los detalles de la persona." }}
          </p>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="grid gap-4 py-4">
            <div class="grid grid-cols-2 gap-4">
              <div class="grid gap-2">
                <label for="nombre" class="text-sm font-medium leading-none">Nombre</label>
                <input id="nombre" v-model="formData.person_firstname" placeholder="Nombre"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required />
              </div>
              <div class="grid gap-2">
                <label for="apellido" class="text-sm font-medium leading-none">Apellido</label>
                <input id="apellido" v-model="formData.person_lastname" placeholder="Apellido"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="grid gap-2">
                <label for="ubicacion" class="text-sm font-medium leading-none">Ubicación</label>
                <input id="ubicacion" v-model="formData.person_location" placeholder="Ubicación"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
              </div>
              <div class="grid gap-2">
                <label for="urlsite" class="text-sm font-medium leading-none">Sitio Web</label>
                <input id="urlsite" v-model="formData.person_urlsite" placeholder="https://ejemplo.com" type="url"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
              </div>
            </div>

            <div class="grid gap-2">
              <label class="text-sm font-medium leading-none">Roles Asignados</label>

              <!-- Badges para mostrar roles seleccionados -->
              <div class="flex flex-wrap gap-2 mb-2" v-if="formData.selectedRoles.length > 0">
                <Badge v-for="roleId in formData.selectedRoles" :key="roleId" class="flex items-center gap-1">
                  {{ getRoleDescription(roleId) }}
                  <button type="button" @click="removeRole(roleId)" class="text-xs hover:text-red-500">
                    ×
                  </button>
                </Badge>
              </div>
              <p v-else class="text-sm text-gray-500">No hay roles asignados</p>

              <!-- Select de roles -->
              <div class="relative">
                <select v-model="selectedRoleToAdd" @change="addSelectedRole"
                  class="block w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring">
                  <option value="">Seleccione un rol para agregar</option>
                  <option v-for="role in availableRoles" :key="role.role_id" :value="role.role_id"
                    :disabled="formData.selectedRoles.includes(role.role_id)">
                    {{ role.role_description }}
                  </option>
                </select>
              </div>
              <p v-if="roleError" class="text-sm text-red-500">Debe asignar al menos un rol</p>
            </div>

          </div>
          <div class="flex justify-end space-x-2">
            <Button type="button" variant="outline" @click="onClose">
              Cancelar
            </Button>
            <Button type="submit" :disabled="isLoading">
              <span v-if="isLoading">Procesando...</span>
              <span v-else>{{ mode === "create" ? "Crear Persona" : "Guardar Cambios" }}</span>
            </Button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Button from '../../common/Button.vue'
import Badge from '../../common/Badge.vue'
import { personsApi, rolesApi, stakeholdersApi } from '../../../lib/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  onClose: {
    type: Function,
    required: true
  },
  persona: {
    type: Object,
    default: null
  },
  mode: {
    type: String,
    required: true,
    validator: (value) => ['create', 'edit'].includes(value)
  }
})

const emit = defineEmits(['success'])

const formData = ref({
  person_firstname: '',
  person_lastname: '',
  person_location: '',
  person_urlsite: '',
  selectedRoles: []
})

const availableRoles = ref([])
const selectedRoleToAdd = ref('')
const isLoading = ref(false)
const roleError = ref(false)

// Methods
const getRoleDescription = (roleId) => {
  const role = availableRoles.value.find(r => r.role_id === roleId)
  return role ? role.role_description : 'Rol desconocido'
}

const addSelectedRole = () => {
  if (selectedRoleToAdd.value && !formData.value.selectedRoles.includes(selectedRoleToAdd.value)) {
    formData.value.selectedRoles.push(selectedRoleToAdd.value)
    selectedRoleToAdd.value = ''
    roleError.value = false
  }
}

const removeRole = (roleId) => {
  formData.value.selectedRoles = formData.value.selectedRoles.filter(id => id !== roleId)
}

const loadAvailableRoles = async () => {
  try {
    const response = await rolesApi.getAll()
    availableRoles.value = response.data
  } catch (error) {
    console.error('Error cargando roles:', error)
    alert('Error al cargar los roles disponibles')
  }
}

const loadPersonRoles = async (personId) => {
  if (!personId) return

  try {
    const response = await stakeholdersApi.getAll()
    const baseRoles = response.data
      .filter(s => s.person_id === personId && !s.project_id)
      .map(s => s.role_id)

    formData.value.selectedRoles = [...new Set(baseRoles)]
  } catch (error) {
    console.error('Error cargando roles de persona:', error)
  }
}

const resetForm = () => {
  formData.value = {
    person_firstname: '',
    person_lastname: '',
    person_location: '',
    person_urlsite: '',
    selectedRoles: []
  }
  selectedRoleToAdd.value = ''
  roleError.value = false
}

// Lifecycle hooks
onMounted(async () => {
  await loadAvailableRoles()
  if (props.mode === 'edit' && props.persona) {
    await loadPersonRoles(props.persona.id)
  }
})

watch(() => props.persona, async (newPersona) => {
  if (newPersona) {
    formData.value = {
      person_firstname: newPersona.person_firstname || newPersona.nombre || '',
      person_lastname: newPersona.person_lastname || newPersona.apellido || '',
      person_location: newPersona.person_location || '',
      person_urlsite: newPersona.person_urlsite || '',
      selectedRoles: []
    }
    await loadPersonRoles(newPersona.id)
  } else {
    resetForm()
  }
}, { immediate: true })

async function handleSubmit() {
  if (formData.value.selectedRoles.length === 0) {
    roleError.value = true
    return
  }
  roleError.value = false

  isLoading.value = true
  try {
    if (props.mode === 'create') {
      const personResponse = await personsApi.create({
        firstname: formData.value.person_firstname,
        lastname: formData.value.person_lastname,
        location: formData.value.person_location,
        urlsite: formData.value.person_urlsite
      })

      const personId = personResponse.data?.person_id || personResponse.data?.id
      if (!personId) throw new Error('No se recibió el ID de la persona creada')

      await Promise.all(
        formData.value.selectedRoles.map(roleId =>
          stakeholdersApi.create({
            person_id: personId,
            role_id: roleId
          })
        )
      )

      emit('success', { action: 'create', message: 'Persona creada exitosamente' })
      resetForm()
      props.onClose()
    } else {
      const personId = props.persona.id

      await personsApi.update(personId, {
        firstname: formData.value.person_firstname,
        lastname: formData.value.person_lastname,
        location: formData.value.person_location,
        urlsite: formData.value.person_urlsite
      })

      const stakeholdersRes = await stakeholdersApi.getAll()
      const existingBaseStakeholders = stakeholdersRes.data.filter(
        s => s.person_id === personId && !s.project_id
      )

      const currentRoles = existingBaseStakeholders.map(s => s.role_id)
      const newRoles = formData.value.selectedRoles

      const rolesToAdd = newRoles.filter(roleId => !currentRoles.includes(roleId))
      const rolesToRemove = currentRoles.filter(roleId => !newRoles.includes(roleId))

      await Promise.all([
        ...existingBaseStakeholders
          .filter(s => rolesToRemove.includes(s.role_id))
          .map(s => stakeholdersApi.delete(s.stakeholder_id)),
        ...rolesToAdd.map(roleId =>
          stakeholdersApi.create({
            person_id: personId,
            role_id: roleId
          })
        )
      ])

      emit('success', {
        action: 'update',
        message: 'Persona y roles actualizados correctamente'
      })
      props.onClose()
    }
  } catch (error) {
    console.error('Error al guardar:', error)
    alert(error.message || 'Error al procesar la solicitud')
  } finally {
    isLoading.value = false
  }
}
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