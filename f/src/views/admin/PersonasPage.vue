<template>
  <div class="space-y-2">
    <div class="flex flex-col gap-4">
      <div class="flex items-center justify-between">
        <h2 class="text-3xl font-bold tracking-tight">Gestión de Personas</h2>
        <Button v-if="personas.length > 0" @click="modalStore.openCreateModal()" class="md:size-default">
          <HrsldUsersPlus class="h-4 w-4" />
          <span class="hidden md:inline ml-2">Nueva Persona</span>
        </Button>
      </div>
      <div class="relative w-full max-w-sm">
        <HrsldSearch class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <input type="search" placeholder="Buscar por nombre o apellido..."
          class="flex h-8 w-full rounded-md border border-input bg-background px-3 py-1 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          v-model="searchTerm" />
      </div>
    </div>

    <!-- Vista móvil (cards) -->
    <div v-if="filteredPersonas.length > 0" class="md:hidden space-y-2">
      <div v-for="persona in filteredPersonas" :key="persona.id" class="p-4 border rounded-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="font-medium">{{ persona.nombre }} {{ persona.apellido }}</h3>
            <div class="mt-1 flex flex-wrap gap-1">
              <template v-if="persona.roles.length > 1">
                <Badge class="text-xs">+{{ persona.roles.length }} roles</Badge>
              </template>
              <template v-else>
                <Badge v-for="(rol, index) in persona.roles" :key="index" class="text-xs">
                  {{ rol }}
                </Badge>
              </template>
            </div>

            <div class="mt-1 text-sm text-muted-foreground flex items-center gap-1">
              <TblrMapPin class="h-4 w-4" />
              {{ persona.person_location || 'Sin ubicación asignada' }}
            </div>

            <div class="mt-1">
              <a :href="persona.person_urlsite || 'https://access.cinvestav.mx/investigacion/directorio-de-investigacion/category/unidad-tamaulipas'"
                target="_blank" rel="noopener noreferrer"
                class="text-sm text-blue-600 hover:underline flex items-center gap-1">
                <TblrLink class="h-4 w-4" />
                {{ persona.person_urlsite ? 'Sitio web' : 'Sitio default' }}
              </a>
            </div>

          </div>
          <div class="flex space-x-1">
            <Button variant="ghost" size="sm" @click="handleEdit(persona)" class="p-2">
              <TblrEdit class="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" @click="handleDelete(persona)"
              class="p-2 text-red-600 hover:text-red-800">
              <HrsldTrash class="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Vista desktop (tabla) -->
    <div v-if="filteredPersonas.length > 0" class="hidden md:block rounded-md border">
      <div :style="{ 'max-height': containerHeight + 'px' }" class="overflow-auto">
        <table class="w-full">
          <thead class="sticky top-0 bg-white shadow-md">
            <tr class="border-b bg-muted/50">
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Nombre</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Apellido</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Ubicación</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Sitio Web</th>
              <th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Rol Asignado</th>
              <th class="h-12 px-4 text-right align-middle font-medium text-muted-foreground">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="persona in filteredPersonas" :key="persona.id" class="border-b">
              <td class="p-4 align-middle font-medium">{{ persona.nombre }}</td>
              <td class="p-4 align-middle">{{ persona.apellido }}</td>

              <td class="p-4 align-middle truncate max-w-[150px]">
                {{ persona.person_location || 'Sin ubicación asignada' }}
              </td>

              <td class="p-4 align-middle">
                <Badge class="text-center align-middle gap-2">
                  <TblrLink class="h-4 w-4" />
                  <a target="_blank"
                    :href="persona.person_urlsite || 'https://access.cinvestav.mx/investigacion/directorio-de-investigacion/category/unidad-tamaulipas'"
                    rel="noopener noreferrer">
                    {{ persona.person_urlsite ? 'Perfil web' : 'Sitio default' }}
                  </a>
                </Badge>
              </td>

              <td class="p-4 align-middle">
                <template v-if="persona.roles.length > 1">
                  <Badge class="text-center align-middle hover:bg-primary cursor-default">
                    +{{ persona.roles.length }} roles
                  </Badge>
                </template>
                <template v-else>
                  <div v-for="(rol, index) in persona.roles" :key="index" class="inline-block">
                    <Badge class="text-center align-middle hover:bg-primary cursor-default">
                      {{ rol }}
                    </Badge>
                  </div>
                </template>
              </td>
              <td class="p-4 align-middle text-right">
                <Button variant="ghost" size="sm" @click="handleEdit(persona)">
                  <TblrEdit class="mr-2 h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm" class="text-red-600 hover:text-red-800"
                  @click="handleDelete(persona)">
                  <HrsldTrash class="mr-2 h-4 w-4" />
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <EmptyState v-else title="No hay personas registradas" description="Comience creando su primer persona"
      actionText="Crear persona" :icon="TblrSettings" :onAction="modalStore.openCreateModal" />
  </div>

  <!-- Modales -->
  <PersonaModal :is-open="modalStore.isCreateModalOpen" :on-close="modalStore.closeCreateModal" mode="create"
    @success="fetchPersonas" />
  <PersonaModal v-if="modalStore.currentItem" :is-open="modalStore.isEditModalOpen"
    :on-close="modalStore.closeEditModal" :persona="modalStore.currentItem" mode="edit" @success="fetchPersonas" />

  <!-- Alert Modal -->
  <AlertModal :is-open="modalStore.isAlertOpen" :on-close="modalStore.closeAlert" :title="modalStore.alertConfig.title"
    :message="modalStore.alertConfig.message" :confirm-text="modalStore.alertConfig.confirmText"
    :cancel-text="modalStore.alertConfig.cancelText" :loading-text="modalStore.alertConfig.loadingText"
    :confirm-variant="modalStore.alertConfig.confirmVariant" :show-cancel="modalStore.alertConfig.showCancel"
    :on-confirm="modalStore.alertConfig.onConfirm" />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useModalStore } from '../../stores/modal'
import Button from '../../components/common/Button.vue'
import Badge from '../../components/common/Badge.vue'
import PersonaModal from '../../components/modals/users/PersonaModal.vue'
import AlertModal from '../../components/modals/general/AlertModal.vue'
import {
  personsApi,
  rolesApi,
  stakeholdersApi,
  projectStakeholdersApi
} from '../../lib/api'
import EmptyState from '../../components/common/EmptyState.vue'
import { useContainerHeight } from '../../utils/calculateContainerHeight'

const { containerHeight } = useContainerHeight()
const modalStore = useModalStore();
const personas = ref([]);
const searchTerm = ref('');

const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

const sortedPersonas = computed(() => {
  return [...personas.value].sort((a, b) => b.id - a.id)
})

const filteredPersonas = computed(() => {
  if (!searchTerm.value.trim()) return sortedPersonas.value

  const searchTermNormalized = normalizeString(searchTerm.value)
  return sortedPersonas.value.filter(persona =>
    normalizeString(persona.nombre).includes(searchTermNormalized) ||
    normalizeString(persona.apellido).includes(searchTermNormalized) ||
    normalizeString(persona.person_location).includes(searchTermNormalized))
})

const fetchPersonas = async () => {
  try {
    const [personsRes, rolesRes, stakeholdersRes, projectStakeholdersRes] = await Promise.all([
      personsApi.getAll(),
      rolesApi.getAll(),
      stakeholdersApi.getAll(),
      projectStakeholdersApi.getAll()
    ]);

    const persons = personsRes.data;
    const roles = rolesRes.data;
    const stakeholders = stakeholdersRes.data;
    const projectStakeholders = projectStakeholdersRes.data;

    const roleMap = roles.reduce((acc, role) => {
      acc[role.role_id] = role.role_description;
      return acc;
    }, {});

    const projectsCountPerPerson = projectStakeholders.reduce((acc, ps) => {
      const stakeholder = stakeholders.find(s => s.stakeholder_id === ps.stakeholder_id);
      if (stakeholder) {
        const personId = stakeholder.person_id;
        acc[personId] = (acc[personId] || 0) + 1;
      }
      return acc;
    }, {});

    const rolesByPerson = stakeholders.reduce((acc, stakeholder) => {
      const personId = stakeholder.person_id;
      const roleDescription = roleMap[stakeholder.role_id];
      if (roleDescription) {
        if (!acc[personId]) {
          acc[personId] = [];
        }
        acc[personId].push(roleDescription);
      }
      return acc;
    }, {});

    personas.value = persons.map(person => ({
      id: person.person_id,
      nombre: person.person_firstname,
      apellido: person.person_lastname,
      person_location: person.person_location,
      person_urlsite: person.person_urlsite,
      roles: rolesByPerson[person.person_id] || [],
      num_pryts: projectsCountPerPerson[person.person_id] || 0
    }));

  } catch (error) {
    console.error('Error fetching data:', error);
    modalStore.showAlert('Error al cargar los datos de personas', 'Error');
  }
};

onMounted(fetchPersonas);

function handleEdit(persona) {
  modalStore.openEditModal({
    ...persona,
    person_firstname: persona.nombre,
    person_lastname: persona.apellido
  });
}

const handleDelete = async (persona) => {
  const confirmed = await modalStore.showConfirm(
    `¿Estás seguro de que deseas eliminar a ${persona.nombre} ${persona.apellido}?`,
    'Confirmar eliminación'
  );

  if (confirmed) {
    try {
      await personsApi.delete(persona.id);
      await fetchPersonas();
      modalStore.showAlert(
        `${persona.nombre} ${persona.apellido} ha sido eliminado correctamente`,
        'Eliminación exitosa'
      );
    } catch (error) {
      console.error('Error deleting person:', error);
      modalStore.showAlert('No se pudo eliminar la persona', 'Error');
    }
  }
};
</script>

<style scoped>
.text-red-600 {
  color: #dc2626;
}

.text-red-600:hover {
  color: #991b1b;
}
</style>