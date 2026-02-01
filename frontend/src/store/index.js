import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
})

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    data: null,
    loading: false,
  }),
  actions: {
    async fetch() {
      this.loading = true
      try {
        const res = await api.get('/dashboard/')
        this.data = res.data
      } finally {
        this.loading = false
      }
    },
  },
})

export const useAvitoStore = defineStore('avito', {
  state: () => ({
    accounts: [],
    ads: [],
    templates: [],
    competitors: [],
    messages: [],
    autoReplies: [],
    loading: false,
  }),
  actions: {
    async fetchAccounts() {
      this.loading = true
      try {
        const res = await api.get('/avito/accounts')
        this.accounts = res.data
      } finally { this.loading = false }
    },
    async createAccount(data) {
      const res = await api.post('/avito/accounts', data)
      this.accounts.push(res.data)
      return res.data
    },
    async deleteAccount(id) {
      await api.delete(`/avito/accounts/${id}`)
      this.accounts = this.accounts.filter(a => a.id !== id)
    },
    async fetchAds() {
      this.loading = true
      try {
        const res = await api.get('/avito/ads')
        this.ads = res.data
      } finally { this.loading = false }
    },
    async createAd(data) {
      const res = await api.post('/avito/ads', data)
      this.ads.push(res.data)
      return res.data
    },
    async deleteAd(id) {
      await api.delete(`/avito/ads/${id}`)
      this.ads = this.ads.filter(a => a.id !== id)
    },
    async publishAd(id) {
      return (await api.post(`/avito/ads/${id}/publish`)).data
    },
    async fetchTemplates() {
      this.loading = true
      try {
        const res = await api.get('/avito/templates')
        this.templates = res.data
      } finally { this.loading = false }
    },
    async fetchCompetitors() {
      this.loading = true
      try {
        const res = await api.get('/avito/competitors')
        this.competitors = res.data
      } finally { this.loading = false }
    },
    async createCompetitor(data) {
      const res = await api.post('/avito/competitors', data)
      this.competitors.push(res.data)
      return res.data
    },
    async fetchMessages() {
      this.loading = true
      try {
        const res = await api.get('/avito/messages')
        this.messages = res.data
      } finally { this.loading = false }
    },
    async fetchAutoReplies() {
      const res = await api.get('/avito/auto-replies')
      this.autoReplies = res.data
    },
    async createAutoReply(data) {
      const res = await api.post('/avito/auto-replies', data)
      this.autoReplies.push(res.data)
      return res.data
    },
  },
})

export const useEmailStore = defineStore('email', {
  state: () => ({
    campaigns: [],
    templates: [],
    loading: false,
  }),
  actions: {
    async fetchCampaigns() {
      this.loading = true
      try {
        const res = await api.get('/email/campaigns')
        this.campaigns = res.data
      } finally { this.loading = false }
    },
    async createCampaign(data) {
      const res = await api.post('/email/campaigns', data)
      this.campaigns.push(res.data)
      return res.data
    },
    async sendCampaign(id) {
      return (await api.post(`/email/campaigns/${id}/send`)).data
    },
    async fetchTemplates() {
      this.loading = true
      try {
        const res = await api.get('/email/templates')
        this.templates = res.data
      } finally { this.loading = false }
    },
    async createTemplate(data) {
      const res = await api.post('/email/templates', data)
      this.templates.push(res.data)
      return res.data
    },
  },
})

export const useContactStore = defineStore('contacts', {
  state: () => ({
    contacts: [],
    segments: [],
    loading: false,
  }),
  actions: {
    async fetchContacts() {
      this.loading = true
      try {
        const res = await api.get('/contacts/')
        this.contacts = res.data
      } finally { this.loading = false }
    },
    async createContact(data) {
      const res = await api.post('/contacts/', data)
      this.contacts.push(res.data)
      return res.data
    },
    async deleteContact(id) {
      await api.delete(`/contacts/${id}`)
      this.contacts = this.contacts.filter(c => c.id !== id)
    },
    async importContacts(file) {
      const form = new FormData()
      form.append('file', file)
      return (await api.post('/contacts/import', form)).data
    },
    async fetchSegments() {
      this.loading = true
      try {
        const res = await api.get('/contacts/segments/')
        this.segments = res.data
      } finally { this.loading = false }
    },
    async createSegment(data) {
      const res = await api.post('/contacts/segments/', data)
      this.segments.push(res.data)
      return res.data
    },
  },
})
