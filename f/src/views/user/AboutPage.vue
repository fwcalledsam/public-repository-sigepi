<template>
    <div class="flex min-h-screen w-full flex-col">
        <NavBar :has-background="true" variant="default" />

        <main class="flex-1 p-4 md:p-6 pt-[80px] md:pt-[80px]">
            <div class="mx-auto max-w-6xl space-y-6">
                <!-- Sección superior con título y estadísticas -->
                <div class="flex flex-col md:flex-row gap-6 items-start">
                    <div class="flex-1 space-y-2">
                        <h1 class="text-3xl font-bold tracking-tight">Sobre Nosotros</h1>
                        <p class="text-lg text-muted-foreground">
                            El Grupo ALEF es un equipo multidisciplinario dedicado a la investigación de vanguardia y al
                            desarrollo de soluciones tecnológicas innovadoras.
                        </p>
                    </div>
                    <Card class="w-full md:w-72">
                        <CardHeader class="space-y-0">
                            <div class="flex justify-between">
                                <CardTitle class="text-sm font-medium">Fundación</CardTitle>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-[#008d85]" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3"
                                        d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div class="text-2xl font-bold text-[#008d85]">2025</div>
                            <p class="text-xs text-muted-foreground">CINVESTAV Tamaulipas</p>
                        </CardContent>
                    </Card>
                </div>

                <!-- Sección de valores -->
                <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card>
                        <CardHeader>
                            <div class="flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#008d85]" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                </svg>
                                <CardTitle>Colaboración</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <p class="text-sm text-muted-foreground">
                                Permite una comunicación fluida entre docentes, investigadores, personal administrativo
                                y estudiantes gracias a un entorno unificado de gestión de proyectos.
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <div class="flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#008d85]" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <CardTitle>Accesibilidad</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <p class="text-sm text-muted-foreground">
                                El sistema es accesible vía web y se adapta a distintos dispositivos, de modo que la
                                información está disponible para toda la comunidad académica.
                            </p>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <div class="flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#008d85]" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                                <CardTitle>Innovación abierta</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <p class="text-sm text-muted-foreground">
                                Fomentamos la colaboración con agentes externos (startups, universidades, otras
                                instituciones) y promovemos el intercambio de conocimientos.
                            </p>
                        </CardContent>
                    </Card>
                </div>

                <!-- Sección de historia -->
                <Card>
                    <CardHeader>
                        <CardTitle class="text-xl">Historia del Grupo ALEF</CardTitle>
                    </CardHeader>
                    <CardContent class="space-y-4">
                        <p>
                            El Grupo ALEF nació de un proyecto académico en el CINVESTAV Unidad Tamaulipas (Ciudad
                            Victoria) orientado a mejorar la gestión de proyectos de investigación.
                        </p>
                        <p>
                            Este proyecto fue desarrollado por un residente de Ingeniería en Sistemas Computacionales
                            bajo la supervisión del Dr. Edwyn Javier Aldana Bobadilla, incorporando tecnologías de
                            código abierto con un enfoque de escalabilidad y accesibilidad.
                        </p>
                        <p>
                            A partir de esa experiencia, el equipo se consolidó como una iniciativa tecnológica aplicada
                            a la investigación. Nuestra plataforma se diseñó con tecnologías abiertas, escalables y
                            centradas en el usuario, lo que ha permitido sentar las bases para innovar en la gestión
                            científica y atender las necesidades reales de docentes e investigadores.
                        </p>
                    </CardContent>
                </Card>
            </div>
        </main>
    </div>
</template>

<script setup>
import NavBar from '../../components/layout/NavBar.vue'
import Card from '../../components/common/Card.vue'
import CardHeader from '../../components/common/CardHeader.vue'
import CardTitle from '../../components/common/CardTitle.vue'
import CardContent from '../../components/common/CardContent.vue'
</script>