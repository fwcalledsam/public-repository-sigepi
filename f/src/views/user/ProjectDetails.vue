<template>
    <div>
        <!-- Línea superior -->
        <div class="fixed top-0 left-0 right-0 h-2 bg-[#008d85] z-50"></div>

        <div class="flex min-h-screen w-full flex-col bg-white" style="padding-top: 2px;">
            <header class="sticky top-0 z-10 flex h-16 items-center gap-4 bg-white px-4 md:px-6">
                <Button variant="ghost" size="icon" @click="$router.back()">
                    <HrsldArrowLeft class="h-5 w-5" />
                </Button>
                <div class="flex items-center gap-2 font-semibold">
                    <LogoSVG class="w-6 h-6" />
                </div>
            </header>

            <main class="flex-1 p-4 md:p-6">
                <div v-if="!proyecto" class="flex items-center justify-center h-screen">Proyecto no encontrado</div>
                <div v-else class="mx-auto max-w-4xl space-y-6">
                    <div class="flex flex-col md:flex-row md:items-start gap-6">
                        <div class="flex-1">
                            <div class="flex flex-col gap-2">
                                <!-- Versión Desktop -->
                                <div class="hidden md:flex items-center gap-2">
                                    <h1 class="text-2xl font-bold">{{ proyecto.nombre_proyecto }}</h1>
                                    <Badge variant="outline" class="bg-[#008d85] text-white">{{ proyecto.nivel }}
                                    </Badge>
                                </div>

                                <!-- Versión Mobile -->
                                <div class="md:hidden flex flex-col gap-2">
                                    <h1 class="text-xl font-bold">{{ proyecto.nombre_proyecto }}</h1>
                                    <div>
                                        <Badge variant="outline" class="bg-[#008d85] text-white text-sm">{{
                                            proyecto.nivel }}
                                        </Badge>
                                    </div>
                                </div>
                            </div>

                            <Card class="mt-4">
                                <CardHeader>
                                    <CardTitle class="text-[#008d85]">Información General</CardTitle>
                                </CardHeader>

                                <CardContent class="grid gap-6">
                                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                                        <div class="space-y-4 md:col-span-2">
                                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div class="space-y-1">
                                                    <div class="text-sm text-muted-foreground font-medium">Responsable
                                                        del Proyecto</div>
                                                    <div class="text-sm text-[#008d85] font-bold">{{
                                                        proyecto.responsable }}</div>
                                                </div>
                                                <div class="space-y-1">
                                                    <div class="text-sm text-muted-foreground font-medium">Año</div>
                                                    <div class="text-sm text-[#008d85] font-bold">{{ proyecto.año }}
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="relative">
                                                <div class="text-sm text-muted-foreground transition-all duration-200"
                                                    :class="{ 'line-clamp-7 custom-clamp': !showFullDescription, 'max-h-[999px]': showFullDescription }"
                                                    ref="descriptionElement">
                                                    {{ proyecto.descripcion }}
                                                </div>
                                                <button v-if="isClamped"
                                                    @click="showFullDescription = !showFullDescription"
                                                    class="text-[#008d85] text-xs font-medium mt-1 flex items-center hover:underline focus:outline-none">
                                                    {{ showFullDescription ? 'Mostrar menos' : 'Mostrar más' }}
                                                    <svg xmlns="http://www.w3.org/2000/svg"
                                                        class="h-3 w-3 ml-1 transition-transform duration-200"
                                                        :class="{ 'rotate-180': showFullDescription }"
                                                        viewBox="0 0 20 20" fill="currentColor">
                                                        <path fill-rule="evenodd"
                                                            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                                            clip-rule="evenodd" />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>

                                        <!-- Columna 2: Imagen (solo en desktop) -->
                                        <div class="hidden md:flex md:col-span-2 justify-center items-start">
                                            <div class="w-full h-64 rounded-lg overflow-hidden border border-gray-200">
                                                <img v-if="proyecto.imagen" :src="proyecto.imagen"
                                                    :alt="proyecto.nombre_proyecto"
                                                    class="w-full h-full object-cover" />
                                                <div v-else
                                                    class="w-full h-full bg-gray-100 flex items-center justify-center">
                                                    <span class="text-gray-400">Sin imagen</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>

                            <div v-if="activeTab === 'equipo'" class="space-y-4 mt-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle class="flex items-center gap-2 text-[#008d85]">
                                            <HrsldUsers class="h-5 w-5 text-black" />
                                            Equipo de Investigación
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <div class="space-y-4">
                                            <div v-for="(miembro, index) in proyecto.equipo" :key="index"
                                                class="flex items-start gap-4">
                                                <div
                                                    class="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium">
                                                    {{ miembro.nombre.charAt(0) }}{{ miembro.apellido.charAt(0) }}
                                                </div>
                                                <div class="space-y-1">
                                                    <div class="font-medium">
                                                        {{ miembro.nombre }} {{ miembro.apellido }}
                                                    </div>
                                                    <div class="text-sm text-muted-foreground">{{ miembro.rol }}</div>
                                                </div>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
    projectsApi,
    personsApi,
    rolesApi,
    stakeholdersApi,
    projectStakeholdersApi,
    levelsApi,
    projectImagesApi
} from '../../lib/api'
import Button from '../../components/common/Button.vue'
import Card from '../../components/common/Card.vue'
import CardHeader from '../../components/common/CardHeader.vue'
import CardTitle from '../../components/common/CardTitle.vue'
import CardDescription from '../../components/common/CardDescription.vue'
import CardContent from '../../components/common/CardContent.vue'
import Badge from '../../components/common/Badge.vue'
import LogoSVG from '../../assets/icons/logo.vue'

const route = useRoute()
const activeTab = ref('equipo')
const proyecto = ref(null)
const showFullDescription = ref(false)
const isClamped = ref(false)
const descriptionElement = ref(null)

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

onMounted(() => {
    window.scrollTo(0, 0)
})

onMounted(async () => {
    try {
        // Obtener todos los datos necesarios
        const [
            { data: proyectos },
            { data: persons },
            { data: roles },
            { data: stakeholders },
            { data: projectStakeholders },
            { data: niveles }
        ] = await Promise.all([
            projectsApi.getAll(),
            personsApi.getAll(),
            rolesApi.getAll(),
            stakeholdersApi.getAll(),
            projectStakeholdersApi.getAll(),
            levelsApi.getAll()
        ])

        // Buscar el proyecto correspondiente
        const proyectoData = proyectos.find(p => p.project_id == route.params.id)

        if (!proyectoData) {
            proyecto.value = null
            return
        }

        // Obtener la descripción del nivel
        const nivelDescripcion = niveles.find(n => n.level_id === proyectoData.level_id)?.level_description || 'No especificado'

        // Obtener stakeholders del proyecto
        const stakeholdersDelProyecto = projectStakeholders
            .filter(ps => ps.project_id === proyectoData.project_id)
            .map(ps => stakeholders.find(s => s.stakeholder_id === ps.stakeholder_id))
            .filter(Boolean)

        // Construir el equipo
        const equipo = stakeholdersDelProyecto.map(stakeholder => {
            const persona = persons.find(p => p.person_id === stakeholder.person_id) || {}
            const rol = roles.find(r => r.role_id === stakeholder.role_id) || {}
            return {
                nombre: persona.person_firstname || 'Desconocido',
                apellido: persona.person_lastname || '',
                rol: rol.role_description || 'No definido',
                role_id: stakeholder.role_id
            }
        })

        // Identificar al investigador principal
        // const investigadorPrincipalRole = roles.find(r => r.role_description === "Investigador Principal")
        // const investigador = equipo.find(miembro => miembro.role_id === investigadorPrincipalRole?.role_id)
        const getResponsable = (equipo, roles) => {
            const directorRole = roles.find(r => r.role_description === "Director")
            const director = equipo.find(miembro => miembro.role_id === directorRole?.role_id)
            if (director) return director

            const codirectorRole = roles.find(r => r.role_description === "Codirector")
            const codirector = equipo.find(miembro => miembro.role_id === codirectorRole?.role_id)
            if (codirector) return codirector

            const investigadorPrincipalRole = roles.find(r => r.role_description === "Investigador Principal")
            const investigadorPrincipal = equipo.find(miembro => miembro.role_id === investigadorPrincipalRole?.role_id)
            if (investigadorPrincipal) return investigadorPrincipal

            return null
        }

        const responsable = getResponsable(equipo, roles)

        // Formatear equipo con roles separados por comas
        const equipoFormateado = equipo.reduce((acc, miembro) => {
            // Agrupar por persona para combinar múltiples roles
            const existente = acc.find(m =>
                m.nombre === miembro.nombre &&
                m.apellido === miembro.apellido
            )

            if (existente) {
                existente.rol += `, ${miembro.rol}`
            } else {
                acc.push({ ...miembro })
            }
            return acc
        }, [])

        // Cargar imagen del proyecto
        let imagePath = proyectoData.project_image_path || null
        try {
            const loadedImage = await loadProjectImage(proyectoData.project_id)
            if (loadedImage) {
                imagePath = loadedImage
            }
        } catch (error) {
            console.error('Error loading project image:', error)
        }

        // Asignar datos al proyecto
        proyecto.value = {
            id: proyectoData.project_id,
            nombre_proyecto: proyectoData.project_name || 'Sin nombre',
            descripcion: proyectoData.project_description || 'Sin descripción',
            año: proyectoData.project_agno || 'Desconocido',
            // responsable: investigador ? `${investigador.nombre} ${investigador.apellido}` : "No asignado",
            responsable: responsable ? `${responsable.nombre} ${responsable.apellido}` : "No asignado",
            estado: proyectoData.estado || 'Activo',
            nivel: nivelDescripcion,
            equipo: equipoFormateado,
            documentos: [],
            imagen: imagePath
        }

        // Verificar si el texto está recortado
        const checkClamp = () => {
            nextTick(() => {
                if (descriptionElement.value) {
                    isClamped.value = descriptionElement.value.scrollHeight > descriptionElement.value.clientHeight
                }
            })
        }

        checkClamp()
        window.addEventListener('resize', checkClamp)

        onUnmounted(() => {
            window.removeEventListener('resize', checkClamp)
        })

    } catch (error) {
        console.error('Error al obtener los datos del proyecto:', error)
        proyecto.value = null
    }
})
</script>

<style scoped>
.custom-clamp {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 8;
    overflow: hidden;
}

/* En caso de que el navegador no soperte webkit-line-clamp */
@supports not (-webkit-line-clamp: 8) {
    .custom-clamp {
        max-height: 12rem;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        position: relative;
    }

    .custom-clamp::after {
        content: '...';
        position: absolute;
        bottom: 0;
        right: 0;
        background: white;
        padding-left: 4px;
    }
}
</style>