<template>
    <div v-if="variant === 'home-researcher'"
        class="flex flex-col items-center justify-center py-16 text-muted-foreground">
        <p class="text-xl font-medium">{{ title }}</p>
        <p class="text-sm mb-4 max-w-md">{{ description }}</p>
    </div>

    <div v-else class="flex flex-col items-center justify-center px-4 py-16 text-center text-muted-foreground">
        <p class="text-xl font-medium">{{ title }}</p>
        <p class="text-sm mb-4">{{ description }}</p>
        <Button @click="onAction">
            <component :is="icon" class="h-4 w-4 mr-2" />
            {{ actionText }}
        </Button>
    </div>
</template>

<script setup>
import Button from '../common/Button.vue'

const props = defineProps({
    title: {
        type: String,
        default: 'No hay registros'
    },
    description: {
        type: String,
        default: 'Comience creando su primer registro'
    },
    actionText: {
        type: String,
        required: true
    },
    icon: {
        type: Object,
        required: true
    },
    onAction: {
        type: Function,
        required: true
    },
    variant: {
        type: String,
        default: 'default',
        validator: (value) => ['default', 'home-researcher'].includes(value)
    }
})
</script>