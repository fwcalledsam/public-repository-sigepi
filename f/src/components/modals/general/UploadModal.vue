<template>
    <Transition name="fade">
        <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div class="relative w-full max-w-[550px] rounded-lg bg-background p-6 shadow-lg">
                <div class="flex flex-col space-y-1.5">

                    <h3 class="text-lg font-semibold leading-none tracking-tight flex items-center gap-2">
                        Cargar datos desde archivo
                        <!-- Botón de guía -->
                        <a href="../../../../public/guideTemplate.html" target="_blank" rel="noopener noreferrer"
                            class="p-1 rounded-md hover:bg-gray-100 text-muted-foreground transition-colors"
                            title="Mostrar guía en nueva pestaña">
                            <HrsldBook class="h-5 w-5" />
                        </a>
                    </h3>

                    <p class="text-sm text-muted-foreground">
                        Seleccione un archivo Excel para cargar datos masivamente al sistema.
                    </p>
                </div>

                <div v-if="uploadStatus === 'idle'">
                    <div class="mt-4 border-2 border-dashed rounded-lg p-8 text-center"
                        :class="isDragging ? 'border-primary bg-primary/5' : 'border-muted-foreground/20'"
                        @dragover.prevent="isDragging = true" @dragleave="isDragging = false"
                        @drop.prevent="handleDrop">
                        <div v-if="!file" class="flex flex-col items-center">
                            <TblrUpload class="h-10 w-10 text-muted-foreground mb-4" />
                            <p class="text-sm text-muted-foreground mb-2">
                                Arrastre y suelte su archivo aquí, o
                            </p>
                            <label for="file-upload" class="cursor-pointer">
                                <span
                                    class="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground ring-offset-background transition-colors hover:bg-primary/90">
                                    Seleccionar archivo
                                </span>
                                <input id="file-upload" type="file" accept=".xlsx,.xls" class="sr-only"
                                    @change="handleFileChange" />
                            </label>
                        </div>
                        <div v-else class="flex items-center justify-between">
                            <div class="flex items-center">
                                <HrsldDocumentText class="h-8 w-8 text-primary mr-3" />
                                <div class="text-left">
                                    <p class="font-medium">{{ file.name }}</p>
                                    <p class="text-xs text-muted-foreground">
                                        {{ (file.size / 1024).toFixed(2) }} KB
                                    </p>
                                </div>
                            </div>
                            <button class="rounded-md p-1 hover:bg-muted" @click="clearFile">
                                <TblrXFill class="h-6 w-6 fill-red-700" />
                            </button>
                        </div>
                    </div>

                    <div v-if="file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) && sheetNames.length > 1"
                        class="mt-4">
                        <div class="flex items-center mb-2">
                            <h4 class="text-sm font-medium mb-2">Vista previa:</h4>
                            <select v-model="selectedSheet" @change="updatePreviewForSelectedSheet"
                                class="ml-2 text-xs border rounded px-2 py-1">
                                <option v-for="(sheet, index) in sheetNames" :key="index" :value="sheet">
                                    {{ sheet }}
                                </option>
                            </select>
                        </div>
                    </div>

                    <div v-if="previewData.length > 0" class="mt-4">
                        <div class="border rounded-md overflow-x-auto">
                            <table class="w-full text-xs">
                                <thead class="bg-muted">
                                    <tr>
                                        <th v-for="(header, i) in previewData[0]" :key="i"
                                            class="px-3 py-2 text-left font-medium">
                                            {{ header }}
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(row, i) in previewData.slice(1)" :key="i" class="border-t">
                                        <td v-for="(cell, j) in row" :key="j" class="px-3 py-2">
                                            <span :title="cell">{{ truncateText(cell) }}</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="flex justify-end space-x-2 mt-4">
                        <Button type="button" variant="outline" @click="downloadTemplate" class="text-sm mr-[176px]">
                            <TblrDownload class="h-4 w-4 mr-2" />
                            Plantilla
                        </Button>
                        <Button type="button" variant="outline" @click="onClose">
                            Cancelar
                        </Button>
                        <Button @click="handleUpload" :disabled="!file || isUploading">
                            {{ isUploading ? "Cargando..." : "Cargar datos" }}
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref } from 'vue'
import * as XLSX from 'xlsx'
import { useModalStore } from '../../../stores/modal'
import Button from '../../common/Button.vue'
import { uploadDataToAPI } from '../../../lib/uploadHandler'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true,
        default: false
    },
    onClose: {
        type: Function,
        required: true,
        validator: (value) => typeof value === 'function'
    }
})

const file = ref(null)
const isDragging = ref(false)
const isUploading = ref(false)
const uploadStatus = ref('idle')
const previewData = ref([])
const sheetNames = ref([])
const selectedSheet = ref('')
const workbook = ref(null)

const downloadTemplate = () => {
    const templateWorkbook = XLSX.utils.book_new();

    // Datos de ejemplo para cada hoja
    const exampleData = {
        'roles': [
            ['role_id', 'role_description'],
            [1, 'Director'],
            [2, 'Investigador Principal'],
            [3, 'Estudiante']
        ],
        'persons': [
            ['person_id', 'person_firstname', 'person_lastname', 'person_location', 'person_urlsite'],
            [1, 'María', 'García López', '', ''],
            [2, 'Carlos', 'Martínez Fernández', '', ''],
            [3, 'Ana', 'Rodríguez Sánchez', '', '']
        ],
        'stakeholders': [
            ['stakeholder_id', 'person_id', 'role_id'],
            [1, 1, 2],  // María como Investigador Principal
            [2, 2, 3],  // Carlos como Estudiante
            [3, 3, 3]   // Ana como Estudiante
        ],
        'levels': [
            ['level_id', 'level_description'],
            [1, 'Licenciatura'],
            [2, 'Maestría'],
            [3, 'Doctorado']
        ],
        'projects': [
            ['project_id', 'project_name', 'project_description', 'project_keywords', 'project_agno', 'level_id', 'project_image_path'],
            [1, 'Proyecto de ejemplo', 'Descripción breve del proyecto de investigación', 'investigación, ciencia', 2024, 2, '']
        ],
        'project_stakeholders': [
            ['prj_stk_id', 'project_id', 'stakeholder_id'],
            [1, 1, 1],  // María asociada al proyecto 1
            [2, 1, 2]   // Carlos asociado al proyecto 1
        ]
    };

    // Crear hojas con datos de ejemplo
    Object.entries(exampleData).forEach(([sheetName, data]) => {
        const worksheet = XLSX.utils.aoa_to_sheet(data);
        XLSX.utils.book_append_sheet(templateWorkbook, worksheet, sheetName);
    });

    // Descargar el archivo
    XLSX.writeFile(templateWorkbook, 'Plantilla_Proyectos.xlsx');
}

const processExcel = (workbook) => {
    try {
        const requiredSheets = {
            'roles': ['role_id', 'role_description'],
            'persons': ['person_id', 'person_firstname', 'person_lastname', 'person_location', 'person_urlsite'],
            'stakeholders': ['stakeholder_id', 'person_id', 'role_id'],
            'levels': ['level_id', 'level_description'],
            'projects': ['project_id', 'project_name', 'project_description', 'project_keywords', 'project_agno', 'level_id'],
            'project_stakeholders': ['prj_stk_id', 'project_id', 'stakeholder_id'],
        };

        const result = {};

        for (const [sheetName, requiredColumns] of Object.entries(requiredSheets)) {
            const worksheet = workbook.Sheets[sheetName];
            if (!worksheet) {
                throw new Error(`Falta la hoja requerida: ${sheetName}`);
            }

            const headers = XLSX.utils.sheet_to_json(worksheet, {
                header: 1,
                defval: null,
                range: 0
            })[0];

            if (!headers || headers.length === 0) {
                console.warn(`Hoja ${sheetName} no tiene encabezados`);
                continue;
            }

            const normalizedHeaders = headers
                .filter(Boolean)
                .map(h => h.toString().toLowerCase().trim().replace(/\s+/g, '_'));

            for (const column of requiredColumns) {
                if (!normalizedHeaders.includes(column.toLowerCase())) {
                    throw new Error(`Falta la columna "${column}" en la hoja ${sheetName}`);
                }
            }

            result[sheetName] = XLSX.utils.sheet_to_json(worksheet);
        }

        return result;
    } catch (error) {
        console.error('Error validando estructura del Excel:', error);
        throw error;
    }
}

const combineProjectData = (excelData) => {
    if (!excelData || !excelData.projects || !excelData.project_stakeholders ||
        !excelData.stakeholders || !excelData.persons || !excelData.roles) {
        return []
    }

    const { projects, project_stakeholders, stakeholders, persons, roles } = excelData

    return projects.map(project => {
        const prjStakeholders = project_stakeholders
            .filter(ps => ps.project_id == project.project_id)
            .map(ps => {
                const stakeholder = stakeholders.find(s => s.stakeholder_id == ps.stakeholder_id)
                if (stakeholder) {
                    const person = persons.find(p => p.person_id == stakeholder.person_id)
                    const role = roles.find(r => r.role_id == stakeholder.role_id)
                    return {
                        stakeholder_id: stakeholder.stakeholder_id,
                        person: person || null,
                        role: role || null,
                        display: person ? `${person.person_firstname} ${person.person_lastname} (${role ? role.role_description : 'Sin rol'})` : 'Desconocido'
                    }
                }
                return null
            }).filter(Boolean)

        return {
            ...project,
            stakeholders: prjStakeholders
        }
    })
}

const handleDrop = (e) => {
    isDragging.value = false
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        const droppedFile = e.dataTransfer.files[0]
        if (isValidFileType(droppedFile)) {
            file.value = droppedFile
            parseFile(droppedFile)
        }
    }
}

const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
        const selectedFile = e.target.files[0]
        if (isValidFileType(selectedFile)) {
            file.value = selectedFile
            parseFile(selectedFile)
        }
    }
}

const isValidFileType = (file) => {
    const validExtensions = ['.xlsx', '.xls']
    const fileName = file.name.toLowerCase()
    return validExtensions.some(ext => fileName.endsWith(ext))
}

const parseFile = (file) => {
    const fileName = file.name.toLowerCase()
    if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
        parseExcel(file)
    }
}

const parseExcel = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        try {
            const data = new Uint8Array(e.target.result)
            workbook.value = XLSX.read(data, {
                type: 'array',
                codepage: 65001,
                raw: false
            })
            sheetNames.value = workbook.value.SheetNames
            selectedSheet.value = sheetNames.value[0]
            updatePreviewForSelectedSheet()
        } catch (error) {
            console.error('Error al parsear el archivo Excel:', error)
        }
    }
    reader.readAsArrayBuffer(file)
}

const updatePreviewForSelectedSheet = () => {
    if (!workbook.value || !selectedSheet.value) return

    try {
        const worksheet = workbook.value.Sheets[selectedSheet.value]
        const jsonData = XLSX.utils.sheet_to_json(worksheet, {
            header: 1,
            defval: '',
            raw: false
        })

        previewData.value = jsonData
            .filter(row => row.some(cell => cell !== undefined && cell !== null && cell !== ''))
            .slice(0, 5)
    } catch (error) {
        console.error('Error al actualizar la vista previa:', error)
        previewData.value = []
    }
}

const clearFile = () => {
    file.value = null
    previewData.value = []
    sheetNames.value = []
    selectedSheet.value = ''
    workbook.value = null
}

const handleUpload = async () => {
    if (!file.value) return;

    isUploading.value = true;
    uploadStatus.value = 'idle';

    try {
        let processedData = null;
        const fileName = file.value.name.toLowerCase();

        if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
            const excelBuffer = await readFileAsArrayBuffer(file.value);
            const workbook = XLSX.read(excelBuffer, { type: 'array' });

            const excelData = processExcel(workbook);
            const combinedProjects = combineProjectData(excelData);
            processedData = {
                excelSheets: excelData,
                proyectosCombinados: combinedProjects
            };

            localStorage.setItem('projectData', JSON.stringify(processedData));
            const uploadResult = await uploadDataToAPI();

            if (uploadResult.success) {
                uploadStatus.value = "success";
                localStorage.removeItem('projectData');

                if (uploadResult.details) {
                    const modal = useModalStore();
                    modal.showAlertReload(
                        `Datos cargados exitosamente. ${uploadResult.details.imported || ''} registros importados.`,
                        'Archivo cargado exitosamente'
                    )
                }
            } else {
                uploadStatus.value = "error";
                throw new Error(uploadResult.message || 'Error al subir a la API');
            }

        } else {
            throw new Error('Solo se aceptan archivos Excel (.xlsx, .xls)');
        }
    } catch (error) {
        console.error('Error en handleUpload:', error);
        uploadStatus.value = "error";

        const modal = useModalStore()

        if (error.message.includes('Falta la hoja')) {
            modal.showAlertReload(
                `El archivo no tiene la estructura requerida.`,
                'Error de estructura'
            );
        } else if (error.message.includes('Falta la columna')) {
            modal.showAlertReload(
                `Error en la estructura de columnas. ${error.message}\n\n Verifique los nombres de las columnas.`,
                'Error en columnas'
            );
        } else {
            modal.showAlertReload(
                // `Error al procesar el archivo: ${error.message || 'Verifique que el archivo tenga el formato correcto.'}`,
                `Error al procesar el archivo: Verifique que el archivo tenga el formato correcto.`,
                'Error al cargar el archivo'
            );
        }

    } finally {
        isUploading.value = false;

        if (uploadStatus.value === "success") {
            setTimeout(() => {
                clearFile();
                uploadStatus.value = "idle";
                props.onClose();
            }, 2000);
        }
    }
}

const readFileAsArrayBuffer = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = (e) => reject(e)
        reader.readAsArrayBuffer(file)
    })
}

const truncateText = (text, maxLength = 20) => {
    if (text === null || text === undefined) return ''
    if (typeof text !== 'string') text = String(text)
    text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text
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