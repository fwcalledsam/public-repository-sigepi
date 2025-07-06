<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
        <div class="flex flex-col space-y-1.5">
          <h3 class="text-lg font-semibold leading-none tracking-tight">
            {{ mode === "create" ? "Nuevo Nivel de Proyecto" : "Editar Nivel de Proyecto" }}
          </h3>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="grid gap-4 py-4">
            <div class="grid gap-2">
              <label for="nombre" class="text-sm font-medium leading-none">Nombre del Nivel</label>
              <input id="nombre" v-model="formData.description" placeholder="Nombre del nivel"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                required />
            </div>
          </div>
          <div class="flex justify-end space-x-2">
            <Button type="button" variant="outline" @click="onClose">
              Cancelar
            </Button>
            <Button type="submit" :disabled="isLoading">
              <span v-if="isLoading">Procesando...</span>
              <span v-else>{{ mode === "create" ? "Crear Nivel" : "Guardar Cambios" }}</span>
            </Button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import Button from '../../common/Button.vue'
import { levelsApi } from '../../../lib/api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  onClose: {
    type: Function,
    required: true
  },
  nivel: {
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
  description: props.nivel?.level_description || ''
})
const isLoading = ref(false)

watch(() => props.nivel, (newNivel) => {
  if (newNivel) {
    formData.value.description = newNivel.level_description
  } else {
    formData.value.description = ''
  }
}, { immediate: true })

async function handleSubmit() {
  isLoading.value = true
  try {
    if (props.mode === 'create') {
      const response = await levelsApi.create(formData.value)
      emit('success', {
        action: 'create',
        message: 'Nivel creado exitosamente',
        newLevel: response.data
      })
    } else {
      await levelsApi.update(props.nivel.level_id, formData.value)
      emit('success', {
        action: 'update',
        message: 'Nivel actualizado exitosamente',
        levelId: props.nivel.level_id,
        newData: formData.value
      })
    }
    props.onClose()
  } catch (error) {
    console.error('Error al guardar el nivel:', error)
    alert(error.response?.data?.message || 'Ocurrió un error al guardar el nivel')
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