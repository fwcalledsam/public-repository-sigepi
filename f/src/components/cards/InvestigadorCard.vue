<template>
  <Card class="flex flex-col h-full">
    <CardHeader class="mb-[-12px]">
      <div class="flex items-center gap-4">
        <div
          class="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium text-lg">
          {{ investigador.nombre.charAt(0) }}{{ investigador.apellido.charAt(0) }}
        </div>
        <div>
          <CardTitle class="text-lg truncate max-w-[250px] text-[#008d85]">
            {{ investigador.nombre }} {{ investigador.apellido }}
          </CardTitle>
          <p class="text-xs text-muted-foreground">
            {{ investigador.rol }}
          </p>
        </div>
      </div>
    </CardHeader>
    <CardContent class="flex-1 grid gap-4">
      <div class="grid gap-2">
        <div class="flex items-center gap-2 text-sm text-muted-foreground">
          <TblrMapPin class="h-8 w-8 text-[#008d85]" />
          {{ investigador.ubicacion }}
        </div>
      </div>
    </CardContent>
    <div class="p-4 pt-0 flex justify-end">
      <Badge variant="outline" size="sm" class="bg-[#ddd]">
        <div v-if="hasWebsite" class="flex items-center gap-2 text-primary">
          <a :href="investigador.urlsite" target="_blank" rel="noopener noreferrer"
            class="flex items-center text-[#555]">
            <TblrLink class="h-4 w-4 mr-1" />
            Ver mas
          </a>
        </div>
      </Badge>

    </div>
  </Card>
</template>

<script setup>
import Card from '../common/Card.vue'
import CardHeader from '../common/CardHeader.vue'
import CardTitle from '../common/CardTitle.vue'
import CardContent from '../common/CardContent.vue'
import Badge from '../common/Badge.vue'

defineProps({
  investigador: {
    type: Object,
    required: true
  },
  hasWebsite: {
    type: Boolean,
    default: false
  }
})
</script>