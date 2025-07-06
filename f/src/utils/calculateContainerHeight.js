import { onMounted, onBeforeUnmount, ref } from 'vue'

export function useContainerHeight(initialHeight = 385, headerHeight = 200, margin = 32) {
    const containerHeight = ref(initialHeight)

    function calculateHeight() {
        const windowHeight = window.innerHeight
        const calculatedHeight = Math.max(
            Math.min(windowHeight - headerHeight - margin, windowHeight * 0.8),
            initialHeight
        )
        containerHeight.value = calculatedHeight
    }

    onMounted(() => {
        calculateHeight()
        window.addEventListener('resize', calculateHeight)
    })

    onBeforeUnmount(() => {
        window.removeEventListener('resize', calculateHeight)
    })

    return { containerHeight }
}