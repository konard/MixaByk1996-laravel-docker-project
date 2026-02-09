import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('../views/DashboardView.vue') },
  // Avito
  { path: '/avito/accounts', name: 'AvitoAccounts', component: () => import('../views/avito/AccountsView.vue') },
  { path: '/avito/ads', name: 'AvitoAds', component: () => import('../views/avito/AdsView.vue') },
  { path: '/avito/templates', name: 'AvitoTemplates', component: () => import('../views/avito/TemplatesView.vue') },
  { path: '/avito/competitors', name: 'AvitoCompetitors', component: () => import('../views/avito/CompetitorsView.vue') },
  { path: '/avito/messages', name: 'AvitoMessages', component: () => import('../views/avito/MessagesView.vue') },
  // Email
  { path: '/email/campaigns', name: 'EmailCampaigns', component: () => import('../views/email/CampaignsView.vue') },
  { path: '/email/templates', name: 'EmailTemplates', component: () => import('../views/email/TemplatesView.vue') },
  // Contacts
  { path: '/contacts', name: 'Contacts', component: () => import('../views/contacts/ContactsView.vue') },
  { path: '/contacts/segments', name: 'ContactSegments', component: () => import('../views/contacts/SegmentsView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
