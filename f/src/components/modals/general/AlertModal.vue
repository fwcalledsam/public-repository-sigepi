<template>
    <Transition name="fade">
        <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div class="relative w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
                <div class="flex flex-col space-y-2">
                    <h3 class="text-lg font-semibold leading-none tracking-tight">
                        {{ title }}
                    </h3>
                    <p class="text-sm text-muted-foreground">
                        {{ message }}
                    </p>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button type="button" variant="outline" @click="onClose" v-if="showCancel">
                        {{ cancelText }}
                    </Button>
                    <Button type="button" :variant="confirmVariant" @click="handleConfirm" :disabled="isLoading">
                        <span v-if="isLoading">{{ loadingText }}</span>
                        <span v-else>{{ confirmText }}</span>
                    </Button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref } from 'vue'
import Button from '../../common/Button.vue'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
    onClose: {
        type: Function,
        required: true
    },
    title: {
        type: String,
        default: 'Alerta'
    },
    message: {
        type: String,
        required: true
    },
    confirmText: {
        type: String,
        default: 'Aceptar'
    },
    cancelText: {
        type: String,
        default: 'Cancelar'
    },
    loadingText: {
        type: String,
        default: 'Procesando...'
    },
    confirmVariant: {
        type: String,
        default: 'default'
    },
    showCancel: {
        type: Boolean,
        default: true
    },
    onConfirm: {
        type: Function,
        default: () => { }
    }
})

const emit = defineEmits(['confirm'])
const isLoading = ref(false)

const handleConfirm = async () => {
    isLoading.value = true
    try {
        await props.onConfirm()
        emit('confirm')
        props.onClose()
    } catch (error) {
        console.error('Error in confirmation:', error)
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