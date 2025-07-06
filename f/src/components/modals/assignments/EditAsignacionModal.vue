<template>
    <Transition name="fade">
        <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div class="relative w-full max-w-md lg:max-w-4xl rounded-lg bg-background p-6 shadow-lg">
                <div class="flex flex-col space-y-1.5">
                    <h3 class="text-lg font-semibold leading-none tracking-tight">
                        Editar Asignación
                    </h3>
                    <p class="text-sm text-muted-foreground">
                        Modifique los roles para <strong>{{ asignacion.persona }}</strong> en el proyecto <strong>{{
                            asignacion.proyecto }}</strong>.
                    </p>
                </div>
                <form @submit.prevent="handleSubmit" class="mt-4">
                    <div class="grid lg:grid-cols-2 gap-4 py-4 lg:gap-8">
                        <!-- Columna izquierda -->
                        <div class="space-y-4">
                            <div class="grid gap-2">
                                <label class="text-sm font-medium leading-none">Persona</label>
                                <div
                                    class="flex h-10 w-full text-gray-600 font-medium rounded-md border border-input bg-background px-3 py-2 text-sm cursor-not-allowed">
                                    {{ asignacion.persona }}
                                </div>
                            </div>

                            <div class="grid gap-2">
                                <label class="text-sm font-medium leading-none">Proyecto</label>
                                <div
                                    class="flex h-18 w-full text-gray-600 font-medium rounded-md border border-input bg-background px-3 py-2 text-sm cursor-not-allowed">
                                    {{ asignacion.proyecto }}
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
                                            <div v-if="filteredRoles.length === 0"
                                                class="py-6 text-center text-sm text-muted-foreground">
                                                No se encontraron roles.
                                            </div>
                                            <div v-else v-for="role in filteredRoles" :key="role.role_id"
                                                class="flex items-center space-x-2">
                                                <input type="checkbox" :id="`role-${role.role_id}`"
                                                    :checked="formData.roles.includes(role.role_id)"
                                                    @change="handleRoleToggle(role.role_id)"
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
                            <span v-if="isLoading">Procesando...</span>
                            <span v-else>Guardar Cambios</span>
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Button from '../../common/Button.vue'
import Badge from '../../common/Badge.vue'
import { X } from 'lucide-vue-next'
import { rolesApi, stakeholdersApi, projectStakeholdersApi } from '../../../lib/api'

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
        required: true
    }
})

const emit = defineEmits(['success'])

const roles = ref([])
const searchTerm = ref('')
const isLoading = ref(false)
const formData = ref({
    roles: []
})

const filteredRoles = computed(() => {
    return roles.value.filter(role =>
        role.role_description.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
})

const getRoleName = (roleId) => {
    const role = roles.value.find(r => r.role_id === roleId)
    return role ? role.role_description : 'Rol desconocido'
}

const handleRoleToggle = (roleId) => {
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

const loadRoles = async () => {
    try {
        const rolesRes = await rolesApi.getAll()
        roles.value = rolesRes.data
    } catch (error) {
        console.error('Error al cargar los roles:', error)
    }
}

watch(() => props.asignacion, (newVal) => {
    if (newVal) {
        try {
            let currentRoles = []

            if (Array.isArray(newVal.rol)) {
                currentRoles = newVal.rol.map(r => {
                    if (typeof r === 'object') return r.id || r.role_id
                    const foundRole = roles.value.find(role =>
                        role.role_description === r || role.role_id === r
                    )
                    return foundRole?.role_id
                }).filter(Boolean)
            } else if (newVal.rol) {
                if (typeof newVal.rol === 'object') {
                    currentRoles = [newVal.rol.id || newVal.rol.role_id]
                } else {
                    const foundRole = roles.value.find(role =>
                        role.role_description === newVal.rol || role.role_id === newVal.rol
                    )
                    if (foundRole) currentRoles = [foundRole.role_id]
                }
            }

            formData.value.roles = [...new Set(currentRoles)] // Eliminar duplicados
        } catch (error) {
            console.error('Error parsing roles:', error)
            formData.value.roles = []
        }
    }
}, { immediate: true, deep: true })

const handleSubmit = async () => {
    if (formData.value.roles.length === 0) {
        alert('Debe seleccionar al menos un rol');
        return;
    }

    isLoading.value = true;

    try {
        // 1. Obtener stakeholders existentes para esta persona
        const stakeholdersRes = await stakeholdersApi.getAll();
        const personStakeholders = stakeholdersRes.data.filter(
            s => s.person_id === props.asignacion.personaId
        );

        // 2. Obtener TODAS las relaciones proyecto-stakeholder para este proyecto
        const projectStakeholdersRes = await projectStakeholdersApi.getAll();

        // 3. Filtrar solo las relaciones que pertenecen a esta persona
        const existingRelations = projectStakeholdersRes.data.filter(ps => {
            // Verificar si el stakeholder pertenece a esta persona
            const stakeholder = personStakeholders.find(s => s.stakeholder_id === ps.stakeholder_id);
            return stakeholder && ps.project_id === props.asignacion.proyectoId;
        });

        // 4. Para cada rol seleccionado, crear o actualizar
        const newStakeholderIds = [];

        for (const roleId of formData.value.roles) {
            try {
                // Verificar si ya existe un stakeholder para esta persona y rol
                let existingStakeholder = personStakeholders.find(
                    s => s.role_id === roleId
                );

                let stakeholderId;

                if (existingStakeholder) {
                    stakeholderId = existingStakeholder.stakeholder_id;

                    // Verificar si ya existe la relación proyecto-stakeholder para ESTE PROYECTO
                    const relationExists = existingRelations.some(
                        ps => ps.stakeholder_id === stakeholderId
                    );

                    if (relationExists) {
                        newStakeholderIds.push(stakeholderId);
                        continue; // Ya existe, pasar al siguiente rol
                    }
                } else {
                    // Crear nuevo stakeholder si no existe
                    const newStakeholder = await stakeholdersApi.create({
                        person_id: props.asignacion.personaId,
                        role_id: roleId
                    });
                    stakeholderId = newStakeholder.data?.stakeholder_id ||
                        newStakeholder.data?.id ||
                        newStakeholder.stakeholder_id;
                }

                // Crear nueva relación proyecto-stakeholder
                await projectStakeholdersApi.create({
                    project_id: props.asignacion.proyectoId,
                    stakeholder_id: stakeholderId
                });

                newStakeholderIds.push(stakeholderId);
            } catch (error) {
                console.error(`Error procesando rol ${roleId}:`, error);
                continue;
            }
        }

        // 5. Eliminar solo las relaciones que pertenecen a esta persona y proyecto
        // y que no están en los nuevos roles seleccionados
        const relationsToRemove = existingRelations.filter(
            ps => !newStakeholderIds.includes(ps.stakeholder_id)
        );

        for (const relation of relationsToRemove) {
            try {
                await projectStakeholdersApi.delete(relation.prj_stk_id);
            } catch (error) {
                console.error('Error eliminando relación obsoleta:', error);
            }
        }

        emit('success', {
            action: 'update',
            message: 'Asignación actualizada exitosamente'
        });
        props.onClose();
    } catch (error) {
        console.error('Error general en handleSubmit:', {
            error: error,
            requestData: {
                person_id: props.asignacion.personaId,
                roles: formData.value.roles
            },
            response: error.response?.data
        });

        let errorMessage = 'Error al actualizar la asignación';
        if (error.response?.data?.message) {
            errorMessage += `: ${error.response.data.message}`;
        } else if (error.message) {
            errorMessage += `: ${error.message}`;
        }

        alert(errorMessage);
    } finally {
        isLoading.value = false;
    }
}

loadRoles()
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