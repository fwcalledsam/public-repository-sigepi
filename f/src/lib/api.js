import api from "./AxiosCache";

// Auth API
export const authApi = {
    login: (username, password) => api.post("/login", { username, password }),
    logout: () => api.post("/logout"),
};

// Persons API
export const personsApi = {
    getAll: () => api.get("/persons"),
    create: (data) => api.post("/persons", data),
    update: (id, data) => api.put(`/persons/${id}`, data),
    delete: (id) => api.delete(`/persons/${id}`),
};

// Roles API
export const rolesApi = {
    getAll: () => api.get("/roles"),
    create: (data) => api.post("/roles", data),
    update: (id, data) => api.put(`/roles/${id}`, data),
    delete: (id) => api.delete(`/roles/${id}`),
};

// Stakeholders API
export const stakeholdersApi = {
    getAll: () => api.get("/stakeholders"),
    create: (data) => api.post("/stakeholders", data),
    update: (id, data) => api.put(`/stakeholders/${id}`, data),
    delete: (id) => api.delete(`/stakeholders/${id}`),
};

// Levels API
export const levelsApi = {
    getAll: () => api.get("/levels"),
    create: (data) => api.post("/levels", data),
    update: (id, data) => api.put(`/levels/${id}`, data),
    delete: (id) => api.delete(`/levels/${id}`),
};

// Projects API
export const projectsApi = {
    getAll: () => api.get("/projects"),
    create: (data) => api.post("/projects", data),
    update: (id, data) => api.put(`/projects/${id}`, data),
    delete: (id) => api.delete(`/projects/${id}`),
};

// Project Stakeholders API
export const projectStakeholdersApi = {
    getAll: () => api.get("/project_stakeholders"),
    create: (data) => api.post("/project_stakeholders", data),
    update: (id, data) => api.put(`/project_stakeholders/${id}`, data),
    delete: (id) => api.delete(`/project_stakeholders/${id}`),
};

// Project Images API
export const projectImagesApi = {
    upload: (projectId, file) => {
        const formData = new FormData();
        formData.append("file", file);
        return api.post(`/projects/${projectId}/upload-image?_=${Date.now()}`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
        });
    },
    get: (projectId) => api.get(`/projects/${projectId}/image?_=${Date.now()}`, {
        responseType: 'blob',
        headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    }),
    delete: (projectId) => api.delete(`/projects/${projectId}/delete-image`),
    update: (projectId, file) => {
        const formData = new FormData();
        formData.append("file", file);
        return api.put(`/projects/${projectId}/update-image`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
        });
    }
};

export default {
    auth: authApi,
    persons: personsApi,
    roles: rolesApi,
    stakeholders: stakeholdersApi,
    levels: levelsApi,
    projects: projectsApi,
    projectStakeholders: projectStakeholdersApi,
    projectImages: projectImagesApi,
};