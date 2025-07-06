
import {
    levelsApi,
    rolesApi,
    personsApi,
    stakeholdersApi,
    projectsApi,
    projectStakeholdersApi,
} from './api';

/**
 * Guarda los datos del localStorage en la base de datos mediante las APIs.
 * @returns {Promise<{success: boolean, message: string, details: object}>}
*/
export async function uploadDataToAPI() {
    try {
        // 1. Obtener datos del localStorage
        const storedData = localStorage.getItem('projectData');
        if (!storedData) throw new Error('No hay datos en localStorage');

        console.log('[1] Datos cargados desde localStorage:', JSON.parse(storedData));

        // 2. Parsear y normalizar datos
        let { excelSheets } = JSON.parse(storedData);
        excelSheets = normalizeExcelData(excelSheets);
        console.log('[2] Datos normalizados:', excelSheets);

        // 3. Estructura de resultados
        const results = {
            levels: [],
            roles: [],
            persons: [],
            stakeholders: [],
            projects: [],
            projectStakeholders: []
        };

        // 4. Obtener datos existentes
        console.log('[3] Obteniendo datos existentes...');
        const [existingRoles, existingLevels, existingPersons, existingStakeholders, existingProjects] = await Promise.all([
            rolesApi.getAll().then(res => res.data),
            levelsApi.getAll().then(res => res.data),
            personsApi.getAll().then(res => res.data),
            stakeholdersApi.getAll().then(res => res.data),
            projectsApi.getAll().then(res => res.data)
        ]);

        console.log('[4] Datos existentes:', {
            roles: existingRoles,
            levels: existingLevels,
            persons: existingPersons,
            stakeholders: existingStakeholders,
            projects: existingProjects
        });

        // 5. Mapeos de IDs
        const roleIdMap = {};
        const levelIdMap = {};
        const personIdMap = {};
        const stakeholderIdMap = {};
        const projectIdMap = {}; // Nuevo mapa para proyectos

        // Función para obtener ID de un registro recién creado
        const getCreatedId = async (api, searchCriteria, idFieldName) => {
            const allItems = await api.getAll().then(res => res.data);
            const foundItem = allItems.find(item =>
                Object.keys(searchCriteria).every(key =>
                    String(item[key]).toLowerCase() === String(searchCriteria[key]).toLowerCase()
                )
            );
            return foundItem ? foundItem[idFieldName] : null;
        };

        // ----------------- ETAPA 1: ROLES Y NIVELES -----------------
        console.log('[5] ETAPA 1: Procesando roles y niveles');

        // Procesar roles (sin cambios)
        if (excelSheets.roles) {
            for (const role of excelSheets.roles) {
                const exists = existingRoles.find(r =>
                    r.role_description.toLowerCase() === role.role_description.toLowerCase()
                );

                if (exists) {
                    roleIdMap[role.role_id] = exists.role_id;
                    console.log(`Role existente mapeado: ${role.role_id} -> ${exists.role_id}`);
                } else if (role.role_description) {
                    try {
                        await rolesApi.create({
                            description: role.role_description
                        });

                        const newRoleId = await getCreatedId(
                            rolesApi,
                            { role_description: role.role_description },
                            'role_id'
                        );

                        if (newRoleId) {
                            roleIdMap[role.role_id] = newRoleId;
                            results.roles.push({ role_id: newRoleId, role_description: role.role_description });
                            console.log(`Nuevo role creado: ${role.role_id} -> ${newRoleId}`);
                        }
                    } catch (error) {
                        console.error(`Error procesando role ${role.role_id}:`, error);
                        throw error;
                    }
                }
            }
        }

        // Procesar niveles (sin cambios)
        if (excelSheets.levels) {
            for (const level of excelSheets.levels) {
                const exists = existingLevels.find(l =>
                    l.level_description.toLowerCase() === level.level_description.toLowerCase()
                );

                if (exists) {
                    levelIdMap[level.level_id] = exists.level_id;
                    console.log(`Nivel existente mapeado: ${level.level_id} -> ${exists.level_id}`);
                } else if (level.level_description) {
                    try {
                        await levelsApi.create({
                            description: level.level_description
                        });

                        const newLevelId = await getCreatedId(
                            levelsApi,
                            { level_description: level.level_description },
                            'level_id'
                        );

                        if (newLevelId) {
                            levelIdMap[level.level_id] = newLevelId;
                            results.levels.push({ level_id: newLevelId, level_description: level.level_description });
                            console.log(`Nuevo nivel creado: ${level.level_id} -> ${newLevelId}`);
                        }
                    } catch (error) {
                        console.error(`Error procesando nivel ${level.level_id}:`, error);
                        throw error;
                    }
                }
            }
        }

        // ----------------- ETAPA 2: PERSONAS Y STAKEHOLDERS -----------------
        console.log('[6] ETAPA 2: Procesando personas y stakeholders');

        // Procesar personas (sin cambios)
        if (excelSheets.persons) {
            for (const person of excelSheets.persons) {
                const exists = existingPersons.find(p =>
                    p.person_firstname.toLowerCase() === person.person_firstname.toLowerCase() &&
                    p.person_lastname.toLowerCase() === person.person_lastname.toLowerCase()
                );

                if (exists) {
                    personIdMap[person.person_id] = exists.person_id;
                    console.log(`Persona existente mapeada: ${person.person_id} -> ${exists.person_id}`);
                } else if (person.person_firstname && person.person_lastname) {
                    try {
                        await personsApi.create({
                            firstname: person.person_firstname,
                            lastname: person.person_lastname,
                            location: person.person_location || '',
                            urlsite: person.person_urlsite || ''
                        });

                        const newPersonId = await getCreatedId(
                            personsApi,
                            {
                                person_firstname: person.person_firstname,
                                person_lastname: person.person_lastname
                            },
                            'person_id'
                        );

                        if (newPersonId) {
                            personIdMap[person.person_id] = newPersonId;
                            results.persons.push({
                                person_id: newPersonId,
                                person_firstname: person.person_firstname,
                                person_lastname: person.person_lastname,
                                person_location: person.person_location || '',
                                person_urlsite: person.person_urlsite || ''
                            });
                            console.log(`Nueva persona creada: ${person.person_id} -> ${newPersonId}`);
                        }
                    } catch (error) {
                        console.error(`Error procesando persona ${person.person_id}:`, error);
                        throw error;
                    }
                }
            }
        }

        // Procesar stakeholders (sin cambios)
        if (excelSheets.stakeholders) {
            for (const stakeholder of excelSheets.stakeholders) {
                const personId = personIdMap[stakeholder.person_id];
                const roleId = roleIdMap[stakeholder.role_id];

                console.log(`Procesando stakeholder: persona=${stakeholder.person_id}->${personId}, rol=${stakeholder.role_id}->${roleId}`);

                if (!personId || !roleId) {
                    console.warn(`Faltan IDs para stakeholder - persona: ${personId}, rol: ${roleId}`);
                    continue;
                }

                const exists = [...existingStakeholders, ...results.stakeholders].find(s =>
                    s.person_id == personId && s.role_id == roleId
                );

                if (exists) {
                    stakeholderIdMap[stakeholder.stakeholder_id] = exists.stakeholder_id;
                    console.log(`Stakeholder existente mapeado: ${stakeholder.stakeholder_id} -> ${exists.stakeholder_id}`);
                } else {
                    try {
                        await stakeholdersApi.create({
                            person_id: personId,
                            role_id: roleId
                        });

                        const newStakeholderId = await getCreatedId(
                            stakeholdersApi,
                            {
                                person_id: personId,
                                role_id: roleId
                            },
                            'stakeholder_id'
                        );

                        if (newStakeholderId) {
                            stakeholderIdMap[stakeholder.stakeholder_id] = newStakeholderId;
                            results.stakeholders.push({
                                stakeholder_id: newStakeholderId,
                                person_id: personId,
                                role_id: roleId
                            });
                            console.log(`Nuevo stakeholder creado: ${stakeholder.stakeholder_id} -> ${newStakeholderId}`);
                        }
                    } catch (error) {
                        console.error(`Error creando stakeholder:`, error);
                    }
                }
            }
        }

        // ----------------- ETAPA 3: PROYECTOS Y ASIGNACIONES -----------------
        console.log('[7] ETAPA 3: Procesando proyectos y asignaciones');

        // Procesar proyectos (modificado para incluir projectIdMap)
        if (excelSheets.projects) {
            for (const project of excelSheets.projects) {
                const levelId = levelIdMap[project.level_id];

                console.log(`Procesando proyecto: ${project.project_name}, nivel ${project.level_id}->${levelId}`);

                if (!levelId) {
                    console.warn(`Nivel no encontrado para proyecto ${project.project_name}`);
                    continue;
                }

                if (!project.project_name) {
                    console.warn(`Proyecto sin nombre - omitiendo`);
                    continue;
                }

                // Verificar si proyecto ya existe
                const exists = existingProjects.find(p =>
                    p.project_name.toLowerCase() === project.project_name.toLowerCase() &&
                    p.level_id == levelId
                );

                if (exists) {
                    projectIdMap[project.project_id] = exists.project_id;
                    console.log(`Proyecto existente mapeado: ${project.project_id} -> ${exists.project_id}`);
                } else {
                    try {
                        await projectsApi.create({
                            name: project.project_name,
                            description: project.project_description || '',
                            keywords: project.project_keywords || '',
                            agno: project.project_agno || new Date().getFullYear(),
                            level_id: levelId,
                        });

                        const newProjectId = await getCreatedId(
                            projectsApi,
                            {
                                project_name: project.project_name,
                                level_id: levelId
                            },
                            'project_id'
                        );

                        if (newProjectId) {
                            projectIdMap[project.project_id] = newProjectId;
                            results.projects.push({
                                project_id: newProjectId,
                                project_name: project.project_name,
                                project_description: project.project_description || '',
                                project_keywords: project.project_keywords || '',
                                project_agno: project.project_agno || new Date().getFullYear(),
                                level_id: levelId,
                            });
                            console.log(`Proyecto creado: ${newProjectId} - ${project.project_name}`);
                        }
                    } catch (error) {
                        console.error(`Error creando proyecto ${project.project_name}:`, error);
                    }
                }
            }
        }

        // Procesar asignaciones proyecto-stakeholder (versión corregida)
        if (excelSheets.project_stakeholders) {
            const allProjectStakeholders = await projectStakeholdersApi.getAll().then(res => res.data).catch(() => []);

            for (const ps of excelSheets.project_stakeholders) {
                const realProjectId = projectIdMap[ps.project_id];
                const realStakeholderId = stakeholderIdMap[ps.stakeholder_id];

                console.log(`Asignación: proyecto=${ps.project_id}->${realProjectId}, stakeholder=${ps.stakeholder_id}->${realStakeholderId}`);

                if (!realProjectId || !realStakeholderId) {
                    console.warn(`Faltan IDs para asignación - proyecto: ${realProjectId}, stakeholder: ${realStakeholderId}`);
                    continue;
                }

                const exists = allProjectStakeholders.some(existingPs =>
                    existingPs.project_id === realProjectId &&
                    existingPs.stakeholder_id === realStakeholderId
                );

                if (!exists) {
                    try {
                        const res = await projectStakeholdersApi.create({
                            project_id: realProjectId,
                            stakeholder_id: realStakeholderId
                        });
                        results.projectStakeholders.push(res.data);
                        console.log(`Asignación creada: proyecto ${realProjectId} - stakeholder ${realStakeholderId}`);
                    } catch (error) {
                        console.error(`Error creando asignación proyecto-stakeholder:`, error);
                    }
                } else {
                    console.log(`Asignación existente: proyecto ${realProjectId} - stakeholder ${realStakeholderId}`);
                }
            }
        }

        return {
            success: true,
            message: 'Datos importados correctamente',
            details: {
                roles: results.roles,
                levels: results.levels,
                persons: results.persons,
                stakeholders: results.stakeholders,
                projects: results.projects,
                projectStakeholders: results.projectStakeholders,
                idMappings: {
                    roles: roleIdMap,
                    levels: levelIdMap,
                    persons: personIdMap,
                    stakeholders: stakeholderIdMap,
                    projects: projectIdMap
                }
            }
        };
    } catch (error) {
        console.error('Error en el proceso de importación:', error);
        return {
            success: false,
            message: error.response?.data?.message || error.message,
            details: null
        };
    }
}

// Función auxiliar para normalizar datos del Excel
function normalizeExcelData(excelSheets) {
    const normalized = { ...excelSheets };

    Object.keys(normalized).forEach(sheetName => {
        normalized[sheetName] = normalized[sheetName].map(item => {
            const newItem = { ...item };
            Object.keys(newItem).forEach(key => {
                if (key.endsWith('_id') && newItem[key] !== undefined && newItem[key] !== null) {
                    newItem[key] = Number(newItem[key]);
                }
            });
            return newItem;
        });
    });

    return normalized;
}