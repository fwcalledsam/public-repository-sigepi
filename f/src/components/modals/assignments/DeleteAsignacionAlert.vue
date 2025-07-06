<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
        <div class="flex flex-col space-y-2">
          <h3 class="text-lg font-semibold leading-none tracking-tight">
            ¿Está seguro de eliminar esta asignación?
          </h3>
          <p class="text-sm text-muted-foreground">
            Esta acción eliminará la asignación de <strong>{{ safeAsignacion.persona || 'la persona' }}</strong> como
            <strong>{{ rolesNames }}</strong> en el proyecto <strong>{{ safeAsignacion.proyecto || 'el proyecto'
              }}</strong>.
            Esta acción no se puede deshacer.
          </p>
        </div>
        <div class="flex justify-end space-x-2 mt-6">
          <Button type="button" variant="outline" @click="onClose">
            Cancelar
          </Button>
          <Button type="button" variant="destructive" @click="handleDelete" :disabled="isLoading">
            <span v-if="isLoading">Eliminando...</span>
            <span v-else>Eliminar</span>
          </Button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, ref } from 'vue'
import Button from '../../common/Button.vue'
import { projectStakeholdersApi, stakeholdersApi, personsApi, rolesApi } from '../../../lib/api'

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
  }
})

const emit = defineEmits(['success'])
const isLoading = ref(false)

const safeAsignacion = computed(() => ({
  persona: props.asignacion?.persona || 'Persona desconocida',
  proyecto: props.asignacion?.proyecto || 'Proyecto desconocido',
  rol: props.asignacion?.rol || [],
  id: props.asignacion?.id
}))

const rolesNames = computed(() => {
  const roles = safeAsignacion.value.rol

  if (!roles || !Array.isArray(roles) && typeof roles !== 'object') return 'Rol desconocido'

  const rolesArray = Array.isArray(roles) ? roles : [roles]

  return rolesArray
    .map(role => {
      if (!role) return 'Rol desconocido'
      return typeof role === 'object'
        ? role.nombre || role.name || role.role_description || 'Rol desconocido'
        : role
    })
    .filter(Boolean)
    .join(", ") || 'Rol desconocido'
})

const handleDelete = async () => {
  if (!props.asignacion?.stakeholder_id || !props.asignacion?.proyectoId) {
    console.error('No se puede eliminar: IDs no válidos')
    alert('No se puede eliminar la asignación. Falta información requerida.')
    return
  }

  isLoading.value = true
  try {
    console.log('🔄 Iniciando proceso de eliminación...')
    
    // 1. Obtener todos los project_stakeholders y stakeholders
    console.log('📥 Obteniendo project_stakeholders y stakeholders...')
    const [projectStakeholdersResponse, stakeholdersResponse] = await Promise.all([
      projectStakeholdersApi.getAll(),
      stakeholdersApi.getAll()
    ])
    console.log('✅ Datos obtenidos:', {
      projectStakeholders: projectStakeholdersResponse.data,
      stakeholders: stakeholdersResponse.data
    })
    
    // 2. Encontrar todos los stakeholders de la persona con los roles específicos
    console.log('🔍 Filtrando stakeholders de la persona...')
    const personStakeholders = stakeholdersResponse.data.filter(s => 
      s.person_id === props.asignacion.personaId
    )
    console.log('✅ Stakeholders de la persona:', personStakeholders)

    // 3. Filtrar project_stakeholders que corresponden a esta asignación
    console.log('🔍 Filtrando project_stakeholders para esta asignación...')
    const assignmentsToDelete = projectStakeholdersResponse.data.filter(ps => 
      ps.project_id === props.asignacion.proyectoId && 
      personStakeholders.some(s => s.stakeholder_id === ps.stakeholder_id)
    )
    console.log('✅ Asignaciones a eliminar:', assignmentsToDelete)

    console.group('📝 Resumen de eliminación:')
    console.log('Persona:', props.asignacion.persona)
    console.log('Proyecto:', props.asignacion.proyecto)
    console.log('Roles:', props.asignacion.rol.map(r => r.name).join(', '))
    console.log('Asignaciones a eliminar:', assignmentsToDelete)
    console.groupEnd()

    let eliminados = 0
    
    // 4. Eliminar cada project_stakeholder
    for (const assignment of assignmentsToDelete) {
      try {
        console.log(`🗑️ Eliminando asignación ${assignment.prj_stk_id}...`)
        await projectStakeholdersApi.delete(assignment.prj_stk_id)
        console.log(`✅ Asignación ${assignment.prj_stk_id} eliminada exitosamente`)
        eliminados++
      } catch (error) {
        if (error.response?.status === 404) {
          console.warn(`⚠️ La asignación ${assignment.prj_stk_id} ya fue eliminada`)
          continue
        }
        console.error(`❌ Error al eliminar asignación ${assignment.prj_stk_id}:`, error)
        throw error
      }
    }

    console.log(`✅ Proceso de eliminación completado. Total eliminados: ${eliminados}`)

    emit('success', {
      action: 'delete',
      message: `Se eliminaron exitosamente ${eliminados} asignaciones de ${props.asignacion.persona} en el proyecto ${props.asignacion.proyecto}`,
      deletedInfo: {
        persona: props.asignacion.persona,
        proyecto: props.asignacion.proyecto,
        roles: props.asignacion.rol,
        eliminados
      }
    })

    props.onClose()

  } catch (error) {
    console.error('❌ Error en el proceso:', error)
    alert('Error: No se pudo completar la eliminación de las asignaciones')
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