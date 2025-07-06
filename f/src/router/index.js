import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/user/HomePage.vue";
import NotFound from "../views/NotFound.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Usuario Externo
    {
      path: "/",
      name: "inicio",
      component: HomePage,
    },
    {
      path: "/proyectos",
      name: "proyectos",
      component: () => import("../views/user/ProjectsPage.vue"),
    },
    {
      path: "/nosotros",
      name: "nosotros",
      component: () => import("../views/user/AboutPage.vue"),
    },
    {
      path: "/proyectos/:id",
      name: "proyecto-detalle",
      component: () => import("../views/user/ProjectDetails.vue"),
    },
    {
      path: "/investigadores",
      name: "investigadores",
      component: () => import("../views/user/ResearcherPage.vue"),
    },
    // Usuario Interno
    {
      path: "/login",
      name: "login",
      component: () => import("../views/auth/LoginPage.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("../layouts/AdminLayout.vue"),
      meta: { requiresAuth: true }, // Esta ruta requiere autenticación
      children: [
        {
          path: "",
          name: "admin-proyectos",
          component: () => import("../views/admin/ProyectosPage.vue"),
        },
        {
          path: "personas",
          name: "admin-personas",
          component: () => import("../views/admin/PersonasPage.vue"),
        },
        {
          path: "roles",
          name: "admin-roles",
          component: () => import("../views/admin/RolesPage.vue"),
        },
        {
          path: "niveles",
          name: "admin-niveles",
          component: () => import("../views/admin/NivelesPage.vue"),
        },
        {
          path: "project-assignments",
          name: "admin-asignaciones",
          component: () => import("../views/admin/ProjectAssignmentsPage.vue"),
        },
        {
          path: "guia-template-csv",
          name: "guia-template-csv",
          component: () => import("../../public/guideTemplate.html"),
        },
      ],
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFound,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // Bloquea el acceso a rutas protegidas
  } else {
    next();
  }
});

export default router;