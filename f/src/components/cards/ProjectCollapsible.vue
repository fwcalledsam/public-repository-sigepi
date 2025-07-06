<template>
  <div class="border rounded-lg overflow-hidden">
    <div class="flex items-center justify-between p-4 bg-muted/40 cursor-pointer" @click="isOpen = !isOpen">
      <div class="flex items-center gap-2">
        <template v-if="isOpen">
          <HrsldChevronDown class="h-5 w-5" />
        </template>
        <template v-else>
          <HrsldChevronRight class="h-5 w-5" />
        </template>
        <h3 class="font-medium text-lg max-w-lg truncate">{{ projectName }}</h3>
        <Badge variant="outline">{{ Object.keys(safePersonGroups).length }} personas</Badge>
      </div>
    </div>

    <div v-if="isOpen" class="p-4">
      <div class="grid grid-cols-12 gap-4 py-2 px-4 font-medium text-sm text-muted-foreground">
        <div class="col-span-5">Persona</div>
        <div class="col-span-5">Roles</div>
        <div class="col-span-2 text-right">Acciones</div>
      </div>

      <div class="my-2 h-px bg-border"></div>

      <div class="space-y-1">
        <div v-for="[personName, assignments] in Object.entries(safePersonGroups)" :key="personName"
          class="grid grid-cols-12 gap-4 py-3 px-4 rounded-md hover:bg-muted/50">

          <div class="col-span-5 flex items-center gap-3">
            <div class="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium">
              {{ getInitials(personName) }}
            </div>
            <div class="font-medium">{{ personName }}</div>
            <Badge v-if="assignments.length > 1" variant="outline" class="ml-2">
              {{ assignments.length }} roles
            </Badge>
          </div>
          <div class="col-span-5 flex items-center flex-wrap gap-2">
            <template v-if="getAllRoles(assignments).length > 1">
              <Badge class="text-center align-middle">
                Más de un rol asignado
              </Badge>
            </template>
            <template v-else>
              <Badge v-for="(role, index) in getAllRoles(assignments)" :key="index" class="text-center align-middle">
                {{ getRoleName(role) }}
              </Badge>
            </template>
          </div>
          <div class="col-span-2 flex justify-end items-center gap-1">
            <Button variant="ghost" size="icon" class="h-8 w-8" @click="emitEdit(assignments)">
              <TblrEdit class="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" class="h-8 w-8 text-destructive" @click="emitDelete(assignments)">
              <HrsldTrash class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Button from '../common/Button.vue'
import Badge from '../common/Badge.vue'

const props = defineProps({
  projectName: {
    type: String,
    required: true
  },
  projectId: {
    type: Number,
    required: true
  },
  assignments: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['edit', 'delete', 'add-person'])
const isOpen = ref(false)

// Obtiene todos los roles únicos de las asignaciones
const getAllRoles = (assignments) => {
  if (!assignments || !Array.isArray(assignments)) return []

  try {
    const allRoles = assignments.flatMap(a => {
      if (!a?.rol) return []
      return Array.isArray(a.rol) ? a.rol : [a.rol]
    })

    // Filtrar roles duplicados manteniendo el orden
    const uniqueRoles = []
    const seen = new Set()

    allRoles.forEach(role => {
      let roleKey
      if (typeof role === 'object') {
        roleKey = role.id || role.role_id ||
          JSON.stringify({ name: role.name, description: role.role_description })
      } else {
        roleKey = role
      }

      if (!seen.has(roleKey)) {
        seen.add(roleKey)
        uniqueRoles.push(role)
      }
    })

    return uniqueRoles
  } catch (error) {
    console.error('Error processing roles:', error)
    return []
  }
}

// Obtiene el nombre legible del rol
const getRoleName = (role) => {
  if (!role) return 'Rol no especificado'
  if (typeof role === 'object') {
    return role.name || role.role_description || `Rol ${role.id}`
  }
  return role
}

// Versión segura de personGroups que maneja datos faltantes
const safePersonGroups = computed(() => {
  if (!Array.isArray(props.assignments)) return {}

  return props.assignments.reduce((groups, assignment) => {
    if (!assignment || !assignment.persona) return groups

    const persona = assignment.persona
    if (!groups[persona]) {
      groups[persona] = []
    }

    // Asegurar que cada asignación tenga una estructura consistente
    const safeAssignment = {
      id: assignment.id || null,
      persona: assignment.persona,
      personaId: assignment.personaId || null,
      proyecto: assignment.proyecto || props.projectName,
      proyectoId: assignment.proyectoId || props.projectId,
      rol: assignment.rol || [],
      stakeholder_id: assignment.stakeholder_id || null
    }

    groups[persona].push(safeAssignment)
    return groups
  }, {})
})

function getInitials(fullName) {
  if (!fullName) return '';

  const parts = fullName.trim().split(/\s+/);

  const firstInitial = parts.length > 0 ? parts[0].charAt(0) : '';
  const thirdInitial = parts.length >= 3 ? parts[2].charAt(0) : '';

  const lastInitial = parts.length > 1 && !thirdInitial
    ? parts[parts.length - 1].charAt(0)
    : thirdInitial;

  return firstInitial + lastInitial;
}

function emitEdit(assignments) {
  if (!assignments || assignments.length === 0) return

  emit('edit', {
    id: assignments[0].id,
    persona: assignments[0].persona,
    personaId: assignments[0].personaId,
    proyecto: props.projectName,
    proyectoId: props.projectId,
    rol: getAllRoles(assignments),
    stakeholder_id: assignments[0].stakeholder_id
  })
}

function emitDelete(assignments) {
  if (!assignments || assignments.length === 0) return

  emit('delete', {
    id: assignments[0].id,
    persona: assignments[0].persona,
    personaId: assignments[0].personaId,
    proyecto: props.projectName,
    proyectoId: props.projectId,
    rol: getAllRoles(assignments),
    stakeholder_id: assignments[0].stakeholder_id
  })
}
</script>