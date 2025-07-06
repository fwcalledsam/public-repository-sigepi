<template>
  <div class="flex min-h-screen w-full flex-col">

    <NavBar :has-background="true" variant="default" />

    <div class="flex-1">
      <main class="flex flex-col gap-4 p-4 md:gap-8 md:p-6 pt-[75px] md:pt-[80px]">
        <!-- Sección de información institucional -->
        <section class="space-y-6">
          <div class="space-y-2">
            <h1 class="text-3xl font-bold tracking-tight">Grupo de Trabajo en Analítica de Datos | ALEF</h1>
            <p class="text-lg text-muted-foreground">
              Centro de Investigación y de Estudios Avanzados del IPN (CINVESTAV)
            </p>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <Card class="hover:bg-muted/50 transition-colors cursor-pointer">
              <router-link to="/investigadores" class="block">
                <CardHeader class="space-y-0 pb-2">
                  <div class="flex justify-between">
                    <CardTitle class="text-sm font-medium">Investigadores</CardTitle>
                    <HrsldUsers class="h-4 w-4 text-[#008d85]" />
                  </div>
                </CardHeader>
                <CardContent>
                  <div class="text-2xl font-bold text-[#008d85]">{{ totalPersonas }}</div>
                  <p class="text-xs text-muted-foreground">Investigadores y colaboradores activos en diferentes áreas de
                    especializacion</p>
                </CardContent>
              </router-link>
            </Card>
            <Card>
              <CardHeader class="space-y-0 pb-2">
                <div class="flex justify-between">
                  <CardTitle class="text-sm font-medium">Proyectos</CardTitle>
                  <HrsldTools class="h-4 w-4 text-[#008d85]" />
                </div>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold text-[#008d85]">{{ proyectosEnCurso }}</div>
                <p class="text-xs text-muted-foreground">En diferentes áreas de investigación</p>
              </CardContent>
            </Card>
          </div>
        </section>

        <div class="space-y-4">
          <div class="flex flex-col gap-4">
            <h2 class="text-2xl font-semibold tracking-tight">Proyectos de Investigación</h2>
            <div class="relative w-full max-w-sm">
              <HrsldSearch class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <input type="search" placeholder="Buscar por título o palabras clave..."
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                v-model="searchTerm" />
            </div>
          </div>

          <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <template v-if="isLoading">
              <!-- Mostrar 6 tarjetas de carga durante la carga inicial -->
              <ProyectoCard v-for="i in 3" :key="`skeleton-${i}`" :loading="true" />
            </template>

            <template v-else>
              <!-- Mostrar proyectos cargados -->
              <ProyectoCard v-for="proyecto in visibleProyectos" :key="proyecto.id" :proyecto="proyecto" />
            </template>
          </div>

          <div v-if="loadingMore" class="flex justify-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#008d85]"></div>
          </div>

          <div v-if="!isLoading && visibleProyectos.length === 0" class="col-span-full flex justify-center">
            <EmptyState title="No se encontraron proyectos"
              description="No hay proyectos que coincidan con tu búsqueda o no hay proyectos registrados aún."
              variant="home-researcher" class="w-full max-w-md" />
          </div>

          <div v-if="hasMoreProjects && !isLoading && !loadingMore" class="flex justify-center">
            <Button variant="outline" @click="loadMoreProjects" class="mt-4">
              Cargar más proyectos
            </Button>
          </div>

          <div v-if="allDataLoaded && visibleProyectos.length > 0"
            class="text-center text-sm text-muted-foreground py-4">
            Has llegado al final de la lista de proyectos
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Button from '../../components/common/Button.vue'
import Card from '../../components/common/Card.vue'
import CardHeader from '../../components/common/CardHeader.vue'
import CardTitle from '../../components/common/CardTitle.vue'
import CardContent from '../../components/common/CardContent.vue'
import ProyectoCard from '../../components/cards/ProyectoCard.vue'
import LogoSVG from '../../assets/icons/logo.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { projectsApi, personsApi, rolesApi, stakeholdersApi, projectStakeholdersApi, levelsApi, projectImagesApi } from '../../lib/api'

import NavBar from '../../components/layout/NavBar.vue'

const searchTerm = ref('')
const proyectos = ref([])
const totalPersonas = ref(0)
const proyectosEnCurso = ref(0)
const niveles = ref([])
const isLoading = ref(true)
const visibleCount = ref(6) // Mostrar 6 proyectos inicialmente
const loadingMore = ref(false)
const allDataLoaded = ref(false)

// Computed properties
const sortedAndFilteredProyectos = computed(() => {
  const sorted = [...proyectos.value].sort((a, b) => b.id - a.id)

  if (!searchTerm.value.trim()) return sorted

  const searchTermNormalized = normalizeString(searchTerm.value)

  return sorted.filter(proyecto => {
    const matchTitulo = normalizeString(proyecto.titulo).includes(searchTermNormalized)
    const matchKeywords = proyecto.project_keywords
      ? normalizeString(proyecto.project_keywords).includes(searchTermNormalized)
      : false
    return matchTitulo || matchKeywords
  })
})

const visibleProyectos = computed(() => {
  return sortedAndFilteredProyectos.value.slice(0, visibleCount.value)
})

const hasMoreProjects = computed(() => {
  return visibleCount.value < sortedAndFilteredProyectos.value.length
})

// Función para normalizar texto
const normalizeString = (str) => {
  return str?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase() || ''
}

// Función para cargar más proyectos
const loadMoreProjects = () => {
  if (loadingMore.value || allDataLoaded.value) return

  loadingMore.value = true

  setTimeout(() => {
    const remainingProjects = sortedAndFilteredProyectos.value.length - visibleCount.value
    const nextBatch = Math.min(6, remainingProjects)

    if (nextBatch > 0) {
      visibleCount.value += nextBatch
    }

    if (visibleCount.value >= sortedAndFilteredProyectos.value.length) {
      allDataLoaded.value = true
    }

    loadingMore.value = false
  }, 300)
}

// Manejar scroll para carga infinita
const handleScroll = () => {
  const scrollPosition = window.innerHeight + window.scrollY
  const pageHeight = document.body.offsetHeight
  const threshold = 200 // Pixeles antes del final para disparar la carga

  if (scrollPosition >= pageHeight - threshold && hasMoreProjects.value && !loadingMore.value) {
    loadMoreProjects()
  }
}

// Cargar datos iniciales
onMounted(async () => {
  try {
    const { data: levels } = await levelsApi.getAll()
    niveles.value = levels
    const levelMap = {}
    levels.forEach(level => {
      levelMap[level.level_id] = level.level_description
    })

    const { data: persons } = await personsApi.getAll()
    totalPersonas.value = persons.length

    const { data: projects } = await projectsApi.getAll()
    const [{ data: roles }, { data: stakeholders }, { data: projectStakeholders }] = await Promise.all([
      rolesApi.getAll(),
      stakeholdersApi.getAll(),
      projectStakeholdersApi.getAll()
    ])

    proyectos.value = await Promise.all(projects.map(async proyecto => {
      const stakeholdersDelProyecto = projectStakeholders
        .filter(ps => ps.project_id === proyecto.project_id)
        .map(ps => stakeholders.find(s => s.stakeholder_id === ps.stakeholder_id))
        .filter(Boolean)

      const equipo = stakeholdersDelProyecto.map(stakeholder => {
        const persona = persons.find(p => p.person_id === stakeholder.person_id) || {}
        const rol = roles.find(r => r.role_id === stakeholder.role_id) || {}
        return {
          nombre: persona.person_firstname || 'Desconocido',
          apellido: persona.person_lastname || '',
          rol: rol.role_description || 'No definido'
        }
      })

      // const investigador = equipo.find(miembro => miembro.rol === "Investigador Principal")
      const getResponsable = (equipo) => {
        const director = equipo.find(miembro => miembro.rol === "Director")
        if (director) return director

        const codirector = equipo.find(miembro => miembro.rol === "Codirector")
        if (codirector) return codirector

        const investigadorPrincipal = equipo.find(miembro => miembro.rol === "Investigador Principal")
        if (investigadorPrincipal) return investigadorPrincipal

        return null
      }

      const responsable = getResponsable(equipo)

      let imagePath = proyecto.project_image_path || '/placeholder.svg'
      try {
        const loadedImage = await loadProjectImage(proyecto.project_id)
        if (loadedImage) {
          imagePath = loadedImage
        }
      } catch (error) {
        console.error('Error loading project image:', error)
      }

      return {
        id: proyecto.project_id,
        titulo: proyecto.project_name || 'Sin título',
        descripcion: proyecto.project_description || 'Sin descripción',
        año: proyecto.project_agno || 'Desconocido',
        // investigadorPrincipal: investigador ? `${investigador.nombre} ${investigador.apellido}` : "No asignado",
        investigadorPrincipal: responsable ? `${responsable.nombre} ${responsable.apellido}` : "No asignado",
        nivel: levelMap[proyecto.level_id] || "No especificado",
        imagen: imagePath,
        project_keywords: proyecto.project_keywords
      }
    }))

    proyectosEnCurso.value = proyectos.value.length

    // Configurar el event listener para el scroll
    window.addEventListener('scroll', handleScroll)

    // Verificar si ya cargamos todos los proyectos inicialmente
    if (visibleCount.value >= proyectos.value.length) {
      allDataLoaded.value = true
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    isLoading.value = false
  }
})

// Limpieza
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// Función para cargar imágenes de proyectos
async function loadProjectImage(projectId) {
  try {
    const response = await projectImagesApi.get(projectId)
    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    return URL.createObjectURL(blob)
  } catch (error) {
    console.error('Error cargando imagen del proyecto:', error)
    return null
  }
}
</script>