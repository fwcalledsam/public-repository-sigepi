<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative w-full max-w-md lg:max-w-4xl rounded-lg bg-background p-6 shadow-lg">
        <div class="flex flex-col space-y-1.5">
          <h3 class="text-lg font-semibold leading-none tracking-tight">
            {{ mode === "create" ? "Nueva Asignación" : "Editar Asignación" }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ mode === "create"
              ? "Asigne una persona a un proyecto con roles específicos."
              : "Modifique los detalles de la asignación." }}
          </p>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="grid lg:grid-cols-2 gap-4 py-4 lg:gap-8">
            <!-- Columna izquierda -->
            <div class="space-y-4">
              <div class="grid gap-2">
                <label for="persona" class="text-sm font-medium leading-none">Persona</label>
                <select id="persona" v-model="formData.personaId"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required :disabled="mode === 'edit'" @change="onPersonSelected">
                  <option value="" disabled>Seleccione una persona</option>
                  <option v-for="persona in personas" :key="persona.person_id" :value="persona.person_id">
                    {{ persona.person_firstname }} {{ persona.person_lastname }}
                  </option>
                </select>
              </div>

              <div class="grid gap-2">
                <label for="proyecto" class="text-sm font-medium leading-none">Proyecto</label>
                <select id="proyecto" v-model="formData.proyectoId"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required :disabled="mode === 'edit'">
                  <option value="" disabled>Seleccione un proyecto</option>
                  <option v-for="proyecto in proyectos" :key="proyecto.project_id" :value="proyecto.project_id">
                    {{ proyecto.project_name }}
                  </option>
                </select>
              </div>

              <!-- Sección de roles actuales movida aquí -->
              <div class="grid gap-2" v-if="currentPersonRoles.length > 0">
                <label class="text-sm font-medium leading-none">Roles actuales en el proyecto</label>
                <div class="border rounded-md p-4">
                  <p class="text-sm text-muted-foreground mb-2">
                    Esta persona tiene los siguientes roles asignados actualmente:
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <Badge v-for="role in currentPersonRoles" :key="role.role_id" variant="secondary">
                      {{ getRoleName(role.role_id) }}
                    </Badge>
                  </div>
                </div>
              </div>
            </div>

            <!-- Columna derecha -->
            <div class="space-y-4">
              <div class="grid gap-2">
                <label class="text-sm font-medium leading-none">Roles</label>
                <div class="border rounded-md">
                  <div class="p-2 border-b">
                    <input placeholder="Buscar roles..." v-model="searchTerm"
                      class="flex h-8 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
                  </div>
                  <div class="h-52 overflow-auto">
                    <div class="p-2 space-y-2">
                      <div v-if="filteredRoles.length === 0" class="py-6 text-center text-sm text-muted-foreground">
                        No se encontraron roles.
                      </div>
                      <div v-else v-for="role in filteredRoles" :key="role.role_id" class="flex items-center space-x-2">
                        <input type="checkbox" :id="`role-${role.role_id}`"
                          :checked="formData.roles.includes(role.role_id)" @change="handleRoleToggle(role.role_id)"
                          class="h-4 w-4 rounded border-primary text-primary focus:ring-primary" />
                        <label :for="`role-${role.role_id}`"
                          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer">
                          {{ role.role_description }}
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="formData.roles.length > 0" class="flex flex-wrap gap-2 mt-2">
                  <Badge v-for="roleId in formData.roles" :key="roleId" variant="secondary"
                    class="flex items-center gap-1">
                    {{ getRoleName(roleId) }}
                    <button type="button" @click="removeRole(roleId)"
                      class="rounded-full h-4 w-4 inline-flex items-center justify-center text-muted-foreground hover:bg-muted hover:text-foreground">
                      <X class="h-3 w-3" />
                      <span class="sr-only">Eliminar {{ getRoleName(roleId) }}</span>
                    </button>
                  </Badge>
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-end space-x-2">
            <Button type="button" variant="outline" @click="onClose">
              Cancelar
            </Button>
            <Button type="submit" :disabled="formData.roles.length === 0 || isLoading">
              {{ mode === "create" ? "Crear Asignación" : "Guardar Cambios" }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import Button from '../../common/Button.vue'
import Badge from '../../common/Badge.vue'
import { X } from 'lucide-vue-next'
import {
  personsApi,
  projectsApi,
  rolesApi,
  stakeholdersApi,
  projectStakeholdersApi
} from '../../../lib/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  onClose: {
    type: Function,
    required: true
  },
  asignacion: {
    type: Object,
    default: () => ({})
  },
  mode: {
    type: String,
    required: true,
    validator: (value) => ['create', 'edit'].includes(value)
  }
})

const emit = defineEmits(['success'])

const personas = ref([])
const proyectos = ref([])
const roles = ref([])
const searchTerm = ref('')
const currentPersonRoles = ref([])
const isLoading = ref(false)

const formData = ref({
  personaId: '',
  proyectoId: '',
  roles: []
})

watch(() => props.isOpen, (isOpen) => {
  if (!isOpen) {
    formData.value = {
      personaId: '',
      proyectoId: '',
      roles: []
    }
    currentPersonRoles.value = []
    searchTerm.value = ''
  }
})

const loadInitialData = async () => {
  try {
    const [personsRes, projectsRes, rolesRes] = await Promise.all([
      personsApi.getAll().catch(() => ({ data: [] })),
      projectsApi.getAll().catch(() => ({ data: [] })),
      rolesApi.getAll().catch(() => ({ data: [] }))
    ])

    personas.value = personsRes.data || []
    proyectos.value = projectsRes.data || []
    roles.value = rolesRes.data || []

    if (props.mode === 'create' && props.asignacion?.proyectoId) {
      formData.value.proyectoId = String(props.asignacion.proyectoId)
    }

    if (props.mode === 'edit' && props.asignacion?.id) {
      await loadAssignmentData(props.asignacion.id)
    }
  } catch (error) {
    console.error('Error loading initial data:', error)
    alert('Error al cargar los datos iniciales. Por favor intente nuevamente.')
  }
}

const loadAssignmentData = async (prjStkId) => {
  try {
    const [stakeholdersRes, projectStakeholdersRes] = await Promise.all([
      stakeholdersApi.getAll().catch(() => ({ data: [] })),
      projectStakeholdersApi.getAll().catch(() => ({ data: [] }))
    ])

    const prjStk = projectStakeholdersRes.data?.find(ps => ps?.prj_stk_id === prjStkId)
    if (!prjStk) throw new Error('Asignación no encontrada')

    const stakeholder = stakeholdersRes.data?.find(s => s?.stakeholder_id === prjStk?.stakeholder_id)
    if (!stakeholder) throw new Error('Persona no encontrada')

    currentPersonRoles.value = stakeholdersRes.data?.filter(
      s => s?.person_id === stakeholder?.person_id
    ) || []

    const projectStakeholders = projectStakeholdersRes.data?.filter(
      ps => ps?.project_id === prjStk?.project_id
    ) || []

    const projectRoles = stakeholdersRes.data
      ?.filter(s => projectStakeholders.some(ps => ps?.stakeholder_id === s?.stakeholder_id))
      ?.map(s => s?.role_id)
      ?.filter(Boolean) || []

    formData.value = {
      personaId: String(stakeholder.person_id),
      proyectoId: String(prjStk.project_id),
      roles: [...new Set(projectRoles)]
    }
  } catch (error) {
    console.error('Error loading assignment data:', error)
    alert(`Error al cargar los datos: ${error.message}`)
  }
}

const onPersonSelected = async () => {
  if (!formData.value.personaId) return

  try {
    const stakeholdersRes = await stakeholdersApi.getAll()
    currentPersonRoles.value = stakeholdersRes.data?.filter(
      s => s?.person_id === parseInt(formData.value.personaId)) || []

    if (props.mode === 'create' && currentPersonRoles.value.length > 0) {
      const firstRoleId = currentPersonRoles.value[0]?.role_id
      if (firstRoleId && !formData.value.roles.includes(firstRoleId)) {
        formData.value.roles = [firstRoleId]
      }
    }
  } catch (error) {
    console.error('Error getting person roles:', error)
    currentPersonRoles.value = []
  }
}

const filteredRoles = computed(() => {
  if (!Array.isArray(roles.value)) return []

  return roles.value.filter(role =>
    role?.role_description?.toLowerCase()?.includes(searchTerm.value.toLowerCase()) &&
    !formData.value.roles.includes(role?.role_id)
  )
})

const getRoleName = (roleId) => {
  const role = roles.value.find(r => r?.role_id === roleId)
  return role?.role_description || 'Rol desconocido'
}

const handleRoleToggle = (roleId) => {
  if (!roleId) return

  const roles = [...formData.value.roles]
  const roleIndex = roles.indexOf(roleId)

  if (roleIndex > -1) {
    roles.splice(roleIndex, 1)
  } else {
    roles.push(roleId)
  }

  formData.value.roles = roles
}

const removeRole = (roleId) => {
  formData.value.roles = formData.value.roles.filter(r => r !== roleId)
}

const handleSubmit = async () => {
  console.group('🚀 Iniciando proceso de asignación');
  console.log('📝 Datos del formulario:', {
    personaId: formData.value.personaId,
    proyectoId: formData.value.proyectoId,
    roles: formData.value.roles,
    modo: props.mode
  });

  if (formData.value.roles.length === 0) {
    console.warn('⚠️ No hay roles seleccionados');
    alert('Debe seleccionar al menos un rol');
    console.groupEnd();
    return;
  }

  isLoading.value = true;

  try {
    if (!formData.value.personaId || !formData.value.proyectoId) {
      console.error('❌ Datos incompletos');
      throw new Error('Datos incompletos');
    }

    console.group('📊 Obteniendo datos existentes');
    const [existingProjectStakeholdersRes, stakeholdersRes] = await Promise.all([
      projectStakeholdersApi.getAll().catch(() => ({ data: [] })),
      stakeholdersApi.getAll().catch(() => ({ data: [] }))
    ]);

    const existingProjectStakeholders = existingProjectStakeholdersRes.data?.filter(
      ps => ps?.project_id === parseInt(formData.value.proyectoId)
    ) || [];

    const personStakeholders = stakeholdersRes.data?.filter(
      s => s?.person_id === parseInt(formData.value.personaId)
    ) || [];

    console.log('👥 Stakeholders existentes del proyecto:', existingProjectStakeholders);
    console.log('👤 Stakeholders de la persona:', personStakeholders);
    console.groupEnd();

    const processedStakeholderIds = [];

    console.group('🔄 Procesando roles');
    for (const roleId of formData.value.roles) {
      console.group(`📌 Procesando rol ${roleId}`);
      try {
        let existingStakeholder = personStakeholders.find(s => s?.role_id === roleId);
        let stakeholderId;

        if (existingStakeholder) {
          stakeholderId = existingStakeholder.stakeholder_id;
          console.log('✨ Stakeholder existente encontrado:', {
            stakeholderId,
            roleId
          });

          const relationExists = existingProjectStakeholders.some(
            ps => ps?.stakeholder_id === stakeholderId
          );

          if (relationExists) {
            console.log('🔄 Relación ya existe, saltando...');
            processedStakeholderIds.push(stakeholderId);
            console.groupEnd();
            continue;
          }
        } else {
          console.log('🆕 Creando nuevo stakeholder para el rol:', roleId);
          const newStakeholder = await stakeholdersApi.create({
            person_id: parseInt(formData.value.personaId),
            role_id: roleId
          });
          stakeholderId = newStakeholder.data?.stakeholder_id ||
            newStakeholder.stakeholder_id ||
            newStakeholder.data?.id;

          console.log('✅ Nuevo stakeholder creado:', stakeholderId);
        }

        console.log('📝 Creando asignación al proyecto:', {
          project_id: parseInt(formData.value.proyectoId),
          stakeholder_id: stakeholderId
        });

        await projectStakeholdersApi.create({
          project_id: parseInt(formData.value.proyectoId),
          stakeholder_id: stakeholderId
        });

        processedStakeholderIds.push(stakeholderId);
      } catch (error) {
        console.error(`❌ Error procesando rol ${roleId}:`, error);
        continue;
      }
      console.groupEnd();
    }
    console.groupEnd();

    if (props.mode === 'edit') {
      console.group('✏️ Modo edición - Removiendo roles no seleccionados');
      const rolesToRemove = existingProjectStakeholders.filter(ps =>
        personStakeholders.some(s =>
          s?.stakeholder_id === ps?.stakeholder_id &&
          !formData.value.roles.includes(s?.role_id)
        ));

      console.log('🗑️ Roles a eliminar:', rolesToRemove);

      for (const ps of rolesToRemove) {
        try {
          await projectStakeholdersApi.delete(ps.prj_stk_id);
          console.log(`✅ Eliminada asignación: ${ps.prj_stk_id}`);
        } catch (error) {
          console.error('❌ Error eliminando asignación:', error);
        }
      }
      console.groupEnd();
    }

    console.log('✅ Proceso completado exitosamente');
    emit('success', {
      action: props.mode === 'create' ? 'create' : 'edit',
      message: props.mode === 'create' ? 'Asignación creada con éxito' : 'Asignación actualizada con éxito',
      data: {
        processedStakeholderIds,
        personId: formData.value.personaId,
        projectId: formData.value.proyectoId,
        roles: formData.value.roles
      }
    });

    props.onClose();
  } catch (error) {
    console.error('❌ Error en el proceso:', error);
    alert(`Error: ${error.message || 'No se pudo completar la operación'}`);
  } finally {
    isLoading.value = false;
    console.groupEnd();
  }
};

onMounted(loadInitialData)
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