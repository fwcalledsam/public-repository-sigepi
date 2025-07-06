<template>
    <Transition name="fade">
        <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
            <Card class="max-w-4xl w-full max-h-[90vh] overflow-auto">
                <CardHeader>
                    <div class="flex justify-between items-center">
                        <CardTitle>Guía de uso del Dashboard</CardTitle>
                    </div>
                    <CardDescription>Aprenda a utilizar todas las funcionalidades del sistema de gestión de proyectos de
                        investigación.</CardDescription>
                </CardHeader>

                <CardContent class="space-y-4">
                    <!-- Tabs Navigation -->
                    <div class="overflow-x-auto pb-2">
                        <div class="grid grid-cols-6 gap-1 bg-muted p-1 rounded-md w-max md:w-full">
                            <Button v-for="tab in tabs" :key="tab.value" variant="ghost" size="sm"
                                class="bg-tab min-w-[100px] md:min-w-0 text-xs md:text-sm"
                                :class="{ 'bg-background': activeTab === tab.value }" @click="activeTab = tab.value">
                                {{ tab.label }}
                            </Button>
                        </div>
                    </div>

                    <!-- General Tab -->
                    <div v-if="activeTab === 'general'" class="space-y-4">
                        <Card>

                            <CardHeader>
                                <CardTitle class="text-lg">Bienvenido al Sistema de Gestión de Proyectos</CardTitle>
                            </CardHeader>

                            <CardContent>
                                <p>
                                    Este sistema le permite administrar de manera eficiente todos los aspectos
                                    relacionados
                                    con los
                                    proyectos de investigación de su institución.
                                </p>

                                <div class="flex flex-col md:flex-row gap-6">
                                    <!-- Lista de secciones generales (izquierda) -->
                                    <div class="space-y-4 mt-6 flex-1">
                                        <div v-for="section in generalSections" :key="section.title"
                                            class="flex items-start gap-3">
                                            <Badge variant="secondary"
                                                class="relative h-5 w-5 flex items-center justify-center p-0">
                                                <component :is="section.icon" class="absolute h-3 w-3" />
                                            </Badge>
                                            <div>
                                                <h4 class="font-medium">{{ section.title }}</h4>
                                                <p class="text-sm text-muted-foreground">
                                                    {{ section.description }}
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Flujo recomendado (derecha) -->
                                    <div class="md:w-1/3 mt-6">
                                        <Card class="bg-muted/30">
                                            <div class="flex-1">
                                                <CardHeader>
                                                    <div class="flex items-center gap-2">
                                                        <Badge
                                                            class="relative h-8 w-8 flex items-center justify-center p-0">
                                                            <TblrAlertTriangle
                                                                class="absolute h-6 w-6 fill-amber-400" />
                                                        </Badge>
                                                        <CardTitle class="text-lg">Flujo recomendado</CardTitle>
                                                    </div>
                                                    <CardDescription>Sigue este orden para un correcto funcionamiento
                                                    </CardDescription>
                                                </CardHeader>
                                                <CardContent>
                                                    <ol class="list-decimal pl-5 space-y-2 text-sm">
                                                        <li>Crear roles necesarios</li>
                                                        <li>Establecer niveles de proyecto</li>
                                                        <li>Registrar personas con rol inicial</li>
                                                        <li>Crear proyectos con nivel asignado</li>
                                                        <li>Asignar personas a proyectos</li>
                                                    </ol>
                                                </CardContent>
                                            </div>
                                        </Card>
                                    </div>
                                </div>
                            </CardContent>

                        </Card>
                    </div>

                    <!-- Projects Tab -->
                    <div v-if="activeTab === 'proyectos'" class="space-y-4">
                        <Card>
                            <CardHeader>
                                <div class="flex items-center gap-2">
                                    <Badge variant="secondary"
                                        class="relative h-5 w-5 flex items-center justify-center p-0">
                                        <HrsldBriefcase class="absolute h-3 w-3" />
                                    </Badge>
                                    <CardTitle class="text-lg">Gestión de Proyectos</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    La sección de proyectos le permite administrar todos los proyectos de investigación
                                    registrados en el
                                    sistema.
                                </p>

                                <div class="space-y-6 mt-4">
                                    <div>
                                        <h4 class="font-medium mb-2">Crear un nuevo proyecto</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Haga clic en el botón "Nuevo Proyecto" en la parte superior derecha.
                                            </li>
                                            <li>Complete el formulario con la información requerida del proyecto.</li>
                                            <li>Asigne un nivel al proyecto seleccionándolo del menú desplegable.</li>
                                            <li>Suba la imagen del proyecto, si este tiene, de no ser asi se le asignara
                                                un placeholder automatico.</li>
                                            <li>Haga clic en "Crear Proyecto" para guardar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Editar un proyecto existente</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Localice el proyecto que desea modificar en la tabla de proyectos.</li>
                                            <li>Haga clic en el botón "Editar" en la fila correspondiente.</li>
                                            <li>Actualice la información necesaria en el formulario que aparece.</li>
                                            <li>Haga clic en "Guardar Cambios" para actualizar la información.</li>
                                        </ol>
                                    </div>

                                    <Card class="bg-muted/30">
                                        <CardHeader>
                                            <CardTitle class="text-lg">Consejos útiles</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <ul class="list-disc pl-5 space-y-2">
                                                <li>Utilice descripciones claras y concisas para facilitar la
                                                    identificación
                                                    de los proyectos.</li>
                                                <li>Asigne niveles adecuados a los proyectos para facilitar su
                                                    clasificación
                                                    y posterior análisis.</li>
                                            </ul>
                                        </CardContent>
                                    </Card>
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    <!-- Person Tab -->
                    <div v-if="activeTab === 'personas'" class="space-y-4">
                        <Card>
                            <CardHeader>
                                <div class="flex items-center gap-2">
                                    <Badge variant="secondary"
                                        class="relative h-5 w-5 flex items-center justify-center p-0">
                                        <HrsldUsers class="absolute h-3 w-3" />
                                    </Badge>
                                    <CardTitle class="text-lg">Gestión de Personas</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    En esta sección puede administrar a todas las personas involucradas en los proyectos
                                    de
                                    investigación.
                                </p>

                                <div class="space-y-6 mt-4">
                                    <div>
                                        <h4 class="font-medium mb-2">Registrar una nueva persona</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Haga clic en el botón "Nueva Persona" en la parte superior derecha.</li>
                                            <li>Ingrese la informacion solicitada de la persona.</li>
                                            <li>Haga clic en "Crear Persona" para guardar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Editar información de una persona</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Localice a la persona que desea modificar en la tabla.</li>
                                            <li>Haga clic en el botón "Editar" en la fila correspondiente.</li>
                                            <li>Actualice la información necesaria en el formulario que aparece.</li>
                                            <li>Haga clic en "Guardar Cambios" para actualizar la información.</li>
                                        </ol>
                                    </div>

                                    <Card class="bg-muted/30">
                                        <CardHeader>
                                            <CardTitle class="text-lg">Información adicional</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p>
                                                Es necesario asignar un <span class="font-bold">rol inicial
                                                    obligatorio</span> a cada persona
                                                registrada, garantizando consistencia en la estructura organizacional.
                                                Este
                                                rol puede modificarse posteriormente para adaptarse a los requerimientos
                                                específicos de cada proyecto, permitiendo flexibilidad en la asignación
                                                de
                                                responsabilidades.
                                            </p>
                                        </CardContent>
                                    </Card>
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    <!-- Roles Tab -->
                    <div v-if="activeTab === 'roles'" class="space-y-4">
                        <Card>
                            <CardHeader>
                                <div class="flex items-center gap-2">
                                    <Badge variant="secondary"
                                        class="relative h-5 w-5 flex items-center justify-center p-0">
                                        <TblrPuzzle class="absolute h-3 w-3" />
                                    </Badge>
                                    <CardTitle class="text-lg">Gestión de Roles</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    Esta sección le permite definir y administrar los diferentes roles que pueden
                                    desempeñar
                                    las personas en
                                    los proyectos.
                                </p>

                                <div class="space-y-6 mt-4">
                                    <div>
                                        <h4 class="font-medium mb-2">Crear un nuevo rol</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Haga clic en el botón "Nuevo Rol" en la parte superior derecha.</li>
                                            <li>Ingrese el nombre del rol en el campo correspondiente.</li>
                                            <li>Haga clic en "Crear Rol" para guardar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Editar un rol existente</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Localice el rol que desea modificar en la tabla.</li>
                                            <li>Haga clic en el botón "Editar" en la fila correspondiente.</li>
                                            <li>Actualice el nombre del rol en el formulario que aparece.</li>
                                            <li>Haga clic en "Guardar Cambios" para actualizar la información.</li>
                                        </ol>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    <!-- Levels Tab -->
                    <div v-if="activeTab === 'niveles'" class="space-y-4">
                        <Card>
                            <CardHeader>
                                <div class="flex items-center gap-2">
                                    <Badge variant="secondary"
                                        class="relative h-5 w-5 flex items-center justify-center p-0">
                                        <TblrAdjustments class="absolute h-3 w-3" />
                                    </Badge>
                                    <CardTitle class="text-lg">Niveles de Proyecto</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    En esta sección puede definir las categorías o niveles en los que se clasifican los
                                    proyectos de
                                    investigación.
                                </p>

                                <div class="space-y-6 mt-4">
                                    <div>
                                        <h4 class="font-medium mb-2">Crear un nuevo nivel</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Haga clic en el botón "Nuevo Nivel" en la parte superior derecha.</li>
                                            <li>Ingrese el nombre del nivel en el campo correspondiente.</li>
                                            <li>Haga clic en "Crear Nivel" para guardar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Editar un nivel existente</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Localice el nivel que desea modificar en la tabla.</li>
                                            <li>Haga clic en el botón "Editar" en la fila correspondiente.</li>
                                            <li>Actualice el nombre del nivel en el formulario que aparece.</li>
                                            <li>Haga clic en "Guardar Cambios" para actualizar la información.</li>
                                        </ol>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    <!-- Assignments Tab -->
                    <div v-if="activeTab === 'asignaciones'" class="space-y-4">
                        <Card>
                            <CardHeader>
                                <div class="flex items-center gap-2">
                                    <Badge variant="secondary"
                                        class="relative h-5 w-5 flex items-center justify-center p-0">
                                        <TblrReplaceFilled class="absolute h-3 w-3" />
                                    </Badge>
                                    <CardTitle class="text-lg">Asignaciones de Proyectos</CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p>
                                    Esta sección le permite vincular personas a proyectos específicos con roles
                                    determinados
                                    para establecer
                                    responsabilidades.
                                </p>

                                <div class="space-y-6 mt-4">
                                    <div>
                                        <h4 class="font-medium mb-2">Crear una nueva asignación</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Haga clic en el botón "Nueva Asignación" en la parte superior derecha.
                                            </li>
                                            <li>Seleccione la persona que desea asignar.</li>
                                            <li>Seleccione el proyecto al que será asignada.</li>
                                            <li>Seleccione uno o más roles que desempeñará en el proyecto.</li>
                                            <li>Haga clic en "Crear Asignación" para guardar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Editar una asignación existente</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Expanda el proyecto correspondiente haciendo clic en su nombre.</li>
                                            <li>Localice la persona cuya asignación desea modificar.</li>
                                            <li>Haga clic en el icono de edición junto a su nombre.</li>
                                            <li>Actualice los roles asignados según sea necesario.</li>
                                            <li>Haga clic en "Guardar Cambios" para actualizar la información.</li>
                                        </ol>
                                    </div>

                                    <div>
                                        <h4 class="font-medium mb-2">Eliminar una asignación</h4>
                                        <ol class="list-decimal pl-5 space-y-2">
                                            <li>Expanda el proyecto correspondiente haciendo clic en su nombre.</li>
                                            <li>Localice la persona cuya asignación desea eliminar.</li>
                                            <li>Haga clic en el icono de papelera junto a su nombre.</li>
                                            <li>Confirme la eliminación en el diálogo que aparece.</li>
                                        </ol>
                                    </div>

                                    <Card class="bg-muted/30">
                                        <CardHeader>
                                            <CardTitle class="text-lg">Consejos útiles</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <ul class="list-disc pl-5 space-y-2">
                                                <li>Una persona puede tener múltiples roles en un mismo proyecto,
                                                    reflejando
                                                    diferentes responsabilidades.</li>
                                                <li>Revise periódicamente las asignaciones para asegurarse de que
                                                    reflejen
                                                    la estructura actual del equipo.</li>
                                            </ul>
                                        </CardContent>
                                    </Card>
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </CardContent>

                <CardFooter class="flex justify-end">
                    <Button @click="onClose" class="px-6">Entendido</Button>
                </CardFooter>
            </Card>
        </div>
    </Transition>
</template>

<script setup>
import Badge from '../../../components/common/Badge.vue'
import CardContent from '../../../components/common/CardContent.vue'
import Button from '../../../components/common/Button.vue'
import Card from '../../../components/common/Card.vue'
import CardHeader from '../../../components/common/CardHeader.vue'
import CardTitle from '../../../components/common/CardTitle.vue'
import CardFooter from '../../../components/common/CardFooter.vue'
import CardDescription from '../../../components/common/CardDescription.vue'
import { ref, watch } from 'vue'

const props = defineProps({
    isOpen: Boolean,
    onClose: Function,
    initialTab: {
        type: String,
        default: 'general'
    }
});

const activeTab = ref(props.initialTab);

watch(() => props.initialTab, (newVal) => {
    activeTab.value = newVal;
});

const tabs = [
    { value: 'general', label: 'General' },
    { value: 'proyectos', label: 'Proyectos' },
    { value: 'personas', label: 'Personas' },
    { value: 'roles', label: 'Roles' },
    { value: 'niveles', label: 'Niveles' },
    { value: 'asignaciones', label: 'Asignaciones' }
]

const generalSections = [
    {
        title: 'Proyectos',
        description: 'Gestione los proyectos de investigación, incluyendo su información básica, estado y documentación asociada.',
        icon: 'HrsldBriefcase'
    },
    {
        title: 'Personas',
        description: 'Administre los investigadores y colaboradores que participan en los diferentes proyectos.',
        icon: 'HrsldUsers'
    },
    {
        title: 'Roles',
        description: 'Configure los diferentes roles que pueden desempeñar las personas dentro de los proyectos.',
        icon: 'TblrPuzzle'
    },
    {
        title: 'Niveles de Proyecto',
        description: 'Defina las categorías o niveles en los que se clasifican los proyectos de investigación.',
        icon: 'TblrAdjustments'
    },
    {
        title: 'Asignaciones de Proyectos',
        description: 'Vincule personas a proyectos específicos con roles determinados para establecer responsabilidades.',
        icon: 'TblrReplaceFilled'
    },
    {
        title: 'Carga de Datos',
        description: 'Importe datos masivamente desde archivos CSV para agilizar la carga de información.',
        icon: 'TblrUpload'
    }
]
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

.bg-tab:hover {
    background-color: #cbd5e1;
}
</style>