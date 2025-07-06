<template>
    <div class="flex min-h-screen items-center justify-center bg-muted/30 p-4 border-t-[9.5px] border-[#008d85]">
        <div class="mx-auto w-full max-w-md rounded-lg border bg-card text-card-foreground shadow-sm">

            <div class="flex flex-col space-y-1.5 p-6">
                <!-- Botón de regresar a homepage -->
                <div class="flex space-x-[4%] md:space-x-[15%]">
                    <Button variant="ghost" size="icon" @click="$router.back()">
                        <HrsldArrowLeft class="h-5 w-5" />
                    </Button>
                    <router-link to="/" class="flex items-center justify-center">
                        <ImagoTipo class="h-20 w-auto flex items-center justify-center mb-2 mt-5" />
                    </router-link>
                </div>
            </div>

            <div class="px-6 pb-6">
                <div v-if="error"
                    class="mb-4 rounded-md border border-destructive/50 bg-destructive/10 px-3 py-2 text-sm text-destructive">
                    {{ error }}
                </div>
                <form @submit.prevent="handleSubmit">
                    <div class="grid gap-4">
                        <div class="grid gap-2">
                            <label for="email" class="text-sm font-medium leading-none">Correo electrónico</label>
                            <div class="relative">
                                <HrsldMail class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <input id="email" type="email" placeholder="usuario@cinvestav"
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 pl-10 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    v-model="email" required />
                            </div>
                        </div>
                        <div class="grid gap-2">
                            <div class="flex items-center justify-between">
                                <label for="password" class="text-sm font-medium leading-none">Contraseña</label>
                            </div>
                            <div class="relative">
                                <HrsldLock class="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                <input id="password" :type="showPassword ? 'text' : 'password'"
                                    placeholder="***********"
                                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 pl-10 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    v-model="password" required />
                                <button type="button" class="absolute right-3 top-3 h-4 w-4 text-muted-foreground"
                                    @click="togglePasswordVisibility">
                                    <HrsldEye v-if="showPassword" class="h-4 w-4" />
                                    <HrsldEyeOff v-else class="h-4 w-4" />
                                </button>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div class="flex items-center p-6 pt-0">
                <Button class="w-full bg-btn" @click="handleSubmit" :disabled="isLoading">
                    {{ isLoading ? "Iniciando sesión..." : "Iniciar sesión" }}
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authApi } from '../../lib/api';
import Button from '../../components/common/Button.vue'
import ImagoTipo from '../../assets/icons/ImagoTipo.vue'

const router = useRouter();
const email = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};

const handleSubmit = async () => {
    isLoading.value = true;
    error.value = '';

    try {
        const response = await authApi.login(email.value, password.value); // Usa la función de autenticación

        if (response.data.message === 'Login exitoso') {
            // Guarda el estado de autenticación en localStorage
            localStorage.setItem('isAuthenticated', 'true');
            // Redirige al dashboard del administrador
            router.push('/admin');
        } else {
            error.value = 'Credenciales incorrectas. Intente nuevamente.';
        }
    } catch (err) {
        error.value = 'Error al intentar iniciar sesión. Intente nuevamente.';
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
.bg-btn {
    background: #008d85;
    color: white;
}

.bg-btn:hover {
    background: #006b64;
}
</style>