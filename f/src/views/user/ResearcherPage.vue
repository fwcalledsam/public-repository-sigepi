<template>
    <div class="flex min-h-screen w-full flex-col">
        <NavBar :has-background="true" variant="default" />

        <main class="flex-1 p-4 md:p-6 pt-[70px] md:pt-[80px]">
            <div class="mx-auto max-w-6xl space-y-6">
                <div class="flex flex-col md:flex-row gap-6 items-start">
                    <div class="flex-1 space-y-2">
                        <h1 class="text-3xl font-bold tracking-tight">Investigadores</h1>
                        <p class="text-lg text-muted-foreground">
                            Conoce a las y los investigadores que forman parte del Grupo ALEF y han contribuido con sus
                            conocimientos en analítica de datos.
                        </p>
                    </div>
                    <Card class="w-full md:w-72">
                        <CardHeader class="space-y-0">
                            <div class="flex justify-between">
                                <CardTitle class="text-sm font-medium">Investigadores</CardTitle>
                                <HrsldUsers class="h-4 w-4 text-[#008d85]" />
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div class="text-2xl font-bold text-[#008d85]">{{ totalInvestigadores }}</div>
                            <p class="text-xs text-muted-foreground">Activos en diferentes áreas</p>
                        </CardContent>
                    </Card>
                </div>

                <div class="space-y-4">
                    <div class="relative w-full max-w-sm">
                        <svg xmlns="http://www.w3.org/2000/svg"
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        <input type="search" placeholder="Buscar investigadores..."
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 pl-8 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                            v-model="searchTerm" />
                    </div>

                    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        <template v-if="filteredInvestigadores.length > 0">
                            <InvestigadorCard v-for="investigador in filteredInvestigadores" :key="investigador.id"
                                :investigador="investigador" :has-website="!!investigador.urlsite" />
                        </template>
                        <template v-else>
                            <div class="col-span-full flex justify-center">
                                <EmptyState title="No se encontraron investigadores"
                                    description="No hay investigadores que coincidan con tu búsqueda o no hay estan registrados aún."
                                    variant="home-researcher" class="w-full max-w-md" />
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Button from '../../components/common/Button.vue'
import Card from '../../components/common/Card.vue'
import CardHeader from '../../components/common/CardHeader.vue'
import CardTitle from '../../components/common/CardTitle.vue'
import CardContent from '../../components/common/CardContent.vue'
import InvestigadorCard from '../../components/cards/InvestigadorCard.vue'
import EmptyState from '../../components/common/EmptyState.vue'
import { personsApi, stakeholdersApi, rolesApi } from '../../lib/api'
import NavBar from '../../components/layout/NavBar.vue'

const searchTerm = ref('')
const investigadores = ref([])
const totalInvestigadores = ref(0)

onMounted(async () => {
    try {
        const personsResponse = await personsApi.getAll()
        const persons = personsResponse.data || []

        const stakeholdersResponse = await stakeholdersApi.getAll()
        const stakeholders = stakeholdersResponse.data || []

        const rolesResponse = await rolesApi.getAll()
        const roles = rolesResponse.data || []

        investigadores.value = persons.map(person => {
            const personStakeholders = stakeholders
                .filter(s => s.person_id === person.person_id)
                .sort((a, b) => b.stakeholder_id - a.stakeholder_id)

            const latestStakeholders = personStakeholders.slice(0, 2)

            const rolesString = latestStakeholders.map(stakeholder => {
                const role = roles.find(r => r.role_id === stakeholder.role_id) || {}
                return role.role_description || 'Sin rol'
            }).join(', ')

            return {
                id: person.person_id,
                nombre: person.person_firstname || 'N/A',
                apellido: person.person_lastname || 'N/A',
                rol: rolesString,
                ubicacion: person.person_location || 'Centro de Investigación y de Estudios Avanzados del IPN, Unidad Tamaulipas',
                urlsite: person.person_urlsite || 'https://access.cinvestav.mx/investigacion/directorio-de-investigacion/category/unidad-tamaulipas'
            }
        })

        totalInvestigadores.value = investigadores.value.length
    } catch (error) {
        console.error('Error fetching data:', error)
    }
})

const filteredInvestigadores = computed(() => {
    return investigadores.value.filter(
        (investigador) =>
            investigador.nombre.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            investigador.apellido.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            investigador.rol.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            investigador.ubicacion.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
})
</script>