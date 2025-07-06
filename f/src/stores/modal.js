import { defineStore } from "pinia"
import { ref } from "vue"

export const useModalStore = defineStore("modal", () => {
  const isCreateModalOpen = ref(false)
  const isEditModalOpen = ref(false)
  const isDeleteAlertOpen = ref(false)
  const isUploadModalOpen = ref(false)
  const isGuideModalOpen = ref(false)
  
  const currentItem = ref(null)

  const isAlertOpen = ref(false)
  const alertConfig = ref({
    title: 'Alerta',
    message: '',
    confirmText: 'Aceptar',
    cancelText: 'Cancelar',
    loadingText: 'Procesando...',
    confirmVariant: 'default',
    showCancel: true,
    onConfirm: () => Promise.resolve()
  })

  // =====================================================================

  function openCreateModal(item = null) {
    if (item) {
      currentItem.value = item
    }
    isCreateModalOpen.value = true
  }

  function closeCreateModal() {
    isCreateModalOpen.value = false
    currentItem.value = null
  }

  // =====================================================================

  function openEditModal(item) {
    closeAllModals()
    currentItem.value = item
    isEditModalOpen.value = true
  }

  function closeEditModal() {
    isEditModalOpen.value = false
    currentItem.value = null
  }

  // =====================================================================

  function openDeleteAlert(item) {
    closeAllModals()
    currentItem.value = item
    isDeleteAlertOpen.value = true
  }

  function closeDeleteAlert() {
    isDeleteAlertOpen.value = false
    currentItem.value = null
  }

  // =====================================================================

  function openUploadModal() {
    isUploadModalOpen.value = true
  }

  function closeUploadModal() {
    isUploadModalOpen.value = false
  }

  // =====================================================================

  function openAlert(config) {
    closeAllModals()
    alertConfig.value = {
      ...alertConfig.value,
      ...config
    }
    isAlertOpen.value = true
  }

  function closeAlert() {
    isAlertOpen.value = false
  }

  // Función para cerrar todos los modales
  function closeAllModals() {
    isCreateModalOpen.value = false
    isEditModalOpen.value = false
    isDeleteAlertOpen.value = false
    isUploadModalOpen.value = false
    isAlertOpen.value = false
  }

  // =====================================================================

  function showAlert(message, title = 'Alerta') {
    openAlert({
      title,
      message,
      showCancel: false,
      confirmText: 'OK'
    })
  }

  function showAlertReload(message, title = 'Alerta') {
    openAlert({
      title,
      message,
      showCancel: false,
      confirmText: 'OK',
      onConfirm: () => {
        window.location.reload();
      }
    });
  }

  // =====================================================================

  function showConfirm(message, title = 'Confirmar') {
    return new Promise((resolve) => {
      openAlert({
        title,
        message,
        onConfirm: () => resolve(true),
        confirmVariant: 'destructive',
        showCancel: true,
        cancelText: 'Cancelar',
        confirmText: 'Confirmar'
      })

      // Manejar close event
      const unsubscribe = this.$onAction(({ name, after }) => {
        if (name === 'closeAlert') {
          after(() => {
            resolve(false)
            unsubscribe()
          })
        }
      })
    })
  }

  // =====================================================================

  function openGuideModal() {
    isGuideModalOpen.value = true;
  }

  function closeGuideModal() {
    isGuideModalOpen.value = false;
  }

  // =====================================================================

  return {
    isCreateModalOpen,
    isEditModalOpen,
    isDeleteAlertOpen,
    isUploadModalOpen,
    currentItem,
    // ================    
    isAlertOpen,
    alertConfig,
    // ================
    isGuideModalOpen,
    // ================= //
    openCreateModal,
    closeCreateModal,
    openEditModal,
    closeEditModal,
    openDeleteAlert,
    closeDeleteAlert,
    openUploadModal,
    closeUploadModal,
    // ================    
    openAlert,
    closeAlert,
    showAlert,
    showAlertReload,
    showConfirm,
    // ================
    closeAllModals,
    // ================
    openGuideModal,
    closeGuideModal,
  }
})