<template>
    <div class="flex min-h-screen w-full flex-col items-center justify-center bg-background">
        <div class="mx-auto flex max-w-[420px] flex-col items-center justify-center text-center">
            <div class="flex h-40 w-40 items-center justify-center rounded-full bg-muted">
                <TblrAlertTriangle class="h-20 w-20 text-muted-foreground" />
            </div>
            <h3 class="mt-6 text-2xl font-semibold">Página no encontrada</h3>
            <p class="mb-6 mt-2 text-center text-muted-foreground">
                Lo sentimos, la página que estás buscando no existe o ha sido movida.
            </p>
            <router-link to="/"
                class="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                <HrsldArrowLeft class="h-5 w-5 mr-4" />
                Volver al inicio
            </router-link>
        </div>
    </div>
</template>

<script setup>
// No additional setup needed
</script>