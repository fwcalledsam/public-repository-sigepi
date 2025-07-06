<template>
  <Transition name="fade">
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="relative w-full max-w-md lg:max-w-4xl rounded-lg bg-background p-6 shadow-lg">
        <div class="flex flex-col space-y-1.5">
          <h3 class="text-lg font-semibold leading-none tracking-tight">
            {{ mode === "create" ? "Nuevo Proyecto" : "Editar Proyecto" }}
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ mode === "create"
              ? "Complete los detalles para crear un nuevo proyecto de investigación."
              : "Modifique los detalles del proyecto de investigación." }}
          </p>
        </div>
        <form @submit.prevent="handleSubmit" class="mt-4">
          <div class="grid lg:grid-cols-2 gap-4 py-4 lg:gap-8">
            <!-- Columna izquierda -->
            <div class="space-y-4">
              <div class="grid gap-2">
                <label for="name" class="text-sm font-medium leading-none">Nombre del Proyecto</label>
                <input id="name" v-model="formData.project_name" placeholder="Ingrese el nombre del proyecto"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required />
              </div>
              <div class="grid gap-2">
                <label for="description" class="text-sm font-medium leading-none">Descripción</label>
                <textarea id="description" v-model="formData.project_description" placeholder="Descripción del proyecto"
                  rows="5"
                  class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required></textarea>
              </div>
              <div class="grid gap-2">
                <label for="keywords" class="text-sm font-medium leading-none">Palabras clave</label>
                <input id="keywords" v-model="formData.project_keywords"
                  placeholder="Ingrese palabras clave separadas por comas (ej: investigación, desarrollo)"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  maxlength="200" />
                <p class="text-xs text-muted-foreground">Máximo 200 caracteres</p>
              </div>
            </div>

            <!-- Columna derecha -->
            <div class="space-y-4">
              <div class="grid gap-2">
                <label for="year" class="text-sm font-medium leading-none">Año</label>
                <input id="year" v-model.number="formData.project_agno" type="number" placeholder="Año de inicio"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required />
              </div>
              <div class="grid gap-2">
                <label for="level" class="text-sm font-medium leading-none">Nivel</label>
                <select id="level" v-model.number="formData.level_id"
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  required>
                  <option value="" disabled>Seleccione un nivel</option>
                  <option v-for="nivel in niveles" :key="nivel.level_id" :value="nivel.level_id">
                    {{ nivel.level_description }}
                  </option>
                </select>
              </div>
              <div class="grid gap-2">
                <label for="image" class="text-sm font-medium leading-none">Imagen del Proyecto</label>
                <div class="flex items-center gap-4">
                  <input id="image" type="file" accept="image/*" @change="handleImageUpload"
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />

                  <template v-if="formData.project_image_path">
                    <Badge variant="destructive" class="cursor-pointer hover:bg-gray-100" @click="clearImage">
                      Eliminar
                    </Badge>
                  </template>
                </div>
                <p v-if="formData.imageFile" class="text-xs text-muted-foreground">
                  Imagen seleccionada: {{ formData.imageFile.name }} ({{ (formData.imageFile.size / 1024 /
                    1024).toFixed(2)
                  }} MB)
                </p>
                <!-- Vista previa de la imagen -->
                <div v-if="formData.project_image_path" class="mt-2">
                  <img :src="formData.project_image_path" alt="Vista previa de la imagen del proyecto"
                    class="max-h-20 rounded-md object-cover border border-input">
                </div>
              </div>
            </div>
          </div>
          <div class="flex justify-end space-x-2">
            <Button type="button" variant="outline" @click="onClose">
              Cancelar
            </Button>
            <Button type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Procesando...' : mode === "create" ? "Crear Proyecto" : "Guardar Cambios" }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { projectsApi, levelsApi, projectImagesApi } from '../../../lib/api'
import { useModalStore } from '../../../stores/modal'
import Button from '../../common/Button.vue'
import Badge from '../../common/Badge.vue'

const modalStore = useModalStore()
const props = defineProps({
  isOpen: Boolean,
  onClose: Function,
  proyecto: Object,
  mode: String
})

const emit = defineEmits(['refresh'])

const niveles = ref([])
const isSubmitting = ref(false)

const formData = ref({
  project_name: '',
  project_description: '',
  project_agno: new Date().getFullYear(),
  level_id: '',
  project_image_path: null,
  project_keywords: '',
  imageFile: null
})

// Cargar niveles
onMounted(async () => {
  try {
    const response = await levelsApi.getAll()
    niveles.value = response.data
  } catch (error) {
    console.error('Error cargando niveles:', error)
    modalStore.showAlert('Error al cargar los niveles disponibles', 'Error')
  }
})

// Watcher para proyecto
watch(() => props.proyecto, (newProyecto) => {
  if (newProyecto) {
    formData.value = {
      project_name: newProyecto.project_name || '',
      project_description: newProyecto.project_description || '',
      project_agno: newProyecto.project_agno || new Date().getFullYear(),
      level_id: newProyecto.level_id || '',
      project_image_path: newProyecto.project_image_path || null,
      project_keywords: newProyecto.project_keywords || '',
      imageFile: null
    }

    // Si hay una imagen existente, crear una URL de previsualización
    if (newProyecto.project_image_path) {
      loadExistingImage(newProyecto.project_id)
    }
  } else {
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  formData.value = {
    project_name: '',
    project_description: '',
    project_agno: new Date().getFullYear(),
    level_id: '',
    project_image_path: null,
    project_keywords: '',
    imageFile: null
  }
}

async function loadExistingImage(projectId) {
  try {
    const response = await projectImagesApi.get(projectId)
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    formData.value.project_image_path = URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error cargando imagen existente:', error)
    formData.value.project_image_path = null
  }
}

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // Validar tipo de archivo
  if (!file.type.match('image.*')) {
    modalStore.showAlert('Por favor, selecciona un archivo de imagen válido', 'Formato inválido')
    clearImage()
    return
  }

  // Validar tamaño de archivo (ejemplo: máximo 5MB)
  if (file.size > 5 * 1024 * 1024) {
    modalStore.showAlert('La imagen no debe exceder los 5MB', 'Tamaño excedido')
    clearImage()
    return
  }

  // Crear URL de previsualización
  formData.value.project_image_path = URL.createObjectURL(file)
  formData.value.imageFile = file
}

function clearImage() {
  // Liberar memoria de la URL de objeto si existe
  if (formData.value.project_image_path?.startsWith('blob:')) {
    URL.revokeObjectURL(formData.value.project_image_path)
  }

  formData.value.project_image_path = null
  formData.value.imageFile = null

  // Resetear el input de archivo
  const fileInput = document.getElementById('image')
  if (fileInput) fileInput.value = ''
}

async function handleImageOperations(projectId) {
  // Si no hay imagen seleccionada y había una imagen anterior, eliminarla
  if (!formData.value.imageFile && !formData.value.project_image_path && props.proyecto?.project_image_path) {
    try {
      await projectImagesApi.delete(projectId)
    } catch (error) {
      console.error('Error eliminando imagen:', error)
      // Solo lanzar error si no es un 404 (imagen no encontrada)
      if (error.response?.status !== 404) {
        throw error
      }
    }
  }
  // Si hay una nueva imagen, usar el endpoint de actualización
  else if (formData.value.imageFile) {
    try {
      const response = await projectImagesApi.update(projectId, formData.value.imageFile)
      formData.value.project_image_path = response.data.image_path

      // Actualizar la previsualización
      if (formData.value.project_image_path?.startsWith('blob:')) {
        URL.revokeObjectURL(formData.value.project_image_path)
      }
      formData.value.project_image_path = URL.createObjectURL(formData.value.imageFile)
    } catch (error) {
      console.error('Error actualizando imagen:', error)
      throw error
    }
  }
}

async function handleSubmit() {
  isSubmitting.value = true
  try {
    let response

    if (props.mode === 'create') {
      // Primero crear el proyecto sin imagen
      const projectData = {
        name: formData.value.project_name,
        description: formData.value.project_description,
        agno: formData.value.project_agno,
        level_id: formData.value.level_id,
        keywords: formData.value.project_keywords
      }

      response = await projectsApi.create(projectData)
      const projectId = response.data.id

      // Luego manejar la imagen si existe
      if (formData.value.imageFile) {
        await handleImageOperations(projectId)
      }
    } else {
      // Actualizar proyecto
      const projectData = {
        name: formData.value.project_name,
        description: formData.value.project_description,
        agno: formData.value.project_agno,
        level_id: formData.value.level_id,
        keywords: formData.value.project_keywords
      }

      response = await projectsApi.update(props.proyecto.project_id, projectData)

      // Manejar la imagen
      await handleImageOperations(props.proyecto.project_id)
    }

    modalStore.showAlert(
      props.mode === 'create' ? 'Proyecto creado con éxito' : 'Proyecto actualizado con éxito',
      'Éxito'
    )
    emit('refresh')
    props.onClose()
  } catch (error) {
    console.error('Error:', error)
    modalStore.showAlert(
      error.response?.data?.message || error.message || 'Error al guardar el proyecto',
      'Error'
    )
  } finally {
    isSubmitting.value = false
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