<template>
  <Card class="overflow-hidden">
    <template v-if="loading">
      <!-- SplashScreen mientras carga -->
      <div class="relative h-48 w-full bg-gray-200 animate-pulse"></div>
      <CardHeader>
        <CardTitle class="h-6 bg-gray-200 rounded animate-pulse"></CardTitle>
      </CardHeader>
      <CardContent class="space-y-3">
        <div class="h-4 bg-gray-200 rounded animate-pulse"></div>
        <div class="h-4 bg-gray-200 rounded animate-pulse w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded animate-pulse w-1/2"></div>

        <div class="flex flex-wrap gap-2 mt-3">
          <div v-for="i in 3" :key="i" class="h-6 w-16 bg-gray-200 rounded-full animate-pulse"></div>
        </div>

        <div class="mt-4 grid gap-2 text-xs">
          <div class="h-4 bg-gray-200 rounded animate-pulse w-1/3"></div>
          <div class="h-4 bg-gray-200 rounded animate-pulse w-2/3"></div>
          <div class="h-4 bg-gray-200 rounded animate-pulse w-1/4"></div>
        </div>
      </CardContent>
      <CardFooter class="flex justify-end">
        <div class="h-8 w-24 bg-gray-200 rounded animate-pulse"></div>
      </CardFooter>
    </template>

    <template v-else>
      <!-- Contenido real cuando ya está cargado -->
      <div class="relative h-48 w-full">
        <img :src="proyecto.imagen" :alt="`Imagen de ${proyecto.titulo}`" class="object-cover w-full h-full" />
      </div>
      <CardHeader>
        <CardTitle class="line-clamp-1 text-[#008d85]">{{ proyecto.titulo }}</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="text-sm text-muted-foreground line-clamp-3">{{ proyecto.descripcion }}</div>

        <!-- Agregamos los tags usando Badge -->
        <div class="flex flex-wrap gap-2 mt-3">
          <Badge v-for="(keyword, index) in keywordsList" :key="index" variant="destructive"
            class="bg-primary text-primary-foreground hover:bg-primary/80 max-w-[130px] truncate"
            :style="{ backgroundColor: '#f0f0f0', color: '#999' }" :title="keyword.trim()">
            #{{ keyword.trim() }}
          </Badge>
        </div>

        <div class="mt-4 grid gap-2 text-xs">
          <div>
            <span class="font-medium">Año:</span> {{ proyecto.año }}
          </div>
          <div>
            <span class="font-medium">Responsable del Proyecto:</span> {{ proyecto.investigadorPrincipal }}
          </div>
          <div>
            <span class="font-medium">Nivel:</span> {{ proyecto.nivel }}
          </div>
        </div>
      </CardContent>
      <CardFooter class="flex justify-end">
        <Button variant="outline" size="sm" class="bg-[#ddd]">
          <router-link class="text-[#555]" :to="`/proyectos/${proyecto.id}`">Ver detalles</router-link>
        </Button>
      </CardFooter>
    </template>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import Card from '../common/Card.vue'
import CardHeader from '../common/CardHeader.vue'
import CardTitle from '../common/CardTitle.vue'
import CardContent from '../common/CardContent.vue'
import CardFooter from '../common/CardFooter.vue'
import Button from '../common/Button.vue'
import Badge from '../common/Badge.vue'

const props = defineProps({
  proyecto: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const keywordsList = computed(() => {
  if (!props.proyecto.project_keywords || props.proyecto.project_keywords.trim() === '') {
    return []
  }

  return props.proyecto.project_keywords
    .split(',')
    .map(k => k.trim())
    .filter(k => k.length > 0)
    .slice(0, 5) // Mostrar máximo 5 keywords
})
</script>